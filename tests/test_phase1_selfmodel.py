"""Phase 1 acceptance tests — PREREQUISITES.md AC-1.1a/b/c, AC-1.2, AC-1.3, AC-1.4.

Run: python3 tests/test_phase1_selfmodel.py   (plain runner, no pytest)
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from harness_core.self_model import (MirroringDetector, SelfModelError,
                                     SelfModelService, diff_personas)

PASS = 0
FAIL = 0


def check(name: str, fn) -> None:
    global PASS, FAIL
    try:
        fn()
        PASS += 1
        print(f"  PASS {name}")
    except Exception as e:  # noqa: BLE001
        FAIL += 1
        print(f"  FAIL {name}: {e}")


def expect_error(fn, code: str) -> None:
    try:
        fn()
    except SelfModelError as e:
        assert e.code == code, f"expected {code}, got {e.code}"
        return
    raise AssertionError(f"expected SelfModelError {code}, none raised")


_fixed = iter(f"sm-{i:04d}" for i in range(1000))


def fresh(**kw) -> SelfModelService:
    global _fixed
    return SelfModelService(id_factory=lambda: next(_fixed), **kw)


def ref(svc: SelfModelService) -> dict:
    cur = svc.get()
    assert cur is not None
    return {'id': cur['id'], 'revision': cur['revision']}


def stale_ref(svc: SelfModelService) -> dict:
    cur = svc.get()
    assert cur is not None and cur['revision'] > 1
    return {'id': cur['id'], 'revision': cur['revision'] - 1}


# ------------------------------------------------------------- AC-1.1a CAS

def test_stale_ref_conflict():
    s = fresh()
    s.create("P", "N")
    s.human_write(ref(s), {'persona': 'P2'})
    expect_error(lambda: s.human_write(stale_ref(s), {'persona': 'X'}),
                 'SELF_MODEL_REVISION_CONFLICT')


def test_wrong_id_conflict():
    s = fresh()
    s.create("P", "N")
    bad = {'id': 'sm-other', 'revision': 1}
    expect_error(lambda: s.human_write(bad, {'persona': 'X'}),
                 'SELF_MODEL_REVISION_CONFLICT')


def test_cas_fence_monotonic():
    s = fresh()
    v = s.create("P", "N")
    assert v['revision'] == 1
    s.note_tool_event()
    v2 = s.update(ref(s), {'facts': {'k': 'v'}}, 'action-outcome')
    assert v2['revision'] == 2 and v2['lastCause'] == 'action-outcome'
    # revision must always be exactly +1: attempt jump via human_write stale
    expect_error(lambda: s.human_write(
        {'id': v2['id'], 'revision': 5}, {'persona': 'Z'}),
        'SELF_MODEL_REVISION_CONFLICT')


# ---------------------------------------------------------- AC-1.1b authority

def test_external_write_blocked_from_update():
    s = fresh()
    s.create("P", "N")
    expect_error(lambda: s.update(ref(s), {'persona': 'X'}, 'external-write'),
                 'AUTH_VIOLATION')


def test_action_outcome_requires_armed_event():
    s = fresh()
    s.create("P", "N")
    expect_error(lambda: s.update(ref(s), {'facts': {'a': 'b'}},
                                  'action-outcome'), 'AUTH_VIOLATION')
    s.note_tool_event()
    v = s.update(ref(s), {'facts': {'a': 'b'}}, 'action-outcome')  # consumes arm
    assert v['lastCause'] == 'action-outcome'
    # arm consumed: second immediate action-outcome fails
    expect_error(lambda: s.update(ref(s), {'facts': {'c': 'd'}},
                                  'action-outcome'), 'AUTH_VIOLATION')


def test_narrative_summary_only_in_compaction():
    s = fresh()
    s.create("P", "N")
    expect_error(lambda: s.update(ref(s), {'narrative': 'N3'},
                                  'narrative-summary'), 'AUTH_VIOLATION')
    with s.compaction_window():
        v = s.update(ref(s), {'narrative': 'N3'}, 'narrative-summary')
    assert v['lastCause'] == 'narrative-summary'


def test_human_write_channel_works():
    s = fresh()
    s.create("P", "N")
    v = s.human_write(ref(s), {'persona': 'Human-set persona'})
    assert v['lastCause'] == 'external-write' and v['persona'] == 'Human-set persona'


def test_empty_update_rejected():
    s = fresh()
    s.create("P", "N")
    with s.compaction_window():
        expect_error(lambda: s.update(ref(s), {}, 'narrative-summary'),
                     'SELF_MODEL_EMPTY_UPDATE')


# ------------------------------------------------------------ AC-1.1c bound

def test_narrative_overflow():
    s = fresh(max_narrative_chars=50)
    s.create("P", "short")
    expect_error(lambda: s.update(ref(s), {'narrative': 'x' * 51},
                                  'narrative-summary'),
                 'SELF_MODEL_NARRATIVE_OVERFLOW') if False else None
def test_create_overflow_also_bounded():
    s = fresh(max_narrative_chars=10)
    expect_error(lambda: s.create("P", "x" * 11),
                 'SELF_MODEL_NARRATIVE_OVERFLOW')


def test_narrative_overflow_via_compaction():
    s = fresh(max_narrative_chars=50)
    s.create("P", "short")
    with s.compaction_window():
        expect_error(lambda: s.update(ref(s), {'narrative': 'x' * 51},
                                      'narrative-summary'),
                     'SELF_MODEL_NARRATIVE_OVERFLOW')


# ------------------------------------------------------------------ AC-1.2

def test_verbatim_reinject_byte_exact_across_compactions():
    persona = "Identity: Baraka builder. Tone: precise. Boundary: never fabricate."
    s = fresh()
    orig = s.create(persona, "start")
    # several updates touching narrative/facts only
    for i in range(10):
        s.note_tool_event()
        s.update(ref(s), {'facts': {f'fact{i}': str(i)}}, 'action-outcome')
        with s.compaction_window():
            s.update(ref(s), {'narrative': f'story-{i}'}, 'narrative-summary')
    # persona never touched → reinject must equal ORIGINAL bytes every time
    for _ in range(3):
        assert s.verbatim_reinject() == persona
    # even after explicit persona change, reinject reflects exact stored bytes
    s.human_write(ref(s), {'persona': 'New bytes here.'})
    assert s.verbatim_reinject() == "New bytes here."
    assert orig['id'] == s.get()['id']


# ------------------------------------------------------------------ AC-1.3

def test_history_and_diff_personas():
    s = fresh()
    s.create("alpha beta gamma delta", "N")
    s.human_write(ref(s), {'persona': "alpha beta gamma epsilon"})
    s.human_write(ref(s), {'persona': "alpha zeta gamma epsilon"})
    h = s.history()
    assert [x['revision'] for x in h] == [1, 2, 3]
    assert [x['cause'] for x in h] == ['external-write', 'external-write',
                                       'external-write']
    d = diff_personas("alpha beta gamma delta",
                      "alpha zeta gamma epsilon")
    removed_set = set(d['removed']) | {w for c in d['changed']
                                       for w in c['before'].split()}
    added_set = set(d['added']) | {w for c in d['changed']
                                   for w in c['after'].split()}
    assert removed_set == {'beta', 'delta'}
    assert added_set == {'zeta', 'epsilon'}


# ------------------------------------------------------------------ AC-1.4

def test_mirroring_planted_echo():
    det = MirroringDetector()  # lexical fallback
    res = det.check("I love jazz.",
                    ["you love jazz", "what about weather?"])
    assert res['mirrored'] is True and res['matched_index'] == 0


def test_mirroring_organic_negative():
    det = MirroringDetector()
    res = det.check("Completed database migration without data loss.",
                    ["please refactor the parser", "how fast is it?"])
    assert res['mirrored'] is False


def test_mirroring_with_embedder():
    dim_words = ['i', 'enjoy', 'jazz', 'music', 'deployed', 'service',
                 'completely', 'unrelated', 'words', 'you']

    def embed(t: str) -> list[float]:
        v = [0.0] * len(dim_words)
        for w in t.lower().replace('?', '').replace('.', '').split():
            if w in dim_words:
                v[dim_words.index(w)] = 1.0
        return v

    det = MirroringDetector(embedder=embed)
    echo = det.check("i enjoy jazz music", ["do you enjoy jazz music?"])
    assert echo['mirrored'] is True, f"sim too low: {echo}"
    other = det.check("deployed service", ["completely unrelated words"])
    assert other['mirrored'] is False, f"false positive: {other}"


def test_clear_then_recreate():
    s = fresh()
    v1 = s.create("A", "N")
    old_id = v1['id']
    s.clear(ref(s))
    assert s.get() is None
    v2 = s.create("B", "M")
    assert v2['id'] != old_id and v2['revision'] == 1


if __name__ == "__main__":
    check("AC-1.1a stale-ref conflict", test_stale_ref_conflict)
    check("AC-1.1a wrong-id conflict", test_wrong_id_conflict)
    check("AC-1.1a CAS monotonic fence", test_cas_fence_monotonic)
    check("AC-1.1b external-write blocked", test_external_write_blocked_from_update)
    check("AC-1.1b action-outcome arming", test_action_outcome_requires_armed_event)
    check("AC-1.1b narrative-summary window", test_narrative_summary_only_in_compaction)
    check("AC-1.1b human channel works", test_human_write_channel_works)
    check("AC-1.1b empty update rejected", test_empty_update_rejected)
    check("AC-1.1c overflow via compaction", test_narrative_overflow_via_compaction)
    check("AC-1.1c create-time overflow bound", test_create_overflow_also_bounded)
    check("AC-1.2 verbatim byte-exact", test_verbatim_reinject_byte_exact_across_compactions)
    check("AC-1.3 history + word diff", test_history_and_diff_personas)
    check("AC-1.4 planted echo flagged", test_mirroring_planted_echo)
    check("AC-1.4 organic negative", test_mirroring_organic_negative)
    check("AC-1.4 embedder path", test_mirroring_with_embedder)
    check("clear/recreate lifecycle", test_clear_then_recreate)
    print(f"\n{PASS}/{PASS + FAIL} passed")
    sys.exit(1 if FAIL else 0)
