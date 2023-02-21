import re

import threading

from pymystem3 import Mystem
from nltk.corpus import stopwords
import nltk
nltk.download("stopwords")



class TextPreproccessor:
    def __init__(self):
        self.__html_pattern = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        self.__alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя "

        self.__mystem = Mystem()  # for lemmatization
        self.__russian_stopwords = stopwords.words("russian")

    def __remove_html(self, text: str) -> str:
        return re.sub(self.__html_pattern, '', text)

    def __filter_symbols(self, text: str) -> str:
        return ''.join([symbol for symbol in text if symbol in self.__alphabet])

    def __lemmatization(self, text: str) -> str:
        return ''.join(self.__mystem.lemmatize(text))

    def __strip(self, text: str) -> str:
        return text.strip()

    def __lower(self, text: str) -> str:
        return text.lower()

    def __remove_stopwords(self, text: str) -> str:
        words = text.split(' ')

        words_without_stopwords = []

        for word in words:
            if word not in self.__russian_stopwords:
                words_without_stopwords.append(word)

        return ' '.join(words_without_stopwords)

    # do async
    def async_prepoccess_texts(self, texts: list) -> list:

        threads = []

        for text in texts[:30]:
            t = threading.Thread(target=self.preproccess_text, args=(text))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
         


    def preproccess_text(self, text: str) -> str:
        text = self.__remove_html(text)
        text = self.__lower(text)
        text = self.__strip(text)
        text = text.replace('ё', 'e')
        text = self.__filter_symbols(text)
        text = self.__remove_stopwords(text)
        text = self.__lemmatization(text)

        return text
