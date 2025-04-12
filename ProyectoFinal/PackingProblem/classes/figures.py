
# Clase base para figuras geométricas
class Figure:
    def __init__(self, x, y):
        self.x = x  # Coordenada x
        self.y = y  # Coordenada y

    def is_overlapping(self, other):
        """ Método que debe ser implementado por subclases."""
        raise NotImplementedError("Debe implementarse en subclases")

    def data(self):
        """ Devuelve los datos de la figura."""
        return {
            'x': self.x,
            'y': self.y
        }


# Clase para rectángulos
class Rectangle(Figure):
    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def is_overlapping(self, other):
        """Revisa si este rectángulo se solapa con otra figura (bounding box)."""
        if isinstance(other, Rectangle):
            if self.x is None or other.x is None or self.y is None or other.y is None:
                return False

            return not (
                    self.x + self.width <= other.x or
                    self.x >= other.x + other.width or
                    self.y + self.height <= other.y or
                    self.y >= other.y + other.height
            )
        elif isinstance(other, Triangle):
            # Revisar solapamiento con triángulo usando vértices. Por simplicidad chequeamos cajas delimitantes.
            return other.is_overlapping(self)

    def data(self):
        """ Devuelve los datos del rectángulo."""
        return {
            'type': 'rectangle',
            'x': self.x,
            'y': self.y,
            'width': self.width,
            'height': self.height
        }

    def __repr__(self):
        return f"Rectangle(x={self.x}, y={self.y}, width={self.width}, height={self.height})"


# Clase para triángulos
def get_min_max_values(vertices):
    min_x = min(v[0] for v in vertices)
    max_x = max(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)
    return min_x, max_x, min_y, max_y


class Triangle(Figure):
    def __init__(self, x, y, base, height):
        super().__init__(x, y)
        self.base = base
        self.height = height
        # Calcular vértices a partir de la base y altura
        self.vertices = [
            (x, y),  # Vértice inferior izquierdo
            (x + base, y),  # Vértice inferior derecho
            (x, y + height)  # Vértice superior izquierdo
        ]

    def is_overlapping(self, other):
        """ Revisa si este triángulo se solapa con otra figura."""
        if isinstance(other, Rectangle):
            # Bounding box del triángulo
            if self.x is None or other.x is None or self.y is None or other.y is None:
                return False
            # Bounding box del triángulo
            min_x, max_x, min_y, max_y = get_min_max_values(self.vertices)

            return not (
                    max_x <= other.x or
                    min_x >= other.x + other.width or
                    max_y <= other.y or
                    min_y >= other.y + other.height
            )
        elif isinstance(other, Triangle):
            if self.x is None or other.x is None or self.y is None or other.y is None:
                return False
            # Similar al anterior: para simplicidad utilizamos bounding boxes
            other_min_x, other_max_x, other_min_y, other_max_y = get_min_max_values(other.vertices)
            # Bounding box del triángulo
            self_min_x, self_max_x, self_min_y, self_max_y = get_min_max_values(self.vertices)

            return not (
                    self_max_x <= other_min_x or
                    self_min_x >= other_max_x or
                    self_max_y <= other_min_y or
                    self_min_y >= other_max_y
            )

    def data(self):
        """ Devuelve los datos del triángulo."""
        return {
            'type': 'triangle',
            'x': self.x,
            'y': self.y,
            'base': self.base,
            'height': self.height,
            'vertices': self.vertices
        }

    def __repr__(self):
        return f"Triangle(vertices={self.vertices})"