import csv
from os import remove
import re
from string import punctuation
from io import StringIO
import pdftotext
from nltk import word_tokenize
from nltk.corpus import stopwords
import fitz
stopword = stopwords.words("english")


def pdf_to_txt(file):
    doc = fitz.open(file)
    project_data = StringIO()
    for page in range(doc.pageCount):
        project_data.write(doc[page].getText("block"))
    project_data_content = project_data.getvalue()
    reading = project_data_content.split("\n")
    title = reading[0].strip()
    body = project_data_content.strip()
    work = word_tokenize(body)
    removing_stopwords = [word for word in work if word not in stopword]
    removing_stopwords[:] = [x for x in removing_stopwords if x != '“']
    listToStr = ' '.join(map(str, removing_stopwords))
    removed_words = re.sub(r'\b\w{1,3}\b', ' ', listToStr)
    '''remove_unwanted_strings'''
    new_data = ''.join(c for c in removed_words if c not in punctuation)
    tab_removed = re.sub('\s+', ' ', new_data)
    filtered_data = tab_removed.replace('−', '').replace('  ', '')
    return title, filtered_data
