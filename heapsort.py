"""
heapsort.py

"""

import random
import time
import sys

sys.setrecursionlimit(20000)

# Heapsort


def heapsort(arr: list) -> list:
    """
    Sort arr in ascending order using Heapsort.

    Time complexity : O(n log n)

    Returns a sorted copy; the original array is not modified.
    """
    arr = arr[:]    
    n = len(arr)

    # Phase 1: Build max-heap.
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, n, i)

    # Phase 2: Extract elements one by one.
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down(arr, end, 0)

    return arr


def _sift_down(arr: list, heap_size: int, root: int) -> None:
 
    while True:
        largest = root
        left    = 2 * root + 1
        right   = 2 * root + 2

        if left  < heap_size and arr[left]  > arr[largest]:
            largest = left
        if right < heap_size and arr[right] > arr[largest]:
            largest = right

        if largest == root:
            break                       # heap property satisfied

        arr[root], arr[largest] = arr[largest], arr[root]
        root = largest                  # continue sifting down


# Comparison algorithms

def merge_sort(arr: list) -> list:
    """Standard top-down Merge Sort. O(n log n) time"""
    if len(arr) <= 1:
        return arr[:]
    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list, right: list) -> list:
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quicksort(arr: list) -> list:
    """Randomized Quicksort (iterative to avoid recursion limit)."""
    arr = arr[:]
    stack = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo < hi:
            p = _qs_partition(arr, lo, hi)
            stack.append((lo, p - 1))
            stack.append((p + 1, hi))
    return arr


def _qs_partition(arr: list, lo: int, hi: int) -> int:
    pivot_idx = random.randint(lo, hi)
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


# Input generators

def make_random(n):   return [random.randint(0, 10 * n) for _ in range(n)]
def make_sorted(n):   return list(range(n))
def make_reverse(n):  return list(range(n, 0, -1))
def make_repeated(n): return [random.randint(0, 9) for _ in range(n)]

DISTRIBUTIONS = {
    "Random":          make_random,
    "Sorted":          make_sorted,
    "Reverse-sorted":  make_reverse,
    "Repeated values": make_repeated,
}

ALGORITHMS = {
    "Heapsort":   heapsort,
    "Quicksort":  quicksort,
    "Merge Sort": merge_sort,
}

SIZES  = [500, 1000, 2000, 4000]
TRIALS = 3

# Benchmark

def time_sort(fn, arr: list) -> float:
    start = time.perf_counter()
    fn(arr[:])
    return time.perf_counter() - start


def run_benchmark() -> dict:
    """Return results[dist][n][algo] = avg_seconds."""
    results = {}
    for dist_name, generator in DISTRIBUTIONS.items():
        results[dist_name] = {}
        for n in SIZES:
            results[dist_name][n] = {name: 0.0 for name in ALGORITHMS}
            for _ in range(TRIALS):
                arr = generator(n)
                for name, fn in ALGORITHMS.items():
                    results[dist_name][n][name] += time_sort(fn, arr)
            for name in ALGORITHMS:
                results[dist_name][n][name] /= TRIALS
    return results


def print_results(results: dict) -> None:
    col = 12
    names = list(ALGORITHMS.keys())
    print("\n" + "=" * 70)
    print(f"  BENCHMARK RESULTS  (average of {TRIALS} trials)")
    print("  Note: timings are machine-specific.")
    print("=" * 70)
    for dist, size_data in results.items():
        print(f"\n  Distribution: {dist}")
        header = f"  {'n':>5}  " + "  ".join(f"{n:>{col}}" for n in names)
        print(header)
        print("  " + "-" * (len(header) - 2))
        for n, timings in sorted(size_data.items()):
            row = f"  {n:>5}  "
            row += "  ".join(f"{timings[name]*1000:>{col}.3f} ms" for name in names)
            print(row)
    print()


# Correctness smoke-test

def _smoke_test() -> None:
    cases = [
        [],
        [1],
        [3, 1, 2],
        [5, 5, 5, 5],
        list(range(10)),
        list(range(9, -1, -1)),
        [random.randint(-100, 100) for _ in range(50)],
    ]
    for arr in cases:
        expected = sorted(arr)
        assert heapsort(arr)    == expected, f"Heapsort failed on {arr}"
        assert quicksort(arr)   == expected, f"Quicksort failed on {arr}"
        assert merge_sort(arr)  == expected, f"Merge Sort failed on {arr}"
    print("  Smoke tests passed for all three algorithms.\n")


# Entry point

if __name__ == "__main__":
    print("\nRunning correctness smoke tests...")
    _smoke_test()
    print("Running benchmark (this may take a few seconds)...")
    results = run_benchmark()
    print_results(results)
