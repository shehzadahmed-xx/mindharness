"""Witnessed memory consolidation (Phase 5).

Three-phase pipeline modeled on OpenClaw Dreaming / EverMemOS, with our
addition: every promotion carries a signed cause tag. NO UNTAGGED PROMOTION
EVER — enforced by assertion in the DEEP writer (AC-5.1 hard invariant).

PREREQUISITES.md compliance:
  AC-5.1  100% promotions carry cause in enum
  AC-5.2  utility gate: >=2 distinct query types OR human_endorsed
  AC-5.3  REM-ablation switch observably changes output
"""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

Cause = Literal['action-outcome', 'narrative-summary', 'external-write']
CAUSES = ('action-outcome', 'narrative-summary', 'external-write')
Tier = Literal['episodic', 'semantic']


@dataclass
class MemoryItem:
    content: str
    tier: Tier = 'episodic'
    id: str = field(default_factory=lambda: f"mem-{uuid.uuid4().hex[:10]}")
    created_turn: int = 0
    query_hits: set[str] = field(default_factory=set)   # distinct query TYPES
    human_endorsed: bool = False
    # promotion fields (set only when promoted):
    cause: Cause | None = None
    source_refs: list[str] = field(default_factory=list)
    concept_tags: set[str] = field(default_factory=set)


@dataclass
class ConsolidationReport:
    deduped_removed: int
    rem_ran: bool
    candidates: list[dict]
    promoted: list[dict]
    skipped: list[dict]


class Consolidator:
    def __init__(
        self,
        items: dict[str, MemoryItem],
        *,
        rem_ablation: bool = False,
        min_query_types: int = 2,
        similarity_fn: Callable[[str, str], float] | None = None,
        dedup_threshold: float = 0.92,
        concept_tagger: Callable[[str], set[str]] | None = None,
    ) -> None:
        self.items = items                       # shared store, mutated in place
        self.rem_ablation = rem_ablation
        self.min_query_types = min_query_types
        self.similarity_fn = similarity_fn or self._lexical_sim
        self.dedup_threshold = dedup_threshold
        self.concept_tagger = concept_tagger or self._default_tags

    # -- helpers -----------------------------------------------------------

    @staticmethod
    def _lexical_sim(a: str, b: str) -> float:
        import difflib
        ta = [w.strip('.,!?;:').lower() for w in a.split()]
        tb = [w.strip('.,!?;:').lower() for w in b.split()]
        return difflib.SequenceMatcher(None, ta, tb).ratio()

    @staticmethod
    def _default_tags(content: str) -> set[str]:
        stop = {'the', 'a', 'an', 'and', 'or', 'of', 'to', 'in', 'on', 'is',
                'was', 'it', 'that', 'with', 'for'}
        return {w.strip('.,!?').lower() for w in content.split()
                if w.lower().strip('.,!?') not in stop and len(w) > 2}

    # -- phases --------------------------------------------------------------

    def light_pass(self) -> int:
        """Dedupe near-identical episodic traces; returns removed count."""
        eps = [i for i in self.items.values() if i.tier == 'episodic']
        removed = 0
        dropped: set[str] = set()
        ordered = sorted(eps, key=lambda i: i.created_turn)
        for i, a in enumerate(ordered):
            if a.id in dropped:
                continue
            for b in ordered[i + 1:]:
                if b.id in dropped:
                    continue
                if self.similarity_fn(a.content, b.content) >= self.dedup_threshold:
                    a.query_hits |= b.query_hits     # merge signal before drop
                    a.source_refs.extend(b.source_refs)
                    dropped.add(b.id)
        for did in dropped:
            del self.items[did]
            removed += 1
        return removed

    def rem_pass(self, current_turn: int) -> list[MemoryItem]:
        """Candidate extraction via concept tags. SKIPPED under ablation."""
        if self.rem_ablation:
            return []
        candidates: list[MemoryItem] = []
        for it in self.items.values():
            if it.tier != 'episodic':
                continue
            tags = self.concept_tagger(it.content)
            if not tags:
                continue
            it.concept_tags |= tags
            candidates.append(it)
        return candidates

    def _utility_ok(self, it: MemoryItem) -> tuple[bool, str]:
        if it.human_endorsed:
            return True, 'human_endorsed'
        if len(it.query_hits) >= self.min_query_types:
            return True, 'query_types'
        return False, (f'insufficient utility '
                       f'({len(it.query_hits)} query types, '
                       f'need {self.min_query_types})')

    def deep_pass(self, candidates: list[MemoryItem],
                  cause_by_id: dict[str, Cause]) -> tuple[list[dict], list[dict]]:
        """Promote passing candidates to semantic tier. HARD INVARIANT:
        every promotion carries cause in CAUSES — asserted, never defaulted."""
        promoted, skipped = [], []
        for it in candidates:
            ok, why = self._utility_ok(it)
            item_cause = cause_by_id.get(it.id)
            if ok:
                assert item_cause in CAUSES, (
                    f"UNTAGGED PROMOTION BLOCKED: {it.id} has cause "
                    f"{item_cause!r} — witnessed-consolidation invariant")
                it.tier = 'semantic'
                it.cause = item_cause
                promoted.append({'id': it.id, 'content': it.content[:80],
                                 'cause': it.cause,
                                 'via': why,
                                 'tags': sorted(it.concept_tags)[:6]})
            else:
                skipped.append({'id': it.id, 'reason': why})
        return promoted, skipped

    # -- entry -----------------------------------------------------------------

    def run(self, current_turn: int,
            cause_by_id: dict[str, Cause] | None = None,
            dry_run: bool = False) -> ConsolidationReport:
        cause_map = cause_by_id or {}
        deduped = self.light_pass()
        candidates_items = self.rem_pass(current_turn)

        preview_promoted, preview_skipped = [], []
        for it in candidates_items:
            ok, why = self._utility_ok(it)
            rec = {'id': it.id, 'content': it.content[:80],
                   'query_types': len(it.query_hits),
                   'endorsed': it.human_endorsed}
            (preview_promoted if ok else preview_skipped).append(
                {**rec, **({} if ok else {'reason': why})})

        promoted: list[dict] = []
        if not dry_run:
            promoted, skipped = self.deep_pass(candidates_items, cause_map)
            report = ConsolidationReport(deduped, not self.rem_ablation,
                                         [], promoted, skipped)
        else:
            report = ConsolidationReport(deduped, not self.rem_ablation,
                                         preview_promoted, [], preview_skipped)
        return report


def record_query_hit(items: dict[str, MemoryItem], memory_id: str,
                     query_type: str) -> None:
    it = items.get(memory_id)
    if it is not None:
        it.query_hits.add(query_type)


def endorse_human(items: dict[str, MemoryItem], memory_id: str) -> None:
    it = items.get(memory_id)
    if it is not None:
        it.human_endorsed = True
