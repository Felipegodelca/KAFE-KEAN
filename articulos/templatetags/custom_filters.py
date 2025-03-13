from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    """
    Agrega una clase CSS a un widget de formulario en una plantilla.
    """
    if hasattr(value, 'field') and value.field.widget:
        existing_classes = value.field.widget.attrs.get('class', '')
        value.field.widget.attrs['class'] = f"{existing_classes} {css_class}".strip()
    return value

@register.filter(name='is_active')
def is_active(url_name, current_name):
    """
    Retorna 'active' si el nombre de la URL actual coincide con el proporcionado.
    """
    return 'active' if url_name == current_name else ''