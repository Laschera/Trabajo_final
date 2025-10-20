from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """
    Representa un producto de la tienda.
    `code` debe ser único (ej: "COMIC-001").
    """
    code: str
    name: str
    price: float
    stock: int
    description: Optional[str] = None

    def to_dict(self) -> dict:
        """Retorna una representación dict del producto."""
        return {
            "code": self.code,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "description": self.description,
        }

    def __repr__(self) -> str:
        return (
            f"Product(code={self.code!r}, name={self.name!r}, price={self.price}, "
            f"stock={self.stock})"
        )
