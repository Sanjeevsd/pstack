import csv
import re
from string import punctuation
from io import StringIO
import pdftotext
from nltk import word_tokenize
from nltk.corpus import stopwords

stopword = stopwords.words("english")
def pdf_to_txt(f):
    reading = pdftotext.PDF(f)
    project_data=StringIO()
    for pages in reading:
        if pages!='':
            project_data.write(pages)
        else:
            return ("error","failed to read")
    project_data_content=project_data.getvalue()
    reading=project_data_content.split("\n")
    title = reading[0].strip()
    body = project_data_content.strip()
    work = word_tokenize(body)
    removing_stopwords = [word for word in work if word not in stopword]
    print(work)
    listToStr = ' '.join(map(str, removing_stopwords))
    removed_words = re.sub(r'\b\w{1,3}\b', ' ', listToStr)
    '''remove_unwanted_strings'''
    new_data = ''.join(c for c in removed_words if c not in punctuation)

    tab_removed = re.sub('\s+', ' ', new_data)
    filtered_data = tab_removed.replace('−','').replace('  ', '')
    print(filtered_data)
    return title, filtered_data


