from django import template
# from django.utils.html import conditional_escape
# from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def setActiveClass(name,current):
    if name == current :
        return 'active'
    else:
        return ''