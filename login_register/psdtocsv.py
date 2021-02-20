import os,glob
import csv
from os import remove
import re
from string import punctuation
from io import StringIO
from nltk import word_tokenize
from nltk.corpus import stopwords
import fitz
stopword = stopwords.words("english")


def pdf_to_txt(file):
    try:
        doc = fitz.open(file,None,'pdf')
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
        num_removed= re.sub(r'\d', "", tab_removed)
        spcl_word_removed=re.sub('\W_',' ', num_removed) 
        asd=re.sub("[^a-zA-Z]+", " ", spcl_word_removed)
        filtered_data = asd.replace('−', '').replace('  ', '').replace(u'\ufffd', '')

        return title, filtered_data.casefold()
    except:
        return "error","error"
i=0

path='E:\pdfreports'

with open('reports.csv', 'w', newline='',encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["SN", "FName", "Title","Data"])
    for filename in glob.glob(os.path.join(path, '*.pdf')):
        i=i+1
        filenames=str(filename)
        title,data=(pdf_to_txt(filename))
        if title!="error" and data!="error":
            writer = csv.writer(file)
            writer.writerow([i, filenames, title,data])