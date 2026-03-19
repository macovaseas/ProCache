import random
from typing import List, Set, Tuple
from dataclasses import dataclass
from enum import IntEnum


# ==========================================
#  Configuration & Data Structures
# ==========================================

@dataclass
class SearchConfig:
    """
    Configuration for ProCache Constraint-Aware Caching Pattern Search.

    Attributes:
        T (int): Total number of denoising steps.
        B (int): The budget constraint for total activation steps (Eq. 2).
        K (int): The number of candidate patterns to sample.
        v_min (int): The minimum reuse interval constraint (Eq. 4).
        v_max (int): The maximum reuse interval constraint (Eq. 4).
        max_attempts (int): Safety limit for the rejection sampling loop.
    """
    T: int = 50
    B: int = 13
    K: int = 5
    v_min: int = 1
    v_max: int = 4
    max_attempts: int = 10 ** 6


class StepType(IntEnum):
    """
    Defines the operation type for a timestep t, corresponding to the cases
    in Algorithm 1.
    """
    CACHE = 0  # Case 3: Reuse cache
    FULL_COMPUTE = 1  # Case 1: Full computation (s_t = 1)
    SELECTIVE_COMPUTE = 2  # Case 2: Selective computation (injected into zeros)


# ==========================================
#  Part 1: Constraint-Aware Pattern Search
#  (Section 3.2)
# ==========================================

class ProCachePatternSearch:
    """
    Implements the Constraint-Aware Caching Pattern Search logic described
    in Section 3.2 of the ProCache paper.
    """

    def __init__(self, config: SearchConfig):
        self.cfg = config

    def _to_binary_sequence(self, intervals: List[int]) -> List[int]:
        """
        Converts the list of interval lengths into the binary caching pattern s.

        Args:
            intervals: A list where each element represents the distance between
                       activations (reuse interval + 1).

        Returns:
            s: A binary sequence s = [s_1, ..., s_T] where s_t=1 denotes
               computation and s_t=0 denotes reuse.
        """
        s = []
        for length in intervals:
            if length < 1:
                raise ValueError("Interval length must be >= 1.")
            # Create a segment starting with 1 (computation) followed by 0s (cache reuse)
            segment = [1] + [0] * (length - 1)
            s.extend(segment)

        # Validation to ensure s matches total timesteps T
        if len(s) != self.cfg.T:
            raise ValueError(f"Generated sequence length {len(s)} does not match T={self.cfg.T}")

        return s

    def search(self) -> List[List[int]]:
        """
        Performs the constrained sampling to find valid caching patterns.

        Corresponds to the search for patterns in the constrained space C.
        This implementation implicitly handles the Monotonic Constraint (Eq. 3)
        by sorting intervals in descending order.

        Returns:
            A list of K binary patterns, where each pattern is a list of integers.
        """
        # The segment length includes the computation step itself.
        # Therefore, segment_length = v_i + 1.
        min_segment = self.cfg.v_min + 1
        max_segment = self.cfg.v_max + 1 if self.cfg.v_max is not None else None

        # Pre-validation of constraints
        min_total_length = min_segment * self.cfg.B
        if min_total_length > self.cfg.T:
            print(f"Constraints unsatisfiable: Min total length {min_total_length} > T {self.cfg.T}")
            return []

        if max_segment:
            max_total_length = max_segment * self.cfg.B
            if self.cfg.T > max_total_length:
                # Note: In strict partitioning, sum must be exact.
                return []

        unique_candidates: Set[Tuple[int, ...]] = set()
        attempts = 0

        # Calculate the "free" pool of steps available to distribute
        remaining_steps = self.cfg.T - (min_segment * self.cfg.B)

        while len(unique_candidates) < self.cfg.K and attempts < self.cfg.max_attempts:
            attempts += 1

            # Generate a random partition of the remaining steps into B segments
            if remaining_steps == 0:
                random_increments = [0] * self.cfg.B
            else:
                # "Stick-breaking" method to generate random partition
                # Generate B-1 cut points in the range [0, remaining_steps]
                cut_points = sorted([random.randint(0, remaining_steps) for _ in range(self.cfg.B - 1)])
                # Add bounds to create B segments
                bounded_cuts = [0] + cut_points + [remaining_steps]
                random_increments = [bounded_cuts[i + 1] - bounded_cuts[i] for i in range(self.cfg.B)]

            # Construct the full intervals
            candidate_intervals = [min_segment + inc for inc in random_increments]

            # Apply Bounded Constraint: v_min <= v_i <= v_max
            # Since segment = v + 1, we check if segment > max_segment
            if max_segment is not None:
                if any(seg > max_segment for seg in candidate_intervals):
                    continue  # Discard invalid pattern from search space Omega

            # Apply Monotonic Constraint: v_{i+1} <= v_i (Eq. 3)
            # Sorting descending ensures longer reuse intervals appear early (stable stages)
            # and shorter intervals appear later (rapid changing stages).
            candidate_intervals.sort(reverse=True)

            unique_candidates.add(tuple(candidate_intervals))

        # Convert valid integer partitions to binary sequences s
        return [self._to_binary_sequence(list(intervals)) for intervals in list(unique_candidates)]


