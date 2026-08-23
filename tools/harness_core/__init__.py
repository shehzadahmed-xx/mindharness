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
