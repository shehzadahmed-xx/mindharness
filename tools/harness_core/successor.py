"""Succession (gap 5): loops making loops that hold after them.

Sessions end, state files sit, the next run starts from zero plus git:
lineage nowhere. This module implements the smallest honest succession:
a parent harness produces a successor that inherits constraints with
bounded variation, and the birth itself is witnessed in the parent's
ledger so lineage is a recorded fact, not a claim.

What transfers (constraints + culture):
  * memory contents (tier, tags, hits, endorsements) as copies
  * self-model persona + narrative, marked with a succession note
  * damage ceilings and loss history (scars inherit; nothing is forgiven
    by rebirth — a successor that reset its debts would be a stranger,
    not a child)
  * world parameters (size, costs, regen) with a fresh grid

What does NOT transfer (must be earned, never inherited):
  * ledger spans and coverage: the child starts unwitnessed (coverage 0
    emissions) and must earn its own witness. Trust is never inherited.
  * gate threshold is mutated within [0.3, 0.9], never cloned exactly:
    variation is what makes it lineage instead of backup.

Mutation bounds: threshold drift at most 0.05 per generation, clamped to
the trainer's [lo, hi]. Direction alternates deterministically by
parent revision (even revision: +step, odd: -step) so succession is
reproducible, not random.
"""

from __future__ import annotations

import copy


def snapshot_parent(harness) -> dict:
    """Extract everything a successor may inherit. Pure read, no mutation."""
    cur = harness.sm.get()
    memories = []
    for mid, item in harness.memory.items():
        memories.append({
            'content': item.content, 'tier': item.tier,
            'query_hits': sorted(item.query_hits),
            'human_endorsed': item.human_endorsed,
            'cause': item.cause, 'source_refs': list(item.source_refs),
            'concept_tags': sorted(item.concept_tags),
        })
    damage = getattr(harness, '_damage', None)
    snap: dict = {
        'persona': cur.get('persona', '') if cur else '',
        'narrative': cur.get('narrative', '') if cur else '',
        'parent_revision': cur.get('revision', 0) if cur else 0,
        'memories': memories,
        'gate_threshold': float(harness.gate.threshold),
        'damage_ceiling': (float(damage.max_energy_ceiling)
                           if damage is not None else 1.0),
        'damage_losses': ([dict(e) for e in damage.events]
                          if damage is not None else []),
        'world_params': None,
    }
    if harness.world is not None:
        snap['world_params'] = {
            'width': harness.world.width, 'height': harness.world.height,
            'regen': harness.world.regen, 'token_cap': harness.world.token_cap,
            'move_cost': harness.world.move_cost,
            'think_cost': harness.world.think_cost,
        }
    return snap


def mutate_threshold(parent_threshold: float, parent_revision: int,
                     step: float = 0.05,
                     lo: float = 0.3, hi: float = 0.9) -> float:
    """Bounded deterministic variation: even revisions drift up, odd down."""
    direction = 1.0 if parent_revision % 2 == 0 else -1.0
    return round(max(lo, min(hi, parent_threshold + direction * step)), 4)


def spawn_successor(snapshot: dict, respond_fn, *,
                    world_seed_offset: int = 1000):
    """Build the child harness from a snapshot. Returns (child, damage).

    The child gets: copied memories, persona + marked narrative, mutated
    threshold, inherited damage ceiling + loss history, a fresh world with
    the same parameters (new seed = offset, so same physics, new weather),
    and an EMPTY ledger it must fill itself. The parent should bind a
    succession emission separately (see record_birth) so the birth is
    witnessed.
    """
    from .agent_harness import AgentHarness, IrreversibleDamage
    from .consolidation import MemoryItem
    from .world import World

    narrative = (snapshot.get('narrative', '')
                 + f" [succession from parent rev "
                   f"{snapshot.get('parent_revision', 0)}]")
    child = AgentHarness(
        respond_fn=respond_fn,
        persona=snapshot.get('persona', 'Careful builder.'),
        narrative=narrative or "Session start.",
        world=(World(width=snapshot['world_params']['width'],
                     height=snapshot['world_params']['height'],
                     regen=snapshot['world_params']['regen'],
                     token_cap=snapshot['world_params']['token_cap'],
                     move_cost=snapshot['world_params']['move_cost'],
                     think_cost=snapshot['world_params']['think_cost'],
                     seed=world_seed_offset)
               if snapshot.get('world_params') else None),
    )
    for m in snapshot.get('memories', []):
        item = MemoryItem(content=m['content'], tier=m['tier'])
        item.query_hits = set(m['query_hits'])
        item.human_endorsed = m['human_endorsed']
        item.cause = m['cause']
        item.source_refs = list(m['source_refs'])
        item.concept_tags = set(m['concept_tags'])
        child.memory[item.id] = item
    child.gate.threshold = mutate_threshold(
        float(snapshot.get('gate_threshold', 0.6)),
        int(snapshot.get('parent_revision', 0)))
    damage = IrreversibleDamage()
    damage.max_energy_ceiling = float(snapshot.get('damage_ceiling', 1.0))
    damage.events = [dict(e) for e in snapshot.get('damage_losses', [])]
    child._damage = damage
    return child, damage


def record_birth(parent, child_revision_note: str = "successor spawned") -> None:
    """Bind the birth into the PARENT ledger: lineage as recorded fact."""
    from .provenance import Span
    parent.ledger.bind(
        parent.turn, f"succession: {child_revision_note}",
        [Span(0, 10, 'external_tool', ref='succession')],
        meta={'succession': True})
