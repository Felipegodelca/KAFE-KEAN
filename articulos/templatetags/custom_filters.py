from django import template

register = template.Library()


@register.filter
def percentage(value, maximum=10):
    try:
        value = float(value)
        maximum = float(maximum)
        if maximum == 0:
            return 0
        return max(0, min(100, (value / maximum) * 100))
    except (TypeError, ValueError):
        return 0
