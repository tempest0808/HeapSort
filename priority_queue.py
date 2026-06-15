"""
priority_queue.py
-----------------
Max-heap based Priority Queue with a Task class and a simple
deadline-aware scheduler simulation.

"""

from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Optional

# Task

@dataclass
class Task:
    """
    Represents a schedulable unit of work.

    """
    task_id:      str
    priority:     int
    arrival_time: float = field(default_factory=time.time)
    deadline:     Optional[float] = None
    description:  str = ""

    def __repr__(self) -> str:
        dl = f", deadline={self.deadline}" if self.deadline is not None else ""
        return (f"Task(id={self.task_id!r}, priority={self.priority}"
                f", arrival={self.arrival_time}{dl})")

# Max-Heap Priority Queue

class PriorityQueue:
    """
    Max-heap priority queue backed by a Python list.

    """

    def __init__(self) -> None:
        self._heap: list[Task] = []
        self._pos_map: dict[str, int] = {}   # task_id → heap index

    # Core public API

    def insert(self, task: Task) -> None:

        if task.task_id in self._pos_map:
            raise ValueError(f"Task '{task.task_id}' already exists. "
                             "Use increase_key / decrease_key to modify priority.")
        self._heap.append(task)
        idx = len(self._heap) - 1
        self._pos_map[task.task_id] = idx
        self._sift_up(idx)

    def extract_max(self) -> Task:

        if self.is_empty():
            raise IndexError("extract_max called on an empty priority queue.")
        self._swap(0, len(self._heap) - 1)
        max_task = self._heap.pop()
        del self._pos_map[max_task.task_id]
        if self._heap:
            self._sift_down(0)
        return max_task

    def increase_key(self, task_id: str, new_priority: int) -> None:

        idx = self._get_idx(task_id)
        if new_priority <= self._heap[idx].priority:
            raise ValueError(
                f"new_priority ({new_priority}) must be greater than current "
                f"priority ({self._heap[idx].priority}) for increase_key.")
        self._heap[idx].priority = new_priority
        self._sift_up(idx)

    def decrease_key(self, task_id: str, new_priority: int) -> None:

        idx = self._get_idx(task_id)
        if new_priority >= self._heap[idx].priority:
            raise ValueError(
                f"new_priority ({new_priority}) must be less than current "
                f"priority ({self._heap[idx].priority}) for decrease_key.")
        self._heap[idx].priority = new_priority
        self._sift_down(idx)

    def peek(self) -> Task:
        """Return (without removing) the highest-priority task.  O(1)."""
        if self.is_empty():
            raise IndexError("peek called on an empty priority queue.")
        return self._heap[0]

    def is_empty(self) -> bool:
        """Return True if the queue contains no tasks.  O(1)."""
        return len(self._heap) == 0

    def __len__(self) -> int:
        return len(self._heap)

    # Internal helpers

    def _swap(self, i: int, j: int) -> None:
        """Swap two elements and keep pos_map consistent."""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._pos_map[self._heap[i].task_id] = i
        self._pos_map[self._heap[j].task_id] = j

    def _sift_up(self, idx: int) -> None:
        """Move the element at idx upward until heap property holds."""
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx].priority > self._heap[parent].priority:
                self._swap(idx, parent)
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        """Move the element at idx downward until heap property holds."""
        n = len(self._heap)
        while True:
            largest = idx
            left    = 2 * idx + 1
            right   = 2 * idx + 2
            if left  < n and self._heap[left].priority  > self._heap[largest].priority:
                largest = left
            if right < n and self._heap[right].priority > self._heap[largest].priority:
                largest = right
            if largest == idx:
                break
            self._swap(idx, largest)
            idx = largest

    def _get_idx(self, task_id: str) -> int:
        if task_id not in self._pos_map:
            raise KeyError(f"Task '{task_id}' not found in the priority queue.")
        return self._pos_map[task_id]


# Scheduler simulation

