from collections import deque
from typing import Deque, Generic, List, TypeVar

T = TypeVar("T")


class RecentStack(Generic[T]):
    """
    Historial LIFO de tamaño fijo (ej: últimos 5 productos vistos).
    Se mantiene en orden: índice 0 = más reciente.
    """

    def __init__(self, capacity: int = 5) -> None:
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self.capacity = capacity
        self._d: Deque[T] = deque(maxlen=capacity)

    def push(self, item: T) -> None:
        """
        Añade item al tope (más reciente).
        Si ya existe en el historial, nos quedamos con las duplicaciones (o podríamos eliminar la anterior).
        """
        # Opcional: evitar duplicados moviendo el existente al tope:
        try:
            self._d.remove(item)
        except ValueError:
            pass
        self._d.appendleft(item)

    def pop(self) -> T:
        return self._d.popleft()

    def get_all(self) -> List[T]:
        """Retorna lista desde más reciente hasta el más antiguo."""
        return list(self._d)

    def is_empty(self) -> bool:
        return len(self._d) == 0

    def __len__(self) -> int:
        return len(self._d)

    def __repr__(self) -> str:
        return f"RecentStack({list(self._d)})"
