from typing import Dict, List, Optional
from models.product import Product
from structures.hashtable import HashTable
from structures.queue import Queue
from structures.stack import RecentStack
from structures.tree import CategoryTree
from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    customer_name: str
    items: List[str]  # lista de códigos de producto
    status: str = "pending"


class Tienda:
    """
    Clase principal que integra las estructuras:
      - products: HashTable (código -> Product)
      - orders: Queue[Order]
      - recent_views_by_customer: Dict[customer_id, RecentStack]
      - categories: CategoryTree
    """

    def __init__(self) -> None:
        self.products = HashTable()
        self.orders = Queue[Order]()
        self.recent_views_by_customer: Dict[str, RecentStack[str]] = {}
        self.categories = CategoryTree()

    # ---------------------------
    # Gestión de productos
    # ---------------------------
    def add_product(self, product: Product) -> None:
        """Agrega un producto. Reemplaza si ya existe el código."""
        self.products.insert(product.code, product)

    def update_product(self, code: str, *, name: Optional[str] = None,
                       price: Optional[float] = None, stock: Optional[int] = None,
                       description: Optional[str] = None) -> bool:
        """Actualiza campos de un producto. Retorna True si existe y se actualizó."""
        p = self.products.get(code)
        if p is None:
            return False
        if name is not None:
            p.name = name
        if price is not None:
            p.price = price
        if stock is not None:
            p.stock = stock
        if description is not None:
            p.description = description
        self.products.insert(code, p)  # reemplaza
        return True

    def get_product(self, code: str) -> Optional[Product]:
        return self.products.get(code)

    def remove_product(self, code: str) -> bool:
        # además de remover del hash, remover de categorías si corresponde.
        removed = self.products.remove(code)
        # eliminar en todas las categorías (recorrido simple)
        # (esto es O(n_categories) pero suficiente para práctica)
        self._remove_product_from_all_categories(code)
        return removed

    def _remove_product_from_all_categories(self, code: str) -> None:
        def _rec(node):
            node.remove_product(code)
            for child in node.children.values():
                _rec(child)
        _rec(self.categories.root)

    # ---------------------------
    # Procesamiento de pedidos
    # ---------------------------
    def enqueue_order(self, order: Order) -> None:
        self.orders.enqueue(order)

    def process_next_order(self) -> Optional[Order]:
        """Procesa (dequeue) el siguiente pedido en orden FIFO."""
        order = self.orders.dequeue()
        if order:
            order.status = "processed"
            # lógica adicional podría restar stock, enviar notificación, etc.
            for code in order.items:
                product = self.get_product(code)
                if product and product.stock > 0:
                    product.stock -= 1
                    # si stock negativo no lo permitimos (en este ejemplo no hacemos backorder)
                    if product.stock < 0:
                        product.stock = 0
            # actualizar productos en la tabla:
            for code in order.items:
                p = self.get_product(code)
                if p:
                    self.products.insert(code, p)
        return order

    def peek_next_order(self) -> Optional[Order]:
        return self.orders.peek()

    # ---------------------------
    # Historial de productos vistos
    # ---------------------------
    def _ensure_recent_stack(self, customer_id: str) -> RecentStack[str]:
        if customer_id not in self.recent_views_by_customer:
            self.recent_views_by_customer[customer_id] = RecentStack(capacity=5)
        return self.recent_views_by_customer[customer_id]

    def view_product(self, customer_id: str, product_code: str) -> Optional[Product]:
        """
        Registra que `customer_id` vio `product_code` (push en stack) y retorna el producto.
        """
        product = self.get_product(product_code)
        if product is None:
            return None
        stack = self._ensure_recent_stack(customer_id)
        stack.push(product_code)
        return product

    def get_recently_viewed(self, customer_id: str) -> List[str]:
        stack = self.recent_views_by_customer.get(customer_id)
        if stack is None:
            return []
        return stack.get_all()

    # ---------------------------
    # Categorías
    # ---------------------------
    def add_category_path(self, path: List[str]) -> None:
        self.categories.add_path(path)

    def add_product_to_category(self, path: List[str], product_code: str) -> bool:
        return self.categories.add_product_to_path(path, product_code)

    def get_products_under_category(self, path: List[str]) -> Optional[List[Product]]:
        codes = self.categories.get_products_under_path(path)
        if codes is None:
            return None
        products = []
        for code in codes:
            p = self.get_product(code)
            if p:
                products.append(p)
        return products

    # ---------------------------
    # Utilidades
    # ---------------------------
    def list_all_products(self) -> List[Product]:
        return self.products.values()

    def __repr__(self) -> str:
        return f"Tienda(products={len(self.products)}, orders={len(self.orders)})"
