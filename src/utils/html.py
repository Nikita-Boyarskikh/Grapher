from functools import partial


def tag(name: str, content: str) -> str:
    return '<{tag}>{content}</{tag}>'.format(tag=name, content=content)


def link(content: str, href: str = '#') -> str:
    return '<a href="{}">{}</a>'.format(href, content)


ul = partial(tag, 'ul')
li = partial(tag, 'li')
p = partial(tag, 'p')
