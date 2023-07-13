from django import template

register = template.Library()

BAD_WORDS = ('fuck', 'bitch', 'Fuck', 'Bitch')

class StrException(Exception):
    def __str__(self):
        return 'Фильтр censor принимает только текст '


@register.filter()
def censor(text):
    if not isinstance(text, str):
        raise StrException
    else:
        t = text.split(' ')
        for i, b in enumerate(t):
            if b in BAD_WORDS:
                t[i] = b[0] + '*' * int(len(b) - 1)
        return ' '.join(t)




