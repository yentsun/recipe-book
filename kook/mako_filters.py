from markdown import markdown as markdown_

def markdown(text):
    return markdown_(text, output_format='html5', safe_mode=True)

def not_none(string):
    if string is None or string == 'None':
        return ''
    return string