from bs4 import BeautifulSoup
import requests
import random
import re

HEADERS = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9 ',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/101.0.4951.54 Safari/537.36'}

url_dict = 'https://dictionary.cambridge.org/ru/%D1%81%D0%BB%D0%BE%D0%B2%D0%B0%D1%80%D1%8C/%D0%B0%D0%BD%D0%B3%D0%BB' \
           '%D0%B8' \
           '%D0%B9%D1%81%D0%BA%D0%B8%D0%B9/'

alert = 'wordNotFound'


def get_examples(word_ex):
    """Gets sentences with the word"""
    url = url_dict + word_ex
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.text, "lxml")
    p = list(i.text.strip() for i in soup.select("[class~=deg]"))

    correct_exps = list()
    for i in p:
        if re.findall(r'(?i)\b' + word_ex + r'.*?(?=\W)', i):
            correct_exps += [i]

    return tuple(correct_exps) if len(correct_exps) > 0 else alert


def str_replace_re(bad_word, need_word, line):
    return re.sub(r"(?i)\b" + bad_word + r".*?(?=\W)", need_word, line)


def get_test(need_word):
    """Creates a sentence with a missing word"""
    lst_ex = get_examples(need_word)
    if lst_ex == alert:
        return alert
    n = random.randint(0, len(lst_ex))

    return str_replace_re(need_word, '______', lst_ex[n])


# c = get_test('car')
# print(c)


