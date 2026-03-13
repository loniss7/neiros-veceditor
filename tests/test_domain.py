from vector_editor.domain.shapes import Circle, Oval, Point, Rectangle, Segment, Square


def test_point_summary():
    point = Point(id=1, x=1, y=2)

    assert point.shape_type == "Point"
    assert point.summary() == "x=1, y=2"


def test_segment_summary():
    segment = Segment(id=1, x1=0, y1=0, x2=3, y2=4)

    assert segment.shape_type == "Segment"
    assert segment.summary() == "start=(0, 0), end=(3, 4)"


def test_circle_summary():
    circle = Circle(id=1, center_x=1, center_y=1, radius=5)

    assert circle.shape_type == "Circle"
    assert circle.summary() == "center=(1, 1), radius=5"


def test_square_summary():
    square = Square(id=1, x=0, y=0, side=10)

    assert square.shape_type == "Square"
    assert square.summary() == "origin=(0, 0), side=10"


def test_oval_summary():
    oval = Oval(id=1, center_x=2, center_y=3, radius_x=4, radius_y=5)

    assert oval.shape_type == "Oval"
    assert oval.summary() == "center=(2, 3), rx=4, ry=5"


def test_rectangle_summary():
    rectangle = Rectangle(id=1, x=10, y=20, width=30, height=40)

    assert rectangle.shape_type == "Rectangle"
    assert rectangle.summary() == "origin=(10, 20), width=30, height=40"