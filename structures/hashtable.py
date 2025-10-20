from typing import Any, List, Optional, Tuple


class HashTable:
    """
    Implementación sencilla de hash table con chaining.
    Llaves: strings (códigos de producto). Valores: objetos.
    Operaciones: insert, get, update, remove, contains.
    """

    def __init__(self, capacity: int = 1024) -> None:
        self.capacity = max(8, capacity)
        self.buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(self.capacity)]
        self.size = 0

    def _hash(self, key: str) -> int:
        """Hash simple usando sum of ords + modulo. Podés reemplazar por otra."""
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) & 0xFFFFFFFF
        return h % self.capacity

    def insert(self, key: str, value: Any) -> None:
        """Inserta o reemplaza el valor asociado a key."""
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

    def get(self, key: str) -> Optional[Any]:
        """Retorna el valor o None si no existe."""
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return None

    def contains(self, key: str) -> bool:
        return self.get(key) is not None

    def remove(self, key: str) -> bool:
        """Elimina y retorna True si existía, sino False."""
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def keys(self) -> List[str]:
        ks = []
        for bucket in self.buckets:
            for k, _ in bucket:
                ks.append(k)
        return ks

    def values(self) -> List[Any]:
        vs = []
        for bucket in self.buckets:
            for _, v in bucket:
                vs.append(v)
        return vs

    def items(self) -> List[Tuple[str, Any]]:
        it = []
        for bucket in self.buckets:
            for kv in bucket:
                it.append(kv)
        return it

    def __len__(self) -> int:
        return self.size
