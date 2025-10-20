from collections import deque
from typing import Deque, Generic, Optional, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    """Cola FIFO simple usando deque."""

    def __init__(self) -> None:
        self._q: Deque[T] = deque()

    def enqueue(self, item: T) -> None:
        self._q.append(item)

    def dequeue(self) -> Optional[T]:
        if not self.is_empty():
            return self._q.popleft()
        return None

    def peek(self) -> Optional[T]:
        return self._q[0] if not self.is_empty() else None

    def is_empty(self) -> bool:
        return len(self._q) == 0

    def __len__(self) -> int:
        return len(self._q)

    def __repr__(self) -> str:
        return f"Queue({list(self._q)})"
