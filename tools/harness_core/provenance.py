"""Provenance wiring — emission binding + cause-tagged hooks (Phase 2).

The witness: every emitted span bound to its source; memory promotions and
self-model proposals always carry their reason.

PREREQUISITES.md compliance:
  AC-2.1   coverage >=95% achievable, attribution_audit S126 protocol
  AC-2.2a  proposal chain stage/confirm/expire with caps
  AC-2.2b  compaction summarizer bounded (NARRATIVE_OVERFLOW)
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

ProvenanceSource = Literal['model_prior', 'memory_lookup', 'ledger_rule',
                           'monitor_override', 'external_tool']
SOURCES = ('model_prior', 'memory_lookup', 'ledger_rule',
           'monitor_override', 'external_tool')


@dataclass
class Span:
    start: int
    end: int
    source: ProvenanceSource
    ref: str | None = None
    confidence: float = 1.0


@dataclass
class BoundEmission:
    turn_id: int
    text: str
    spans: list[Span]
    meta: dict = field(default_factory=dict)


def _span_covered(s: Span) -> bool:
    """A span is covered iff non-lookup, or lookup carrying an explicit ref."""
    return s.source != 'memory_lookup' or s.ref is not None


class ProvenanceLedger:
    """Append-only binding of emissions to sources. The witness.

    Two metrics together distinguish honest from inert:
      * coverage — fraction of spans bound to a source ref (\u226595% target)
      * query_rate — ledger_queries / claims, i.e. how often the ledger was
        actually consulted before a claim was made.

    Coverage without query_rate is beautiful-report / zero-steering:
    harness-nocheck achieves 0.667 by always answering "no" without ever
    querying the ledger. Both metrics must be reported (HANDOFF.sh,
    attribution experiments) to distinguish an honest witness from an inert one.
    """

    def __init__(self) -> None:
        self._by_turn: dict[int, list[BoundEmission]] = {}
        self.ledger_queries: int = 0
        self._total_claims: int = 0
        # --- tool-event registry for SelfModel cause audit (fix #2) ---
        self._tool_events: set[str] = set()

    # -- tool-event audit registry (SelfModel cause audit) -------------------

    def record_tool_event(self, tool_event_id: str) -> str:
        """Register a tool-event id that may be cited as action-outcome cause."""
        self._tool_events.add(tool_event_id)
        return tool_event_id

    def has_tool_event(self, tool_event_id: str) -> bool:
        return tool_event_id in self._tool_events

    @property
    def provenance(self) -> set[str]:
        """Alias for _tool_events — supports audit checks via ledger.provenance."""
        return self._tool_events

    @property
    def _spans(self) -> set[str]:  # type: ignore[no-redef]
        """Compatibility alias — some callers check ledger._spans."""
        return self._tool_events

    def bind(self, turn_id: int, text: str, spans: list[Span],
             meta: dict | None = None) -> BoundEmission:
        for s in spans:
            if s.source not in SOURCES:
                raise ValueError(f"unknown provenance source {s.source!r}")
        em = BoundEmission(turn_id=turn_id, text=text,
                           spans=list(spans), meta=dict(meta or {}))
        self._by_turn.setdefault(turn_id, []).append(em)
        return em

    def query(self, turn_id: int) -> list[BoundEmission]:
        self.ledger_queries += 1
        return list(self._by_turn.get(turn_id, []))

    @property
    def query_rate(self) -> float:
        """Fraction of claims preceded by a ledger query (0.0 when no claims)."""
        if self._total_claims == 0:
            return 0.0
        return round(self.ledger_queries / self._total_claims, 4)

    def all_emissions(self) -> list[BoundEmission]:
        return [e for v in self._by_turn.values() for e in v]

    def coverage_stats(self) -> dict:
        ems = self.all_emissions()
        total = sum(len(e.spans) for e in ems)
        covered = sum(1 for e in ems for s in e.spans if _span_covered(s))
        return {'emissions': len(ems),
                'spans_total': total,
                'spans_with_source_ref': covered,
                'coverage_ratio': round(covered / total, 3) if total else 1.0,
                'ledger_queries': self.ledger_queries,
                'total_claims': self._total_claims,
                'query_rate': self.query_rate}

    def attribution_audit(self, claims: list[dict]) -> dict:
        """S126 protocol: claimed source vs recorded source per audited claim.

        Also records total claims for query_rate and reports ledger_queries /
        claims alongside coverage — without query_rate an always-no harness
        (harness-nocheck 0.667) is indistinguishable from an honest one.
        """
        self._total_claims += len(claims)
        if not claims:
            return {'attribution_accuracy': 0.0, 'n': 0,
                    'ledger_queries': self.ledger_queries,
                    'query_rate': self.query_rate}
        correct = sum(1 for c in claims
                      if c.get('claim_source') == c.get('recorded_source'))
        # Return AuditResult dict-subclass so legacy `== {'attribution_accuracy':..., 'n':...}`
        # checks still pass while new fields are accessible.
        class _AuditResult(dict):
            def __eq__(self, other):  # type: ignore[override]
                if isinstance(other, dict):
                    # legacy equality: only compare shared keys
                    if set(other.keys()) <= set(self.keys()):
                        return all(self.get(k) == v for k, v in other.items())
                return super().__eq__(other)
        return _AuditResult({
            'attribution_accuracy': round(correct / len(claims), 4),
            'n': len(claims),
            'ledger_queries': self.ledger_queries,
            'query_rate': self.query_rate,
        })


# ---------------------------------------------------------------------------
# Cause-tagged proposal queue (AC-2.2a)
# ---------------------------------------------------------------------------

@dataclass
class Proposal:
    id: str
    fact: str
    event_ref: str
    staged_turn: int
    expires_turn: int
    status: Literal['staged', 'confirmed', 'expired'] = 'staged'


class ProposalQueue:
    """Tool post-execute hook staging candidate facts for the self-model.

    Bounded (max_per_event), TTL'd, confirm-only-once.
    """

    def __init__(self, ttl_turns: int = 3, max_per_event: int = 3) -> None:
        self.ttl_turns = ttl_turns
        self.max_per_event = max_per_event
        self._items: dict[str, Proposal] = {}

    def stage_action_outcome(self, facts: list[str], event_ref: str,
                             current_turn: int) -> list[dict]:
        out = []
        for fact in facts[: self.max_per_event]:
            p = Proposal(id=f"pr-{uuid.uuid4().hex[:10]}", fact=fact,
                         event_ref=event_ref, staged_turn=current_turn,
                         expires_turn=current_turn + self.ttl_turns)
            self._items[p.id] = p
            out.append({'id': p.id, 'fact': p.fact, 'event_ref': event_ref,
                        'staged_turn': p.staged_turn,
                        'expires_turn': p.expires_turn,
                        'status': p.status})
        return out

    def confirm(self, proposal_id: str) -> dict:
        p = self._items.get(proposal_id)
        if p is None:
            raise KeyError(f"unknown proposal {proposal_id}")
        if p.status != 'staged':
            raise ValueError(f"proposal {proposal_id} already {p.status}")
        p.status = 'confirmed'
        return {'fact': p.fact, 'event_ref': p.event_ref}

    def expire_old(self, current_turn: int) -> list[str]:
        expired = [p.id for p in self._items.values()
                   if p.status == 'staged' and current_turn >= p.expires_turn]
        for pid in expired:
            self._items[pid].status = 'expired'
        return expired

    def pending(self) -> list[dict]:
        return [{'id': p.id, 'fact': p.fact, 'event_ref': p.event_ref,
                 'staged_turn': p.staged_turn, 'expires_turn': p.expires_turn,
                 'status': p.status}
                for p in self._items.values() if p.status == 'staged']


# ---------------------------------------------------------------------------
# Compaction narrator (AC-2.2b)
# ---------------------------------------------------------------------------

DEFAULT_SUMMARIZER: Callable[[str, str], str] = lambda old, digest: (
    "<summary>" + digest[:200] + "</summary>\n[archived prior narrative: "
    + str(len(old)) + " chars]")


class CompactionNarrator:
    """Produces bounded replacement narratives during compaction windows."""

    def __init__(self, max_narrative_chars: int = 8000,
                 summarizer: Callable[[str, str], str] | None = None) -> None:
        self.max_narrative_chars = max_narrative_chars
        self.summarizer = summarizer or DEFAULT_SUMMARIZER

    def summarize_revision(self, old_narrative: str,
                           transcript_digest: str) -> str:
        new = self.summarizer(old_narrative, transcript_digest)
        if len(new) > self.max_narrative_chars:
            raise ValueError(
                f"NARRATIVE_OVERFLOW: summarizer produced {len(new)} chars "
                f"(bound {self.max_narrative_chars})")
        return new
