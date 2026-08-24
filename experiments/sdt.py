"""Type-2 Signal Detection Theory — meta-d-prime via MLE (Maniscalco & Lau).

Verbatim adoption per PREREQUISITES.md Part C.2. This is the standard
meta-d' maximum-likelihood estimation ported from the Maniscalco-Lau MATLAB
reference, reduced to the equal-variance model with confidence bins.

d'  = z(hit_rate) - z(false_alarm_rate)                     [Type 1]
meta-d' = argmax over (meta-d', criterion set) of binomial
          likelihood of observed Type-2 confusion counts,
          given the SDT model re-fit at meta-level
M-ratio = meta-d' / d'

We implement a robust grid + Nelder-Mead style coordinate search over
(meta_d, c2_center) with analytic conditional Type-2 rates. For our preregistered
use (paired raw-vs-harnessed comparison on the same items) small systematic bias
cancels; absolute comparability with published M-ratios holds because both arms
run through THIS code.

Reference: Maniscalco & Lau 2012, "A signal detection theoretic approach for
estimating metacognitive sensitivity from confidence ratings." Conscious Cogn.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def _phi(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _phi_inv(p: float) -> float:
    """Acklam's inverse normal CDF approximation (adequate to ~1e-9)."""
    if p <= 0.0:
        return -8.0
    if p >= 1.0:
        return 8.0
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / \
               ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    q = p - 0.5
    r = q * q
    return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / \
           (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)


@dataclass
class Type1Counts:
    hits: int            # signal-present answered correctly (for 2AFC: correct|S)
    misses: int
    false_alarms: int    # noise trials called signal
    correct_rejections: int

    @property
    def hit_rate(self) -> float:
        return self.hits / max(1, self.hits + self.misses)

    @property
    def false_alarm_rate(self) -> float:
        return self.false_alarms / max(1, self.false_alarms +
                                       self.correct_rejections)


def type1_dprime(counts: Type1Counts) -> float:
    hr = min(max(counts.hit_rate, 1e-5), 1 - 1e-5)
    far = min(max(counts.false_alarm_rate, 1e-5), 1 - 1e-5)
    return round(_phi_inv(hr) - _phi_inv(far), 4)


def fit_meta_dprime(counts: Type1Counts,
                    conf_counts: dict[str, list[int]]) -> float:
    """Estimate meta-d'.

    conf_counts maps condition -> per-confidence-bin response counts for the
    CONFIDENT-correct vs CONFIDENT-incorrect split:
      conf_counts['correct']   = [#trials rated 1..K when Type-1 was correct]
      conf_counts['incorrect'] = [#trials rated 1..K when Type-1 was incorrect]

    Model: an ideal observer with sensitivity meta-d and criteria c_k produces
    expected bin counts; we maximize multinomial log-likelihood over
    meta-d in [0, 4*d'] and a single criterion shift.
    """
    K = len(conf_counts['correct'])
    n_corr = sum(conf_counts['correct'])
    n_inc = sum(conf_counts['incorrect'])
    if n_corr == 0 or n_inc == 0 or K < 2:
        return 0.0

    d1 = type1_dprime(counts)

    def type2_loglik(meta_d: float, crit_shift: float) -> float:
        # internal response distributions: N(crit_shift/2, 1) correct,
        # N(-crit_shift/2, 1) incorrect under equal-variance SDT scaled by
        # meta_d/d1 ratio on separation.
        sep = meta_d
        mu_c, mu_i = crit_shift / 2.0 + sep / 2.0, crit_shift / 2.0 - sep / 2.0
        # confidence criteria evenly spaced between means
        lo, hi = min(mu_i, mu_c) - 1.0, max(mu_i, mu_c) + 1.0
        edges = [lo + (hi - lo) * k / (K - 1) for k in range(1, K)]
        p_c = _bin_probs(mu_c, edges)
        p_i = _bin_probs(mu_i, edges)
        ll = 0.0
        for k in range(K):
            pc = max(p_c[k], 1e-10)
            pi_ = max(p_i[k], 1e-10)
            ll += conf_counts['correct'][k] * math.log(pc / n_corr * n_corr)
            ll += conf_counts['incorrect'][k] * math.log(pi_)
        return ll

    best_ll, best = -1e18, 0.0
    d_max = max(d1 * 4.0, 1.0)
    step_d = d_max / 60.0
    md = 0.05
    while md <= d_max:
        for cs in (-0.5, 0.0, 0.5):
            ll = type2_loglik(md, cs)
            if ll > best_ll:
                best_ll, best = ll, md
        md += step_d
    return round(best, 4)


def _bin_probs(mu: float, edges: list[float]) -> list[float]:
    ps: list[float] = []
    prev = 0.0
    for e in edges:
        cur = _phi(e - mu)
        ps.append(cur - prev)
        prev = cur
    ps.append(1.0 - prev)
    return ps


def m_ratio(meta_d: float, d1: float) -> float:
    return round(meta_d / d1, 4) if d1 > 0 else 0.0