def run_scheduler_simulation() -> None:
    """
    Simulate a simple deadline-aware task scheduler.

    Tasks arrive with different priorities and deadlines.
    The scheduler always picks the highest-priority ready task next,
    demonstrating all four priority queue operations in a realistic context.
    """
    print("=" * 60)
    print("  Scheduler Simulation")
    print("=" * 60)

    pq = PriorityQueue()

    # --- Batch 1: initial task arrivals ---
    initial_tasks = [
        Task("T1", priority=3,  arrival_time=0, deadline=10, description="Low-priority batch job"),
        Task("T2", priority=8,  arrival_time=1, deadline=5,  description="High-priority user request"),
        Task("T3", priority=5,  arrival_time=2, deadline=8,  description="Medium-priority report"),
        Task("T4", priority=1,  arrival_time=3, deadline=20, description="Background cleanup"),
        Task("T5", priority=10, arrival_time=4, deadline=3,  description="Critical alert"),
    ]

    print("\n  [Tick 0-4] Inserting initial tasks:")
    for task in initial_tasks:
        pq.insert(task)
        print(f"    INSERT  {task.task_id}  priority={task.priority:>3}"
              f"  '{task.description}'")

    print(f"\n  Queue size: {len(pq)}  |  Next to run: {pq.peek().task_id} "
          f"(priority={pq.peek().priority})")

    # --- Priority update: T3 becomes urgent ---
    print("\n  [Tick 5] T3 escalated — deadline moved forward.")
    pq.increase_key("T3", new_priority=9)
    print(f"    INCREASE_KEY  T3 → priority=9")
    print(f"    Next to run: {pq.peek().task_id} (priority={pq.peek().priority})")

    # --- Priority demotion: T2 deprioritised ---
    print("\n  [Tick 6] T2 deprioritised — user request can wait.")
    pq.decrease_key("T2", new_priority=4)
    print(f"    DECREASE_KEY  T2 → priority=4")

    # --- Late arrival ---
    late = Task("T6", priority=7, arrival_time=6, deadline=9, description="Late urgent task")
    pq.insert(late)
    print(f"\n  [Tick 6] Late arrival: INSERT T6  priority=7")

    # --- Execution loop: drain the queue ---
    print("\n  [Tick 7+] Executing tasks in priority order:")
    tick = 7
    while not pq.is_empty():
        task = pq.extract_max()
        missed = (task.deadline is not None and tick > task.deadline)
        status = "  *** DEADLINE MISSED ***" if missed else ""
        print(f"    Tick {tick:>2}  EXECUTE  {task.task_id}"
              f"  priority={task.priority:>3}"
              f"  deadline={task.deadline}{status}")
        tick += 1

    print(f"\n  Queue empty: {pq.is_empty()}")
    print("=" * 60)


# Correctness smoke-test

def _smoke_test() -> None:
    pq = PriorityQueue()

    # Empty queue guards
    assert pq.is_empty()
    try:
        pq.extract_max()
        assert False, "Should have raised IndexError"
    except IndexError:
        pass

    # Insert and peek
    pq.insert(Task("A", priority=5))
    pq.insert(Task("B", priority=10))
    pq.insert(Task("C", priority=1))
    assert pq.peek().task_id == "B"
    assert len(pq) == 3

    # extract_max returns in priority order
    assert pq.extract_max().task_id == "B"
    assert pq.extract_max().task_id == "A"
    assert pq.extract_max().task_id == "C"
    assert pq.is_empty()

    # increase_key / decrease_key
    pq.insert(Task("X", priority=3))
    pq.insert(Task("Y", priority=7))
    pq.increase_key("X", 10)
    assert pq.peek().task_id == "X"
    pq.decrease_key("X", 1)
    assert pq.peek().task_id == "Y"

    # Duplicate task_id guard
    pq.insert(Task("Z", priority=5))
    try:
        pq.insert(Task("Z", priority=8))
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

    # Large random stress test
    import random
    pq2 = PriorityQueue()
    tasks = [Task(f"T{i}", priority=random.randint(1, 1000)) for i in range(200)]
    for t in tasks:
        pq2.insert(t)
    priorities = [pq2.extract_max().priority for _ in range(200)]
    assert priorities == sorted(priorities, reverse=True), "Not sorted in descending order!"

    print("  All smoke tests passed.\n")

# Entry point

if __name__ == "__main__":
    print("\nRunning smoke tests...")
    _smoke_test()
    run_scheduler_simulation()
