from django import template
register = template.Library()

@register.filter(name='access')
def access(value, arg):
    if arg is None:
        return "-"
    if arg not in value:
        return arg
    return value[arg]

@register.filter(name='second')
def second(arg):
    return arg[1]

@register.filter(name='third')
def third(arg):
    return arg[2]

@register.filter(name='forth')
def forth(arg):
    return arg[3]

@register.filter(name='fifth')
def fifth(arg):
    return arg[4]

@register.filter(name='sixth')
def sixth(arg):
    return arg[5]

@register.filter(name='seventh')
def seventh(arg):
    return arg[6]

@register.filter(name='eighth')
def eighth(arg):
    return arg[7]

@register.filter(name='nineth')
def nineth(arg):
    return arg[8]
