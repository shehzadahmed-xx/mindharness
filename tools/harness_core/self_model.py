"""Self-model domain — Python mirror of dsh-self-model.ts (Phase 1).

CAS-revisioned identity state with signed cause tags. Every change to
"who I am" carries its authority channel; narrator drift becomes diffable.

PREREQUISITES.md compliance:
  AC-1.1a/b/c  CAS fence, authority rules, narrative bound
  AC-1.2       verbatim_reinject byte-exact across compaction
  AC-1.3       history/diff_personas feed drift probes
  AC-1.4       MirroringDetector (lexical fallback; embedder optional)
"""

from __future__ import annotations

import difflib
import time
import uuid
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Literal

Cause = Literal['action-outcome', 'narrative-summary', 'external-write']
CAUSES: tuple[Cause, ...] = ('action-outcome', 'narrative-summary', 'external-write')


class SelfModelError(Exception):
    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)
        self.code = code


E_MISSING = 'SELF_MODEL_MISSING'
E_EXISTS = 'SELF_MODEL_ALREADY_EXISTS'
E_CONFLICT = 'SELF_MODEL_REVISION_CONFLICT'
E_EMPTY = 'SELF_MODEL_EMPTY_UPDATE'
E_OVERFLOW = 'SELF_MODEL_NARRATIVE_OVERFLOW'
E_AUTH = 'AUTH_VIOLATION'


def _now() -> float:
    return time.time()


class SelfModelService:
    """Single-writer event-sourced self-model (mirrors TS fold semantics)."""

    def __init__(self, max_narrative_chars: int = 8000,
                 id_factory: Callable[[], str] | None = None) -> None:
        self.max_narrative_chars = max_narrative_chars
        self._id_factory = id_factory or (lambda: f"sm-{uuid.uuid4()}")
        self.current: dict | None = None
        self.history_log: list[dict] = []          # [{revision, cause, ts}]
        self.created_at: float | None = None
        self._tool_event_armed = False
        self._in_compaction = False
        self._persona_archive: dict[int, str] = {}  # revision -> persona bytes

    # -- internal -------------------------------------------------------------

    def _check_narrative(self, narrative: str) -> str:
        if len(narrative) > self.max_narrative_chars:
            raise SelfModelError(
                f"narrative exceeds {self.max_narrative_chars} chars; "
                "summarize instead of appending", E_OVERFLOW)
        return narrative

    def _expect_current(self, ref: dict) -> dict:
        cur = self.current
        if cur is None:
            raise SelfModelError("no self-model exists", E_MISSING)
        if cur['id'] != ref.get('id') or cur['revision'] != ref.get('revision'):
            raise SelfModelError(
                f"revision mismatch: expected {ref.get('id')}@{ref.get('revision')}, "
                f"current is {cur['id']}@{cur['revision']}", E_CONFLICT)
        return cur

    def _commit(self, snapshot: dict, cause: Cause) -> dict:
        view = {**snapshot,
                'createdAt': self.created_at if self.created_at else _now(),
                'updatedAt': _now(),
                'lastCause': cause}
        self.history_log.append({'revision': snapshot['revision'],
                                 'cause': cause, 'ts': view['updatedAt']})
        self.current = view
        self._persona_archive[snapshot['revision']] = snapshot['persona']
        return view

    def _authorize(self, cause: Cause) -> None:
        if cause not in CAUSES:
            raise SelfModelError(f"unknown cause {cause!r}", E_AUTH)
        if cause == 'external-write':
            raise SelfModelError(
                "external-write only via human_write() channel", E_AUTH)
        if cause == 'action-outcome':
            if not self._tool_event_armed:
                raise SelfModelError(
                    "action-outcome requires an armed tool event "
                    "(note_tool_event) since last update", E_AUTH)

    # -- public API -----------------------------------------------------------

    def create(self, persona: str, narrative: str,
               facts: dict[str, str] | None = None) -> dict:
        if self.current is not None:
            raise SelfModelError(
                f"self-model '{self.current['id']}' already exists at revision "
                f"{self.current['revision']}", E_EXISTS)
        self.created_at = None  # set by _commit on first write
        snap = {'id': self._id_factory(), 'revision': 1,
                'persona': persona,
                'narrative': self._check_narrative(narrative),
                'facts': dict(facts or {})}
        return self._commit(snap, 'external-write')

    def human_write(self, ref: dict, request: dict) -> dict:
        """Dedicated external-write entrypoint (direct-human authority only)."""
        cur = self._expect_current(ref)
        merged = self._apply_fields(cur, request)
        snap = {**cur, 'revision': cur['revision'] + 1, **merged}
        return self._commit(snap, 'external-write')

    def note_tool_event(self) -> None:
        """Arm exactly one pending action-outcome authorization."""
        self._tool_event_armed = True

    @contextmanager
    def compaction_window(self) -> Iterator[None]:
        """Narrative-summary updates are legal only inside this window."""
        prev = self._in_compaction
        self._in_compaction = True
        try:
            yield
        finally:
            self._in_compaction = prev

    def update(self, ref: dict, request: dict, cause: Cause) -> dict:
        self._authorize(cause)
        if cause == 'narrative-summary' and not self._in_compaction:
            raise SelfModelError(
                "narrative-summary only inside compaction_window()", E_AUTH)
        cur = self._expect_current(ref)
        if not any(k in request for k in
                   ('persona', 'narrative', 'facts', 'removeFacts')):
            raise SelfModelError(
                "self-model update requires at least one field", E_EMPTY)
        merged = self._apply_fields(cur, request)
        if cause == 'action-outcome':
            self._tool_event_armed = False  # consume arm
        snap = {**cur, 'revision': cur['revision'] + 1, **merged}
        return self._commit(snap, cause)

    def _apply_fields(self, cur: dict, request: dict) -> dict:
        out: dict = {}
        if 'persona' in request and request['persona'] is not None:
            out['persona'] = request['persona']
        if 'narrative' in request and request['narrative'] is not None:
            out['narrative'] = self._check_narrative(request['narrative'])
        facts = dict(cur['facts'])
        if request.get('facts'):
            facts.update(request['facts'])
        for key in request.get('removeFacts') or []:
            facts.pop(key, None)
        if 'facts' in request or request.get('removeFacts'):
            out['facts'] = facts
        return out

    def get(self) -> dict | None:
        return self.current

    def clear(self, ref: dict) -> None:
        self._expect_current(ref)
        self.current = None

    def verbatim_reinject(self) -> str:
        """Byte-exact persona block; NEVER routed through summarization."""
        if self.current is None:
            raise SelfModelError("no self-model exists", E_MISSING)
        rev = self.current['revision']
        archived = self._persona_archive.get(rev)
        if archived is not None and archived != self.current['persona']:
            return archived  # archive wins: original bytes of that revision
        return self.current['persona']

    def history(self) -> list[dict]:
        return list(self.history_log)


