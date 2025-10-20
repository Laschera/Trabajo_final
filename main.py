"""
Script de demostración para ejecutar el "motor" de la tienda.
Guardá los módulos en la misma carpeta (o en un paquete) y ejecutá:
    python main.py
"""

from models.product import Product
from tienda import Tienda, Order


def demo():
    tienda = Tienda()

    # --- Agregar productos ---
    p1 = Product(code="COMIC-001", name="Batman #1", price=1200.0, stock=10,
                 description="Primer número - Edición clásica")
    p2 = Product(code="COMIC-002", name="Superman #1", price=1100.0, stock=5)
    p3 = Product(code="FIG-001", name="Figura Batman", price=4500.0, stock=2)

    tienda.add_product(p1)
    tienda.add_product(p2)
    tienda.add_product(p3)

    print("Productos iniciales:", tienda.list_all_products())

    # --- Actualizar producto ---
    tienda.update_product("COMIC-002", price=1150.0, stock=7)
    print("COMIC-002 actualizado:", tienda.get_product("COMIC-002"))

    # --- Categorías ---
    tienda.add_category_path(["Cómics", "DC Comics", "Batman"])
    tienda.add_category_path(["Cómics", "DC Comics", "Superman"])
    tienda.add_category_path(["Merch", "Figuras"])

    tienda.add_product_to_category(["Cómics", "DC Comics", "Batman"], "COMIC-001")
    tienda.add_product_to_category(["Cómics", "DC Comics", "Superman"], "COMIC-002")
    tienda.add_product_to_category(["Merch", "Figuras"], "FIG-001")

    # Mostrar productos bajo "DC Comics" (incluye subcategorías)
    productos_dc = tienda.get_products_under_category(["Cómics", "DC Comics"])
    print("Productos bajo 'Cómics > DC Comics':", productos_dc)

    # --- Pedidos (Queue FIFO) ---
    o1 = Order(order_id="ORD-001", customer_name="Lucas", items=["COMIC-001", "FIG-001"])
    o2 = Order(order_id="ORD-002", customer_name="Ana", items=["COMIC-002"])

    tienda.enqueue_order(o1)
    tienda.enqueue_order(o2)

    print("Siguiente pedido (peek):", tienda.peek_next_order())
    procesado = tienda.process_next_order()
    print("Pedido procesado:", procesado)
    print("Stock tras procesar:", tienda.get_product("COMIC-001").stock,
          tienda.get_product("FIG-001").stock)

    # --- Historial de vistos (stack por cliente) ---
    cliente = "cliente_123"
    tienda.view_product(cliente, "COMIC-001")
    tienda.view_product(cliente, "COMIC-002")
    tienda.view_product(cliente, "FIG-001")
    tienda.view_product(cliente, "COMIC-001")  # si vuelve a ver, se mueve al tope

    print("Vistos recientemente por", cliente, ":", tienda.get_recently_viewed(cliente))

    # --- Borrar un producto ---
    tienda.remove_product("FIG-001")
    print("Productos tras eliminar FIG-001:", tienda.list_all_products())
    # comprobar que ya no está en categorías:
    print("Productos en 'Merch > Figuras':",
          tienda.get_products_under_category(["Merch", "Figuras"]))

    print("Demo finalizada.")


if __name__ == "__main__":
    demo()
