# -*- coding: utf-8 -*-

from operator import attrgetter
from markdown import markdown as markdown_
from datetime import datetime


def markdown(text):
    return markdown_(text, output_format='html5', safe_mode=True)


def failsafe_get(object_, atrr_path):
    #TODO maybe reverse-engineer Deform instead of using this
    if object_:
        try:
            extractor = attrgetter(atrr_path)
            result = extractor(object_)
        except AttributeError:
            try:
                result = object_[atrr_path]
            except (KeyError, TypeError):
                result = None
    else:
        result = None
    return result


def pretty_time(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    taken from:
    http://stackoverflow.com/questions/1551382/python-user-friendly-time-format
    """
    if not time:
        return ''
    now = datetime.now()
    diff = 0
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff is 0:
        if second_diff < 10:
            return u'только что'
        if second_diff < 60:
            return str(second_diff) + u' сек. назад'
        if second_diff < 120:
            return u'минуту назад'
        if second_diff < 3600:
            return str( second_diff / 60 ) + u' мин. назад'
        if second_diff < 7200:
            return u'час назад'
        if second_diff < 86400:
            return str( second_diff / 3600 ) + u' час. назад'
    if day_diff == 1:
        return u'вчера'
    if day_diff < 7:
        return str(day_diff) + u' дн. назад'
    if day_diff < 31:
        return str(day_diff/7) + u' нед. назад'
    if day_diff < 365:
        return str(day_diff/30) + u' мес. назад'
    return str(day_diff/365) + u' лет назад'