"""harness_core — hardened foundation for the Artificial Human Agent Harness.

Phase 0+ of BUILD_PLAN.md. Modules:
    backend         hardened Groq client (fingerprint discipline, capability matrix)
    run_discipline  prediction locks, manifests, abort conditions
"""

from .backend import (CAPABILITIES, BackendClient, CallRecord,
                      CapabilityError, FingerprintDrift)
from .run_discipline import (PredictionLock, RunManifest, assert_lock_committed,
                             hash_items_file)

__all__ = [
    "BackendClient", "CallRecord", "CapabilityError", "FingerprintDrift",
    "CAPABILITIES", "PredictionLock", "RunManifest", "assert_lock_committed",
    "hash_items_file",
]
from .self_model import MirroringDetector, SelfModelError, SelfModelService
from .provenance import (BoundEmission, CompactionNarrator, ProposalQueue,
                         ProvenanceLedger, Span)
from .monitor import (DetectSignals, MetacognitiveLog, MonitorGate, PostJOL,
                      PreSolveFOK)
from .embodiment import EmbodiedState
from .affect import AffectState
from .consolidation import Consolidator, MemoryItem
from .agent_harness import AgentHarness, TurnResult

__all__ += [
    "SelfModelService", "SelfModelError", "MirroringDetector",
    "ProvenanceLedger", "ProposalQueue", "CompactionNarrator",
    "Span", "BoundEmission",
    "MonitorGate", "DetectSignals", "MetacognitiveLog", "PreSolveFOK", "PostJOL",
    "EmbodiedState", "AffectState",
    "Consolidator", "MemoryItem",
    "AgentHarness", "TurnResult",
]
