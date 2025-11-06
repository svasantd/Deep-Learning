"""
Formatting utilities for terminal-style display
"""

# Color constants
COLOR_GREEN = "#00ff41"
COLOR_RED = "#ff0844"
COLOR_WHITE = "#ffffff"
COLOR_BG = "#1a1a1a"


def format_currency(value, decimals=1):
    """
    Format currency values in millions
    Examples: $12.3M, $4.2M
    """
    if value >= 1000000:
        return f"${value/1000000:.{decimals}f}M"
    elif value >= 1000:
        return f"${value/1000:.{decimals}f}K"
    else:
        return f"${value:.0f}"


def format_percentage(value, decimals=0, show_sign=True):
    """
    Format percentage values
    Examples: 8%, -5%, +12%
    """
    sign = ""
    if show_sign and value > 0:
        sign = "+"
    elif show_sign and value < 0:
        sign = ""  # Negative sign included in number

    return f"{sign}{value*100:.{decimals}f}%"


def get_trend_color(value):
    """
    Get color based on trend direction
    Positive = green, Negative = red, Zero = white
    """
    if value > 0:
        return COLOR_GREEN
    elif value < 0:
        return COLOR_RED
    else:
        return COLOR_WHITE


def get_trend_arrow(value):
    """
    Get arrow symbol based on trend direction
    Positive = ▲, Negative = ▼, Zero = →
    """
    if value > 0:
        return "▲"
    elif value < 0:
        return "▼"
    else:
        return "→"


def get_trend_text(value, decimals=0):
    """
    Get formatted trend text with arrow
    Examples: "▲ 8%", "▼ 5%"
    """
    arrow = get_trend_arrow(value)
    pct = format_percentage(abs(value), decimals=decimals, show_sign=False)
    return f"{arrow} {pct}"


def get_expiration_color(days):
    """
    Get color based on contract expiration
    <60 days = red, otherwise white
    """
    if days < 60:
        return COLOR_RED
    else:
        return COLOR_WHITE


def get_expiration_indicator(days):
    """
    Get expiration indicator
    <60 days = 🔴, otherwise empty
    """
    if days < 60:
        return "🔴"
    else:
        return ""


def get_priority_marker(level):
    """
    Get priority marker for action items
    critical = 🔴, high = 🔴, medium = ▲, low = ▼
    """
    if level in ["critical", "high"]:
        return "🔴"
    elif level == "medium":
        return "▲"
    else:
        return "▼"


def format_margin_change(current_margin, previous_margin):
    """
    Format margin change indicator
    Examples: "28% ▲", "15% ▼"
    """
    change = current_margin - previous_margin
    arrow = get_trend_arrow(change)
    return f"{format_percentage(current_margin, decimals=0, show_sign=False)} {arrow}"


def calculate_sgp_2024(sgp_2025, yoy_change):
    """
    Calculate 2024 SGP from 2025 SGP and YoY change
    Formula: SGP_2024 = SGP_2025 / (1 + YoY_change)
    """
    return sgp_2025 / (1 + yoy_change)


def get_colored_text(text, color):
    """
    Wrap text in HTML span with color
    """
    return f'<span style="color: {color};">{text}</span>'


def get_monospace_text(text):
    """
    Wrap text in monospace font
    """
    return f'<span style="font-family: monospace;">{text}</span>'
