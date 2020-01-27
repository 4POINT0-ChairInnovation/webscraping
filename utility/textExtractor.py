from bs4 import BeautifulSoup
from bs4.element import Comment


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    clean_text = ""
    for t in visible_texts:
        t = t.strip()
        if len(t) > 0:
            text = ""
            for line in t.splitlines():
                line = line.strip()
                if len(line) > 0:
                    text = text + '\n'+ line
            clean_text = clean_text + text
    return clean_text
