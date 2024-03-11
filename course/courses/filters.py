from django import template

register = template.Library()

@register.filter
def format_hours(time_string):
    try:
        hours, minutes, seconds = map(int, time_string.split(':'))
        total_hours = hours + minutes / 60 + seconds / 3600
        return f"{total_hours:.0f} hour{'s' if total_hours != 1 else ''}"
    except (ValueError, AttributeError):
        return ''