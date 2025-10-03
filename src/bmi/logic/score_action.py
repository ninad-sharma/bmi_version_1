"""
score_action.py
---------------
Scoring rules for user actions.

We use two measurement types:

1) Exact (includes binary):
   - Target T is an integer count (e.g., meals=3, cigarettes=0, meditate=1).
   - T > 0 → proportional deduction if off target, round UP; never < 0.
   - T = 0 → must do none: 10 if actual==0 else 0.

2) Range (target T, optional upper_limit U):
   A) If upper_limit is None (classic "max allowed"):
      - 10 stars at actual == T.
      - If actual <= T:   raw = 10 + (T - actual) * (10 / T); round UP; cap at 20. (0 → 20)
      - If actual >  T:   raw = 10 - (actual - T) * (10 / T); round DOWN; floor at 0. (zero at 2T)

   B) If upper_limit is provided (bonus region):
      - If actual <  T:   raw = (actual / T) * 10; round DOWN.      (0 → 0)
      - If T <= actual <= U:
                          raw = 10 + (actual - T) * (10 / (U - T)); round UP; cap at 20. (T→10, U→20)
      - If actual >  U:   score = 0 (hard cutoff).

All outputs are integers; global caps: 0 ≤ stars ≤ 20.
"""

import math
from typing import Optional


def score_exact(actual: int, target: int) -> int:
    if target < 0 or actual < 0:
        raise ValueError("actual and target must be non-negative integers")

    if target == 0:
        return 10 if actual == 0 else 0

    raw = (1 - abs(actual - target) / target) * 10
    return max(0, math.ceil(raw))


def score_range(actual: int, target: int, upper_limit: Optional[int] = None) -> int:
    if target <= 0 or actual < 0:
        raise ValueError("actual must be >= 0 and target must be > 0")
    if upper_limit is not None and upper_limit < target:
        raise ValueError("upper_limit must be >= target")

    if upper_limit is None:
        # "Max allowed" model (e.g., drinks). Fewer than target is better (up to 20).
        if actual <= target:
            raw = 10 + (target - actual) * (10 / target)
            return min(20, math.ceil(raw))
        else:
            raw = 10 - (actual - target) * (10 / target)
            return max(0, math.floor(raw))
    else:
        # Bonus up to U; hard zero beyond U.
        if actual < target:
            raw = (actual / target) * 10
            return math.floor(raw)
        elif actual <= upper_limit:
            raw = 10 + (actual - target) * (10 / (upper_limit - target))
            return min(20, math.ceil(raw))
        else:
            return 0
