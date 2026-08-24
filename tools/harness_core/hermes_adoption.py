"""Skill library and knowledge graph — Phase 6.5 Hermes adoptions, witnessed.

Both stores enforce the governing rule: every write carries a cause tag.
Untagged promotions/edges are structurally impossible (assert-blocked).

AC-6.5.1  skill created only from completed task loop, cause-tagged
AC-6.5.2  skill retrieval by lexical match, min-score gated
AC-6.5.3  graph edge requires cause in enum + source_refs non-empty
AC-6.5.4  multi-hop neighbor traversal returns paths
"""

from __future__ import annotations

import difflib
import time
import uuid
from dataclasses import dataclass, field
from typing import Literal

Cause = Literal['action-outcome', 'narrative-summary', 'external-write']
CAUSES = ('action-outcome', 'narrative-summary', 'external-write')


def _now() -> float:
    return time.time()


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


# ---------------------------------------------------------------------------
# Skill library (Hermes-Agent adoption, witnessed)
# ---------------------------------------------------------------------------

@dataclass
class Skill:
    name: str
    body: str                      # reusable instruction/procedure
    cause: Cause
    source_task_id: str
    uses: int = 0
    successes: int = 0
    created_at: float = field(default_factory=_now)

    @property
    def success_rate(self) -> float:
        return self.successes / self.uses if self.uses else 0.0


class SkillLibrary:
    def __init__(self, min_retrieval_score: float = 0.30) -> None:
        self.min_retrieval_score = min_retrieval_score
        self._skills: dict[str, Skill] = {}

    def add_from_task(self, name: str, body: str, task_id: str,
                      cause: Cause) -> Skill:
        """Skills enter ONLY from completed task loops (witnessed)."""
        if cause not in CAUSES:
            raise ValueError(f"unknown cause {cause!r}")
        if cause == 'narrative-summary':
            raise ValueError("skills cannot originate from narrative-summary")
        sk = Skill(name=name, body=body, cause=cause, source_task_id=task_id)
        self._skills[sk.name] = sk
        return sk

    def retrieve(self, task_description: str) -> list[tuple[Skill, float]]:
        out = []
        q = task_description.lower()
        for sk in self._skills.values():
            hay = (sk.name.replace('-', ' ') + ' '
                   + sk.body[:120]).lower()
            score = difflib.SequenceMatcher(None, q, hay).ratio()
            # also credit keyword overlap
            overlap = len(set(q.split()) & set(hay.split())) / max(1, len(set(q.split())))
            combined = max(score, overlap)
            if combined >= self.min_retrieval_score:
                out.append((sk, round(combined, 4)))
        return sorted(out, key=lambda x: -x[1])

    def record_use(self, name: str, success: bool) -> None:
        sk = self._skills[name]
        sk.uses += 1
        if success:
            sk.successes += 1

    def cull_failed(self, min_uses: int = 3, min_rate: float = 0.3) -> list[str]:
        """Selection rule: skills below success-rate after enough uses are DELETED."""
        culled = [n for n, s in self._skills.items()
                  if s.uses >= min_uses and s.success_rate < min_rate]
        for n in culled:
            del self._skills[n]
        return culled

    def all(self) -> list[Skill]:
        return list(self._skills.values())


# ---------------------------------------------------------------------------
# Knowledge graph (hermes-cognition adoption, witnessed)
# ---------------------------------------------------------------------------

@dataclass
class Edge:
    src: str
    rel: str
    dst: str
    cause: Cause
    source_refs: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=_now)


class KnowledgeGraph:
    def __init__(self) -> None:
        self.nodes: set[str] = set()
        self.edges: list[Edge] = []

    def add_node(self, concept: str) -> None:
        self.nodes.add(concept)

    def add_edge(self, src: str, rel: str, dst: str, cause: Cause,
                 source_refs: list[str] | None = None) -> Edge:
        # HARD INVARIANT: cause valid + at least one source ref
        assert cause in CAUSES, f"UNTAGGED EDGE BLOCKED: {src}-{rel}->{dst}"
        assert source_refs, "edge requires >=1 source_ref"
        self.nodes.update((src, dst))
        e = Edge(src=src, rel=rel, dst=dst, cause=cause,
                 source_refs=list(source_refs))
        self.edges.append(e)
        return e

    def neighbors(self, node: str) -> list[tuple[str, str]]:
        out = [(e.rel, e.dst) for e in self.edges if e.src == node]
        out += [(e.rel, e.src) for e in self.edges if e.dst == node]
        return out

    def multi_hop(self, start: str, hops: int = 2) -> list[list[str]]:
        """Paths of length <=hops from start: [[node, rel, node, ...]]."""
        paths: list[list[str]] = []
        frontier: list[list[str]] = [[start]]
        for _ in range(hops):
            nxt: list[list[str]] = []
            for p in frontier:
                cur = p[-1]
                for e in self.edges:
                    if e.src == cur and f"{e.rel}" not in p[-2:]:
                        nxt.append(p + [e.rel, e.dst])
                    elif e.dst == cur and f"{e.rel}" not in p[-2:]:
                        nxt.append(p + [e.rel, e.src])
            paths.extend(nxt)
            frontier = nxt
        return paths

