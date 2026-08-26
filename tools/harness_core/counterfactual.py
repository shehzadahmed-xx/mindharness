from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

from .consolidation import MemoryItem


@dataclass
class CounterfactualTrace:
    original_id: str
    original_content: str
    counterfactual_content: str
    simulated_outcome: str
    regret: float
    source: str


@dataclass
class CounterfactualReport:
    generated: list[CounterfactualTrace]
    high_regret: list[CounterfactualTrace]
    skipped: int


def default_variant_fn(content: str) -> list[str]:
    alts: list[str] = []
    if "abstain" in content.lower():
        alts.append(content.replace("abstain", "proceed"))
        alts.append(content.replace("abstain", "revise"))
    elif "proceed" in content.lower():
        alts.append(content.replace("proceed", "abstain"))
    else:
        alts.append(content + " [alternative framing]")
        alts.append(content + " [with witness check]")
    return alts[:2]


def default_simulate_fn(original: str, variant: str) -> tuple[str, float]:
    if "witness" in variant.lower() and "witness" not in original.lower():
        return "counterfactual reduces confabulation risk", 0.6
    if "abstain" in variant.lower() and "abstain" not in original.lower():
        return "counterfactual avoids premature commitment", 0.4
    if len(variant) > len(original) * 1.5:
        return "counterfactual adds verbosity without gain", -0.2
    return "counterfactual neutral vs original", 0.0


class CounterfactualReplay:
    def __init__(
        self,
        *,
        variant_fn: Callable[[str], list[str]] | None = None,
        simulate_fn: Callable[[str, str], tuple[str, float]] | None = None,
        regret_threshold: float = 0.3,
        max_per_item: int = 2,
        max_items: int = 8,
    ) -> None:
        self.variant_fn = variant_fn or default_variant_fn
        self.simulate_fn = simulate_fn or default_simulate_fn
        self.regret_threshold = regret_threshold
        self.max_per_item = max_per_item
        self.max_items = max_items

    def run(self, candidates: list[MemoryItem]) -> CounterfactualReport:
        generated: list[CounterfactualTrace] = []
        skipped = 0
        for it in candidates[: self.max_items]:
            variants = self.variant_fn(it.content)
            if not variants:
                skipped += 1
                continue
            for var in variants[: self.max_per_item]:
                outcome, regret = self.simulate_fn(it.content, var)
                generated.append(CounterfactualTrace(
                    original_id=it.id,
                    original_content=it.content[:120],
                    counterfactual_content=var[:120],
                    simulated_outcome=outcome,
                    regret=round(regret, 3),
                    source="counterfactual-replay",
                ))
        high = [t for t in generated if t.regret >= self.regret_threshold]
        return CounterfactualReport(generated=generated, high_regret=high, skipped=skipped)
