from django import template

register = template.Library()

@register.filter()
def notificaciones_tag(context):
    user = user_context(context)

    if not user:
        return ''

    return user.notificacion.no_leido()

notificaciones = register.simple_tag(takes_context=True)(notificaciones_tag)

def user_context(context):
    if 'user' not in context:
        return None
    request = context['request']
    user = request.user

    return user