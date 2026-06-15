# HeapSort
Assignment 4: Heap Data Structures - Implementation, Analysis, and Applications

This repository covers two things: a clean Heapsort implementation benchmarked against Quicksort and Merge Sort, and a max-heap backed priority queue with a task scheduler simulation.

Repository Structure

.
├── heapsort.py        # Heapsort + Quicksort + Merge Sort with benchmarking
├── priority_queue.py  # Priority queue, Task class, and scheduler simulation
├── report.docx        # Full write-up: analysis, benchmarks, and design discussion
└── README.md          # This file

Requirements

Python 3.8 or newer. No third-party packages - standard library only (random, time, sys, dataclasses).

How to Run

Heapsort + Benchmark

bashpython heapsort.py

Runs correctness smoke tests first (empty arrays, single elements, all-equal, sorted, reverse-sorted, random), then benchmarks all three sorting algorithms across four distributions (random, sorted, reverse-sorted, repeated values) at sizes 500, 1000, 2000, and 4000. Takes a few seconds to complete.

Priority Queue + Scheduler

bashpython priority_queue.py

Runs smoke tests covering insert, extract_max, increase_key, decrease_key, duplicate ID guards, and a 200-task stress test verifying descending extraction order. Then runs the scheduler simulation showing all operations in a realistic context.

Key Findings

Heapsort guarantees O(n log n) in all cases with O(1) auxiliary space. It holds up well on random and repeated-value inputs but can't exploit existing order the way Merge Sort can on pre-sorted data.

The standout result is on repeated values: with only 10 distinct values across 4000 elements, Quicksort degraded to ~52 ms while Heapsort finished in ~5.5 ms, nearly 10× faster. This is because repeated values cause heavily imbalanced partitions in Lomuto Quicksort, pushing it toward O(n²), while Heapsort's complexity is completely unaffected by value distribution.

Priority queue operations (insert, extract_max, increase_key, decrease_key) all run in O(log n) time. The key implementation decision was maintaining a position map alongside the heap so that increase_key and decrease_key can locate any task in O(1) rather than scanning the entire array. Without it those two operations would be O(n) overall.

The scheduler simulation shows what happens when pure priority scheduling ignores deadlines, higher-priority tasks execute first even when lower-priority ones have tighter deadlines. A real-world scheduler would likely combine priority with Earliest Deadline First or similar deadline-aware logic.

Notes

Timings will differ by machine. The relative patterns, which algorithm is faster and by how much, should be consistent regardless of hardware.
