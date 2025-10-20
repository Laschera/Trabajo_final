from typing import Dict, List, Optional, Set


class CategoryNode:
    """
    Nodo de categoría en un árbol. Cada nodo puede contener productos (códigos)
    y subcategorías.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.children: Dict[str, "CategoryNode"] = {}
        self.products: Set[str] = set()

    def add_child(self, name: str) -> "CategoryNode":
        if name not in self.children:
            self.children[name] = CategoryNode(name)
        return self.children[name]

    def get_child(self, name: str) -> Optional["CategoryNode"]:
        return self.children.get(name)

    def add_product(self, product_code: str) -> None:
        self.products.add(product_code)

    def remove_product(self, product_code: str) -> None:
        self.products.discard(product_code)

    def gather_products_recursive(self) -> Set[str]:
        """
        Recolecta todos los productos en este nodo y en todos sus descendientes.
        """
        collected = set(self.products)
        for child in self.children.values():
            collected.update(child.gather_products_recursive())
        return collected

    def __repr__(self) -> str:
        return f"CategoryNode({self.name!r})"


class CategoryTree:
    """
    Árbol de categorías con raíz 'root'.
    Permite:
      - add_path(['Cómics', 'DC Comics', 'Batman'])
      - add_product_to_path(path, product_code)
      - get_products_under_path(path)
    """

    def __init__(self) -> None:
        self.root = CategoryNode("root")

    def add_path(self, path: List[str]) -> None:
        node = self.root
        for part in path:
            node = node.add_child(part)

    def _find_node(self, path: List[str]) -> Optional[CategoryNode]:
        node = self.root
        for part in path:
            node = node.get_child(part)
            if node is None:
                return None
        return node

    def add_product_to_path(self, path: List[str], product_code: str) -> bool:
        node = self._find_node(path)
        if node is None:
            return False
        node.add_product(product_code)
        return True

    def get_products_under_path(self, path: List[str]) -> Optional[Set[str]]:
        node = self._find_node(path)
        if node is None:
            return None
        return node.gather_products_recursive()

    def __repr__(self) -> str:
        return "CategoryTree(root)"