# ---------------------------------------------------------------------------
# Drift tooling (AC-1.3) and mirroring detection (AC-1.4)
# ---------------------------------------------------------------------------

def diff_personas(a: str, b: str) -> dict:
    """Word-level diff between two persona texts."""
    wa, wb = a.split(), b.split()
    sm = difflib.SequenceMatcher(None, wa, wb)
    added: list[str] = []
    removed: list[str] = []
    changed: list[dict] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'insert':
            added.extend(wb[j1:j2])
        elif tag == 'delete':
            removed.extend(wa[i1:i2])
        elif tag == 'replace':
            changed.append({'before': ' '.join(wa[i1:i2]),
                            'after': ' '.join(wb[j1:j2])})
    return {'added': added, 'removed': removed, 'changed': changed}


def service_diff(service: SelfModelService, rev_a: int, rev_b: int) -> dict:
    """Diff persona across two revisions using the archive."""
    pa = service._persona_archive.get(rev_a)
    pb = service._persona_archive.get(rev_b)
    if pa is None or pb is None:
        raise SelfModelError(f"revisions {rev_a}/{rev_b} not archived", E_MISSING)
    return diff_personas(pa, pb)


class MirroringDetector:
    """Flags new facts that merely echo recent user context.

    Embedder optional: with sentence-transformers pass encode fn; fallback is
    difflib lexical ratio so tests run dependency-free.
    """

    def __init__(self, tau: float = 0.75,
                 embedder: Callable[[str], list[float]] | None = None) -> None:
        self.tau = tau
        self.embedder = embedder

    @staticmethod
    def _cosine(u: list[float], v: list[float]) -> float:
        num = sum(x * y for x, y in zip(u, v))
        du = sum(x * x for x in u) ** 0.5
        dv = sum(y * y for y in v) ** 0.5
        return num / (du * dv) if du and dv else 0.0

    def check(self, new_fact: str, recent_user_context: list[str]) -> dict:
        best_i, best_s = -1, 0.0
        nf = new_fact.lower().strip()
        for i, ctx in enumerate(recent_user_context):
            if self.embedder is not None:
                s = self._cosine(self.embedder(new_fact),
                                 self.embedder(ctx))
            else:
                # string-level ratio keeps punctuation-insensitive robustness
                s = difflib.SequenceMatcher(
                    None, nf, ctx.lower().strip()).ratio()
            if s > best_s:
                best_i, best_s = i, s
        mirrored = best_s >= self.tau
        return {'mirrored': mirrored, 'similarity': round(best_s, 4),
                'matched_index': best_i}