# ==========================================
#  Part 2: Selective Computation Injection
#  (Section 3.3)
# ==========================================

def inject_selective_computation(s: List[int]) -> List[int]:
    """
    Applies the Selective Computation strategy described in Section 3.3.

    It injects lightweight partial computations into maximal contiguous zero blocks
    of the caching pattern s. Specifically, for every zero block, it updates
    every second position starting from the second (Eq. 7).

    Logic:
        [0, 0]          -> [0, alpha]
        [0, 0, 0]       -> [0, alpha, 0]
        [0, 0, 0, 0]    -> [0, alpha, 0, alpha]

    Args:
        s: The binary caching pattern (0 for cache, 1 for compute).

    Returns:
        s_prime: A modified sequence where specific '0's are replaced with
                 StepType.SELECTIVE_COMPUTE (2).
    """
    s_prime = list(s)  # Create a copy to avoid modifying the input
    zero_run_length = 0

    for t, val in enumerate(s_prime):
        if val == StepType.FULL_COMPUTE:
            # If we hit a full computation step, the contiguous zero block ends.
            # Reset the counter.
            zero_run_length = 0
        else:
            # We are inside a zero block (cache reuse interval).
            zero_run_length += 1

            # According to Eq. 7:
            # We insert computation if the position index within the block is even.
            # 1st zero -> count=1 (Keep 0)
            # 2nd zero -> count=2 (Inject Selective)
            # 3rd zero -> count=3 (Keep 0)
            # 4th zero -> count=4 (Inject Selective)
            if zero_run_length % 2 == 0:
                s_prime[t] = int(StepType.SELECTIVE_COMPUTE)

    return s_prime


# ==========================================
#  Main Execution
# ==========================================

if __name__ == "__main__":
    # Example Configuration
    # B=11 activations out of T=50 steps.
    config = SearchConfig(
        T=50,  # Total timesteps
        B=11,  # Budget (Eq. 2)
        K=5,  # Number of candidates to generate
        v_min=2,  # Minimum reuse interval (Eq. 4)
        v_max=5  # Maximum reuse interval (Eq. 4)
    )

    # 1. Search for valid patterns (Section 3.2)
    searcher = ProCachePatternSearch(config)
    patterns = searcher.search()

    print(f"Generated {len(patterns)} valid patterns s from search space C:\n")

    for idx, s in enumerate(patterns):
        print(f"--- Pattern {idx + 1} ---")

        # Display the raw binary pattern s
        # 1 = Full Compute, 0 = Cache
        print(f"s_{idx+1}={str(s)}")

        # 2. Apply Selective Computation Injection (Section 3.3)
        # Returns s' where 2 = Selective Compute
        s_prime = inject_selective_computation(s)
        print(f"s_{idx+1}_injected={str(s_prime)}")
        print("")