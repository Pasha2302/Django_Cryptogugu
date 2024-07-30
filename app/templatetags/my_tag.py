from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import SafeString
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from datetime import datetime
from zoneinfo import ZoneInfo

from app.models import UserSettings

register = template.Library()


@register.simple_tag
def get_current_theme(user_id):
    if user_id:
        user_sett: UserSettings = UserSettings.objects.get(user_id=user_id)
        return user_sett.theme_site


# <is_safe=True> Возвращаемые строки HTML (и другие спец символы) не экранируются. (HTML рендериться как HTML).
@register.filter(is_safe=True)
# @register.filter()
@stringfilter  # Преобразовать объект в его строковое значение перед передачей функцию
def tag_filter_test(value: str, mark_safe_str: str = 'false'):
    mark_safe_bool = mark_safe_str.lower() in ['true', '1', 'yes']
    # print(f"\nInput Filter Data: {value}")

    data = value.replace('фильтра',
                         'TEST!')  # После форматирование строка перестает быть (SafeString) становиться просто (str)
    if mark_safe_bool:
        data = mark_safe(data)  # <mark_safe(str)> Пометить вывод как безопасную строку

    if isinstance(data, SafeString):
        return data

    else:
        return '<h2>Строка не безопасна (имеет символы HTML)</h2>'


# Флаг needs_autoescape и аргумент ключевого слова autoescape означают,
# что при вызове фильтра наша функция будет знать, действует ли автоматическое экранирование
@register.filter(needs_autoescape=True)
def strong_first(text: str, autoescape=True):
    print(f"\nAuto Escape: {autoescape}")
    '''В этом случае нет необходимости беспокоиться о флаге is_safe (хотя его включение ничего не изменит).
    Если вы вручную справитесь с проблемами автоэскейпинга и вернете безопасную строку,
    флаг is_safe ничего не изменит в любом случае.'''
    first, *other = text.split()
    if autoescape:
        # <conditional_escape> Экранирует только те входные данные,
        # которые **не являются экземплярами SafeData. Если экземпляр SafeData передан в conditional_escape(),
        # данные возвращаются без изменений.
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = f"<strong>{esc(first)}</strong> {esc(' '.join(other))}"
    return mark_safe(result)  # <mark_safe(str)> Пометить вывод как безопасную строку


# Фильтры и часовые пояса:
# Если вы пишете пользовательский фильтр,
# который работает с объектами datetime,
# вы обычно регистрируете его с флагом expects_localtime, установленным на True:
@register.filter(expects_localtime=True)
def working_hours(value):
    try:
        return 9 <= value.hour < 17
    except AttributeError:
        return ""


# Когда этот флаг установлен, если первым аргументом вашего фильтра является дататайм с учетом часового пояса,
# Django преобразует его в текущий часовой пояс,
# прежде чем передать его в ваш фильтр, когда это необходимо,
# в соответствии с https://django.fun/docs/django/5.0/topics/i18n/timezones/#time-zones-in-templates


@register.simple_tag
def current_time_in_timezone(timezone_str=None):
    """
    Возвращает текущее время в указанной временной зоне.
    Если временная зона не указана, возвращает время в текущей временной зоне Django.
    """
    # Получаем текущее время в UTC
    now_utc = datetime.now(ZoneInfo("UTC"))

    if timezone_str:
        try:
            # Используем ZoneInfo для конвертации времени в указанную временную зону
            tz = ZoneInfo(timezone_str)
            now_local = now_utc.astimezone(tz)
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        # Преобразуем текущее время в локальное время по умолчанию
        # Используем текущую временную зону Django
        # Убедитесь, что вы установили TIME_ZONE в settings.py
        tz = ZoneInfo("UTC")  # Замените "UTC" на вашу временную зону по умолчанию, если необходимо
        now_local = now_utc.astimezone(tz)

    # Форматируем время для удобства отображения
    return now_local.strftime('%Y-%m-%d %H:%M:%S %Z%z')
