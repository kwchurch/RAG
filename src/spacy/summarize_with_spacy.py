#!/usr/bin/env python3

# based on https://www.geeksforgeeks.org/text-summarization-in-nlp/
# and https://www.geeksforgeeks.org/extract-text-from-pdf-file-using-python/

import sys,os
import spacy
import pytextrank

try:
    nlp = spacy.load("en_core_web_lg")
except Exception as e:
    print('Exception: ' + str(e), file=sys.stderr)
    print('please run this:\n\tpython3 -m spacy download en_core_web_lg', file=sys.stderr)

nlp.add_pipe("textrank")

from pypdf import PdfReader 

for f in sys.argv[1:]:
    print('file: ' + str(f))
    if f.lower().endswith('.pdf'):
        reader = PdfReader(f)
        txt = '\n'.join([page.extract_text() for page in reader.pages])
        doc = nlp(txt)
        print('Summary: ')
        for sent in doc._.textrank.summary(limit_phrases=2, limit_sentences=2):
            print('\t' + str(sent))
    print('\n')


