
# А это шобы библиотека делала нормальные запросы на сервер
def escape_html(text):
    """
    Escapes all html characters in text
    :param str text:
    :rtype: str
    """
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')