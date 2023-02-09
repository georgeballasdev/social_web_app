from django import template


register = template.Library()

@register.filter
def joined(user, members):
    return user in members