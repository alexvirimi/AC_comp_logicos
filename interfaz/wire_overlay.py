from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt6.QtCore import Qt, QPoint, QPointF


GREEN = QColor("#22c55e")
RED = QColor("#ef4444")


class WireOverlay(QWidget):
    """Superposicion para dibujar cables entre compuertas."""

    def __init__(self, parent, circuit, inputs_column, level_columns, scroll_area):
        super().__init__(parent)

        self.circuit = circuit
        self.inputs_column = inputs_column
        self.level_columns = level_columns
        self.scroll_area = scroll_area

        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self.scroll_area.horizontalScrollBar().valueChanged.connect(self.update)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.update)

    # =========================
    # MAPEO GLOBAL PRECISO
    # =========================

    def _map_to_overlay(self, widget, local_point):
        """Convierte un punto local de 'widget' a coordenadas del overlay."""
        global_pos = widget.mapToGlobal(local_point)
        overlay_pos = self.mapFromGlobal(global_pos)
        return QPointF(overlay_pos)

    # =========================
    # PUNTOS DE CONEXIÓN
    # =========================

    def _input_output_point(self, container):
        """Punto de salida de una entrada (lado derecho, centro)."""
        rect = container.rect()
        point = QPoint(rect.right(), rect.center().y())
        return self._map_to_overlay(container, point)

    def _gate_input_point(self, container, input_index):
        """Punto de entrada de una compuerta (lado izquierdo, 35% o 65% alto)."""
        rect = container.rect()
        x = rect.left()
        if input_index == 0:
            y = rect.top() + rect.height() * 0.35
        else:
            y = rect.top() + rect.height() * 0.65
        return self._map_to_overlay(container, QPoint(int(x), int(y)))

    def _gate_output_point(self, container):
        """Punto de salida de una compuerta (lado derecho, centro)."""
        rect = container.rect()
        point = QPoint(rect.right(), rect.center().y())
        return self._map_to_overlay(container, point)

    # =========================
    # DIBUJO CURVA PROFESIONAL
    # =========================

    def _draw_curve(self, painter, start, end, color):
        """Dibuja una curva Bézier cúbica entre dos puntos."""
        path = QPainterPath()
        path.moveTo(start)

        dx = (end.x() - start.x()) * 0.5
        ctrl1 = QPointF(start.x() + dx, start.y())
        ctrl2 = QPointF(end.x() - dx, end.y())

        path.cubicTo(ctrl1, ctrl2, end)

        painter.setPen(QPen(color, 2))
        painter.drawPath(path)

    # =========================
    # RENDER
    # =========================

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        results = self.circuit.results

        if not results:
            return

        # ====================================
        # INPUTS → NIVEL 0
        # ====================================
        if self.level_columns:
            first_level = self.level_columns[0]

            for i, (input_container, _) in enumerate(self.inputs_column.input_buttons):
                start_point = self._input_output_point(input_container)

                gate_index = i // 2
                input_side = i % 2

                if gate_index < len(first_level.gate_widgets):
                    gate_container = first_level.gate_widgets[gate_index][0].parent()
                    end_point = self._gate_input_point(gate_container, input_side)

                    value = self.circuit.inputs[i]
                    color = GREEN if value else RED

                    self._draw_curve(painter, start_point, end_point, color)

        # ====================================
        # ENTRE NIVELES
        # ====================================
        for level in range(1, len(self.level_columns)):
            prev_level = self.level_columns[level - 1]
            current_level = self.level_columns[level]

            for i, (svg, _) in enumerate(current_level.gate_widgets):
                input_a = i * 2
                input_b = i * 2 + 1

                if input_b >= len(prev_level.gate_widgets):
                    continue

                prev_a_container = prev_level.gate_widgets[input_a][0].parent()
                prev_b_container = prev_level.gate_widgets[input_b][0].parent()
                current_container = svg.parent()

                start_a = self._gate_output_point(prev_a_container)
                start_b = self._gate_output_point(prev_b_container)

                end_a = self._gate_input_point(current_container, 0)
                end_b = self._gate_input_point(current_container, 1)

                val_a = results[level - 1][input_a]
                val_b = results[level - 1][input_b]

                self._draw_curve(painter, start_a, end_a, GREEN if val_a else RED)
                self._draw_curve(painter, start_b, end_b, GREEN if val_b else RED)