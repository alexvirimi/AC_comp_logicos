import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog as simpledialog
from tree.builder import TreeBuilder
from gates.and_gate import AND
from gates.or_gate import OR
from gates.nand_gate import NAND
from gates.nor_gate import NOR
from gates.xor_gate import XOR
from gates.xnor_gate import XNOR
from gates.flipflop import FlipFlop


GATE_OPTIONS = ["AND", "OR", "NAND", "NOR", "XOR", "XNOR"]
GATE_CLASS_MAP = {
    "AND": AND,
    "OR": OR,
    "NAND": NAND,
    "NOR": NOR,
    "XOR": XOR,
    "XNOR": XNOR,
}


class CircuitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz de Compuertas Lógicas")

        # Top controls
        self.top_frame = ttk.Frame(root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

        ttk.Label(self.top_frame, text="Niveles:").pack(side=tk.LEFT)
        self.level_var = tk.IntVar(value=3)
        self.level_spin = ttk.Spinbox(self.top_frame, from_=1, to=6, width=4, textvariable=self.level_var)
        self.level_spin.pack(side=tk.LEFT, padx=4)

        self.levels_frame = ttk.Frame(root)
        self.levels_frame.pack(side=tk.TOP, fill=tk.X, padx=6)

        self.level_selectors = []
        self._build_level_selectors(3)

        ttk.Button(self.top_frame, text="Build & Render", command=self.build_and_render).pack(side=tk.LEFT, padx=8)

        # Main area: canvas + right controls
        main_pane = ttk.Panedwindow(root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main_pane, background="white", width=1000, height=700)
        main_pane.add(self.canvas, weight=3)

        right_frame = ttk.Frame(main_pane, width=260)
        main_pane.add(right_frame, weight=1)

        self.info_label = ttk.Label(right_frame, text="Selecciona un nodo para FlipFlop")
        self.info_label.pack(pady=8)

        self.attach_ff_btn = ttk.Button(right_frame, text="Adjuntar/Remover FlipFlop al nodo seleccionado", command=self.toggle_flipflop)
        self.attach_ff_btn.pack(padx=6, pady=4)

        ttk.Label(right_frame, text="FlipFlop Reset (R):").pack(anchor=tk.W, padx=6)
        self.ff_reset_var = tk.IntVar(value=0)
        ttk.Checkbutton(right_frame, text="R=1", variable=self.ff_reset_var, command=self.evaluate_and_update).pack(anchor=tk.W, padx=6)

        ttk.Button(right_frame, text="Evaluar", command=self.evaluate_and_update).pack(pady=8)

        # Internal state
        self.builder = None
        self.root_node = None
        self.node_canvas_map = {}  # Nodo -> dict of canvas ids
        self.selected_node = None

        # Bind change of levels spinbox
        self.level_var.trace_add('write', self.on_levels_change)

        # Ask initial levels and auto-build for a more intuitive start
        self.ask_initial_levels()

    def _build_level_selectors(self, n):
        # Clear
        for child in self.levels_frame.winfo_children():
            child.destroy()
        self.level_selectors = []
        for i in range(1, n + 1):
            frm = ttk.Frame(self.levels_frame)
            frm.pack(side=tk.LEFT, padx=4)
            ttk.Label(frm, text=f"Nivel {i}").pack()
            var = tk.StringVar(value=GATE_OPTIONS[0])
            om = ttk.OptionMenu(frm, var, GATE_OPTIONS[0], *GATE_OPTIONS)
            om.pack()
            self.level_selectors.append(var)

    def on_levels_change(self, *args):
        try:
            n = int(self.level_var.get())
        except Exception:
            return
        self._build_level_selectors(n)

    def build_and_render(self):
        num_levels = int(self.level_var.get())
        gate_types = []
        for var in self.level_selectors[:num_levels]:
            name = var.get()
            gate_types.append(GATE_CLASS_MAP[name])

        self.builder = TreeBuilder(num_levels=num_levels, gate_types=gate_types)
        self.root_node = self.builder.build()

        # Remove any previously selected node reference
        self.selected_node = None

        self.render_tree()
        self.evaluate_and_update()

    def render_tree(self):
        self.canvas.delete('all')
        self.node_canvas_map.clear()
        if not self.builder:
            return

        # Layout nodes in vertical columns per level (columns = levels)
        max_level = self.builder.num_levels + 1  # including leaves level
        width = int(self.canvas['width'])
        height = int(self.canvas['height'])

        # compute x for each level (columns left->right: leaves..root)
        x_gap = width // (max_level + 1)

        for level in range(1, max_level + 1):
            nodes = self.builder._nodes_by_level.get(level, [])
            count = len(nodes)
            if count == 0:
                continue
            x = level * x_gap
            # distribute nodes vertically in the column
            y_gap = height // (count + 1)
            for i, node in enumerate(nodes):
                y = (i + 1) * y_gap
                if node.is_leaf():
                    r = 16
                    oval = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=self._color_for_value(node.value), outline='black')
                    txt = self.canvas.create_text(x, y, text=str(node.value), font=('TkDefaultFont', 10, 'bold'))
                    self.node_canvas_map[node] = {'oval': oval, 'text': txt, 'x': x, 'y': y}
                    # clicking a leaf toggles its value directly
                    self.canvas.tag_bind(oval, '<Button-1>', lambda e, n=node: self.toggle_leaf_node(n))
                    self.canvas.tag_bind(txt, '<Button-1>', lambda e, n=node: self.toggle_leaf_node(n))
                else:
                    w = 80
                    h = 36
                    rect = self.canvas.create_rectangle(x - w//2, y - h//2, x + w//2, y + h//2, fill='#f5f5f8', outline='black')
                    name = node.gate.__class__.__name__
                    txt = self.canvas.create_text(x, y, text=name)
                    # light for output
                    light = self.canvas.create_oval(x + w//2 + 6, y - 8, x + w//2 + 20, y + 8, fill='grey', outline='black')
                    self.node_canvas_map[node] = {'rect': rect, 'text': txt, 'light': light, 'x': x, 'y': y}
                    self.canvas.tag_bind(rect, '<Button-1>', lambda e, n=node: self.on_node_click(n))
                    self.canvas.tag_bind(txt, '<Button-1>', lambda e, n=node: self.on_node_click(n))

        # Draw connections between levels: parent (level L) to children (level L+1)
        for level in range(1, max_level):
            parents = self.builder._nodes_by_level.get(level, [])
            children = self.builder._nodes_by_level.get(level + 1, [])
            for p_idx, parent in enumerate(parents):
                left_child = children[2 * p_idx]
                right_child = children[2 * p_idx + 1]
                pcoords = (self.node_canvas_map[parent]['x'], self.node_canvas_map[parent]['y'])
                lcoords = (self.node_canvas_map[left_child]['x'], self.node_canvas_map[left_child]['y'])
                rcoords = (self.node_canvas_map[right_child]['x'], self.node_canvas_map[right_child]['y'])
                # simple straight lines
                self.canvas.create_line(pcoords[0], pcoords[1], lcoords[0], lcoords[1], fill='#333')
                self.canvas.create_line(pcoords[0], pcoords[1], rcoords[0], rcoords[1], fill='#333')

    def _color_for_value(self, v):
        return 'green' if v == 1 else 'red'

    def on_node_click(self, node):
        self.selected_node = node
        desc = 'Hoja' if node.is_leaf() else node.gate.__class__.__name__
        self.info_label['text'] = f"Seleccionado: {desc}"

    def toggle_leaf_node(self, node):
        # Toggle leaf value only if it's actually a leaf
        if not node.is_leaf():
            # If clicked internal node, select it instead
            self.on_node_click(node)
            return
        node.value = 0 if node.value == 1 else 1
        # Immediately re-evaluate and update visuals
        self.evaluate_and_update()

    def toggle_flipflop(self):
        if self.selected_node is None:
            self.info_label['text'] = 'Selecciona primero un nodo.'
            return
        node = self.selected_node
        if hasattr(node, 'attached_flipflop') and node.attached_flipflop is not None:
            node.attached_flipflop = None
            node.flip_reset_value = 0
            self.info_label['text'] = 'FlipFlop removido.'
        else:
            node.attached_flipflop = FlipFlop()
            node.flip_reset_value = self.ff_reset_var.get()
            self.info_label['text'] = 'FlipFlop adjuntado.'
        self.evaluate_and_update()

    def evaluate_and_update(self):
        if not self.root_node:
            return
        # Update flip reset values globally to currently selected reset Var
        # For simplicity, apply same reset value to all attached flipflops
        r = int(self.ff_reset_var.get())
        # walk all nodes and set flip_reset_value if attached
        for level_nodes in self.builder._nodes_by_level.values():
            for node in level_nodes:
                if hasattr(node, 'attached_flipflop') and node.attached_flipflop is not None:
                    node.flip_reset_value = r

        out = self.root_node.evaluate()

        # Update canvas lights and leaf visuals
        for node, items in self.node_canvas_map.items():
            if node.is_leaf():
                color = self._color_for_value(node.result if node.result is not None else node.value)
                self.canvas.itemconfig(items['oval'], fill=color)
                if 'text' in items:
                    # show the effective result if available, otherwise the leaf value
                    display = node.result if node.result is not None else node.value
                    self.canvas.itemconfig(items['text'], text=str(display))
            else:
                val = node.result
                color = 'green' if val == 1 else 'red'
                self.canvas.itemconfig(items['light'], fill=color)

        # No separate leaves panel; values updated directly on canvas

        self.info_label['text'] = f"Salida total: {out}"

    def ask_initial_levels(self):
        # Prompt the user for initial number of levels (1..6)
        try:
            n = simpledialog.askinteger("Niveles", "Elige cantidad de niveles (1-6):", minvalue=1, maxvalue=6, initialvalue=self.level_var.get(), parent=self.root)
        except Exception:
            n = None
        if n is None:
            return
        self.level_var.set(n)
        self._build_level_selectors(n)
        # Auto-build initial tree
        self.build_and_render()


def main():
    root = tk.Tk()
    app = CircuitGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
