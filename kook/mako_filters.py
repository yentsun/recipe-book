from operator import attrgetter
from markdown import markdown as markdown_

def markdown(text):
    return markdown_(text, output_format='html5', safe_mode=True)

def not_none(string):
    if string is None or string == 'None':
        return ''
    return string

def failsafe_get(object, atrr_path):
    #TODO maybe reverse-engineer Deform instead of using this
    if object:
        try:
            extractor = attrgetter(atrr_path)
            result = extractor(object)
        except AttributeError:
            try:
                result = object[atrr_path]
            except (KeyError, TypeError):
                result = None
    else:
        result = None
    return not_none(result)