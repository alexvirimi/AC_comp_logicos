"""Constantes y configuración de la aplicación."""

# Colores para los niveles (neon)
LEVEL_COLORS = [
    {"border": "#facc15", "bg": "rgba(250, 204, 21, 0.08)", "text": "#facc15"},         # Amarillo
    {"border": "#22c55e", "bg": "rgba(34, 197, 94, 0.08)", "text": "#22c55e"},         # Verde
    {"border": "#3b82f6", "bg": "rgba(59, 130, 246, 0.08)", "text": "#3b82f6"},       # Azul
    {"border": "#f97316", "bg": "rgba(249, 115, 22, 0.08)", "text": "#f97316"},       # Naranja
    {"border": "#a855f7", "bg": "rgba(168, 85, 247, 0.08)", "text": "#a855f7"},       # Púrpura
    {"border": "#ec4899", "bg": "rgba(236, 72, 153, 0.08)", "text": "#ec4899"},       # Rosa
]

# Colores de tema oscuro
COLORS = {
    "bg_primary": "#0f172a",        # Fondo principal oscuro
    "bg_secondary": "#1e293b",      # Fondo secundario
    "bg_tertiary": "#334155",       # Fondo terciario
    "border": "#475569",             # Color de borde
    "border_color": "#475569",      # Alias para borde
    "text_primary": "#f1f5f9",      # Texto principal
    "text_secondary": "#94a3b8",    # Texto secundario
    "green": "#22c55e",             # Verde (1)
    "red": "#ef4444",               # Rojo (0)
    "success_green": "#22c55e",     # Verde (1)
    "error_red": "#ef4444",         # Rojo (0)
    "primary_blue": "#3b82f6",      # Azul primario
}

# Dimensiones y espacios
LAYOUT = {
    "input_column_width": 80,
    "level_column_width": 200,
    "gate_size": (80, 80),
    "spacing": 20,
}

WINDOW_SIZE = (1400, 800)
INITIAL_DIALOG_SIZE = (500, 400)
