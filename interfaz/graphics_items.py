from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt6.QtGui import QBrush, QPen, QColor, QFont
from PyQt6.QtCore import Qt


GREEN = QColor("#22c55e")
RED = QColor("#ef4444")
WHITE = QColor("#f1f5f9")


class InputNodeItem(QGraphicsEllipseItem):
    def __init__(self, index, x, y, radius=15):
        super().__init__(-radius, -radius, radius * 2, radius * 2)
        self.index = index
        self.value = 0
        self.setPos(x, y)
        self.setBrush(QBrush(RED))
        self.setPen(QPen(Qt.GlobalColor.white, 2))
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable, True)

        self.text = QGraphicsTextItem("0", self)
        self.text.setDefaultTextColor(WHITE)
        font = QFont()
        font.setBold(True)
        self.text.setFont(font)
        self.text.setPos(-5, -10)

    def toggle(self):
        self.value = 0 if self.value else 1
        self.setBrush(QBrush(GREEN if self.value else RED))
        self.text.setPlainText(str(self.value))


class GateItem(QGraphicsEllipseItem):
    def __init__(self, x, y, gate_type):
        super().__init__(-30, -30, 60, 60)
        self.setPos(x, y)
        self.gate_type = gate_type
        self.output_value = 0

        self.setBrush(QBrush(QColor("#1e293b")))
        self.setPen(QPen(Qt.GlobalColor.white, 2))

        self.text = QGraphicsTextItem(gate_type, self)
        self.text.setDefaultTextColor(WHITE)
        font = QFont()
        font.setBold(True)
        self.text.setFont(font)
        self.text.setPos(-20, -10)

    def set_output(self, value):
        self.output_value = value
        color = GREEN if value else RED
        self.setPen(QPen(color, 3))


class WireItem(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.setPen(QPen(RED, 2))

    def set_signal(self, value):
        color = GREEN if value else RED
        self.setPen(QPen(color, 3))