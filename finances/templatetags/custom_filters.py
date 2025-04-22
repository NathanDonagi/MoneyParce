import random
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

PASTEL_COLORS = [
    "#FFF0F5",  # Lavender Blush (very pale pink)
    "#F0FFF0",  # Honeydew (very pale green)
    "#F0F8FF",  # Alice Blue (very pale blue)
    "#FFF8E7",  # Cosmic Latte (very pale cream)
    "#E6F5FD",  # Light Cyan (very pale cyan)
    "#FFEEF2",  # Pale Pink (very light pink)
    "#F5F0FF",  # Lavender Mist (very pale purple)
    "#F0FFE6",  # Light Mint (very pale mint green)
    "#FFF5EE",  # Seashell (very pale orange)
    "#E8F8F5"   # Mint Cream (very pale teal)
]

color_index = 0

assigned_colors = {}

@register.filter
def get_dynamic_color(category):
    global color_index
    global assigned_colors

    if category.id not in assigned_colors:
        assigned_colors[category.id] = PASTEL_COLORS[color_index]
        color_index = (color_index + 1) % len(PASTEL_COLORS)

    return assigned_colors[category.id]

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0
