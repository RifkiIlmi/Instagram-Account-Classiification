from django import template
register = template.Library()

@register.simple_tag()
def multiply(a, b, *args, **kwargs):
    # you would need to do any localization of the result here
    return float(a) * float(b)