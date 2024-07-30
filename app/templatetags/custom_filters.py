from django import template

register = template.Library()


@register.filter(name='split')
def split(value, delimiter=' '):
    return value.split(delimiter)


@register.filter(name='get_index')
def get_index(value, arg):
    try:
        index = int(arg)  # Пытаемся преобразовать аргумент в целое число (индекс)
        return value[index]  # Возвращаем элемент списка по индексу
    except (IndexError, ValueError, TypeError):
        return None  # В случае ошибки возвращаем None или можно вернуть другое значение по умолчанию
