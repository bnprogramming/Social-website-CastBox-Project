# write special and customize filter and template tag
from django import template
from jalali_date import date2jalali

register = template.Library()


def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, "")


def lower(value):  # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()


@register.filter(name="showjalalidate")
def show_jalali_date(value):
    date = date2jalali(value)
    return f' Date : {date.day} - {date.month} - {date.year}'


@register.filter(name="showtime")
def show_time(value):
    time = value.strftime('%H:%M')
    return f'Hour : {time}'


register.filter("cut", cut)
register.filter("mylower", lower)
