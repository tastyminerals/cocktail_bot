#!/usr/bin/env python3
"""
This script implements information extraction model that uses cosine similarity
and tf-idf statistics. It uses cocktails.xml as a data source. The script
evaluates user query and returns the most relevant document.
"""

import os
import string
import xml.etree.cElementTree as cet
import numpy as np
import math
import sys
from collections import Counter, defaultdict
from nltk import word_tokenize, pos_tag
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn


# @profile
def init_cocktails_database(dbfile, tf_file=False, idf_file=False):
    """
    This function reads db_file, does basic text normalization steps and
    converts all data into a bad of words model. The scipt also writes tf and
    tfidf index files for faster processing.

    INPUT:
        db_file --  full path to cocktails database
        tf_file --  filename with .tf extension
        idf_file    --  filename with .idf extension
    OUTPUT:
        cocktails.tf    --  file containing term freq values
        cocktails.tfidf --  file containing term freq - inverted doc freq values
        docs    --  dict representation of db_file
        # wordsbag    --  normalized dictionary of terms per doc
    """
    # parsing xml file and creating its dict representation
    docs = {}
    xml_iter = cet.iterparse(dbfile, events=('start', 'end'))
    for event, elem in xml_iter:
        if event == 'start':
            if elem.tag == 'cocktail':
                docid = elem.attrib['name']
                docs[docid] = ''
        if event == 'end':
            if elem.tag == 'prime':
                docs[docid] = {'prime': elem.text}
            elif elem.tag == 'description':
                docs[docid].update({'description': elem.text})
            elif elem.tag == 'history':
                docs[docid].update({'history': elem.text})
            elif elem.tag == 'trivia':
                docs[docid].update({'trivia': elem.text})
            elif elem.tag == 'comments':
                docs[docid].update({'comments': elem.text})
            elif elem.tag == 'ingredients':
                docs[docid].update({'ingredients': elem.text})
            elif elem.tag == 'mixing':
                docs[docid].update({'mixing': elem.text})
            elem.clear()
    del xml_iter
    # normalizing xml file data and creating a bad of words dict
    # initializing SnowballStemmer from nltk
    sst = SnowballStemmer('english')
    # taking stopwords from nltk
    stop = stopwords.words('english')
    # creating translation table to remove punctuation
    transpunct = {ord(c): None for c in string.punctuation}
    # first we remove any punctuation and concatenate specific nodes into one
    dirtywordsbag = {}
    for doc in docs:
        dirtywordsbag[doc] = ""
        nodes = filter(lambda x: x in
                       ['description', 'history', 'trivia', 'comments'],
                       docs[doc])
        for node in nodes:
            node_text = (docs[doc][node] or "")  # in case node is empty
            dirtywordsbag[doc] += node_text.lower().translate(transpunct)
    # now we remove stop words and stem the rest
    wordsbag = {doc: tuple(sst.stem(tok) for tok in text.split()
                           if tok not in stop)
                for doc, text in dirtywordsbag.items()}
    # we now create tf and tfidf files from db_file if they do not exist
    # we flatten our wordsbag and calc term frequency of every word for each doc
    # we take db_file name without extension and add .tf extension to it
    # max_freqs is a dict where {doc id: freq of most occurring token, ...}
    max_freqs = {doc: Counter(tokens).most_common()[0]
                 for doc, tokens in wordsbag.items()}
    terms_set = (set(term for d in wordsbag for term in wordsbag[d]))
    if tf_file and tf_file not in os.listdir(os.getcwd()):
        with open(tf_file, 'a') as afile:
            for doc in wordsbag:
                for term in wordsbag[doc]:
                    # calculating tf-values and writing them to file
                    tf_str = str(Counter(wordsbag[doc])[term]/max_freqs[doc][1])
                    vlst = '\t'.join([doc, term, tf_str])
                    afile.write(vlst)
                    afile.write('\n')

    # we take db_file name without extension and add .idf extension to it
    if idf_file and idf_file not in os.listdir(os.getcwd()):
        doc_cnt = len(wordsbag)
        with open(idf_file, 'a') as afile:
            for term in terms_set:
                # calculating idf values and writing them to idf file
                idf = math.log(doc_cnt/len([term for doc in wordsbag
                                            if term in wordsbag[doc]]))
                afile.write('\t'.join([term, str(idf)]))
                afile.write('\n')
    return docs


# @profile
def wordnet_sim(query, db):
    """
    This function imlements simple wordnet definition lookup and compares it
    with a different block of text. For every word match between the definition
    token and text token doc receives +1.

    INPUT:
    query  --  string that represents user query expanded with word net defs
    db  --  dict representation of database xml file

    OUTPUT:
    maxdoc  --  the document with the highest score
    """
    # print('QUERY:', query)
    # initializing SnowballStemmer from nltk
    sst = SnowballStemmer('english')
    # taking stopwords from nltk
    stop = stopwords.words('english')
    # creating translation table to remove punctuation
    transnone = {ord(c): None for c in string.punctuation}
    # first we remove any punctuation and concatenate specific nodes into one
    query_nopunct = query.lower().translate(transnone)
    query_stems = [sst.stem(token) for token in query_nopunct.split()
                   if token not in stop]
    doc_scores = defaultdict(float)
    for doc in db:
        for block, text in db[doc].items():
            # normalize block text
            if not text:
                continue
            text_nopunct = text.lower().translate(transnone)
            text = [sst.stem(t) for t in text_nopunct.split() if t not in stop]
            # here we can finetune the block score multiplicators
            # some blocks are more important than the others
            if block == 'description':
                for s in query_stems:
                    doc_scores[doc] += text.count(s) / len(text) * 2
            elif block == 'trivia':
                for s in query_stems:
                    doc_scores[doc] += text.count(s) / len(text) * 0.5
            elif block == 'history':
                for s in query_stems:
                    doc_scores[doc] += text.count(s) / len(text) * 0.5
            elif block == 'comments':
                for s in query_stems:
                    doc_scores[doc] += text.count(s) / len(text)
    maxdoc = max(doc_scores, key=lambda x: doc_scores[x])
    debug = sorted([(k,v) for k,v in doc_scores.items()], key=lambda x: x[1])
    return (debug, maxdoc)


# @profile
def expand_with_wordnet(query):
    """
    This function expands every contentful word in the query with its wordnet
    definition. The word itself is not removed. Stop words are removed from the
    word definition as well.
    (Contentful means that it is not a stopword or punctuation sign)

    INPUT:
        query   --  user query that is a simple string
    OUTPUT:
        expanded_query  --  user query + definitions of contentful words
    """
    stop = stopwords.words('english')
    stop += EXCLUDED
    contentful_tokens = [tok for tok in query.split() if tok not in stop]
    # take the first definition for the current word
    defs = []
    for token in contentful_tokens:
        syn1 = wn.synsets(token, pos=wn.ADJ)[:1]
        syn2 = wn.synsets(token, pos=wn.NOUN)[:1]
        # we take into account only adj defs
        if syn1:
            defs.append(token)
            def_tokenized = word_tokenize(syn1[0].definition())
            [defs.append(t[0]) for t in pos_tag(def_tokenized) if t[1] in ['NN', 'JJ']]
        elif syn2:
            defs.append(token)
            def_tokenized = word_tokenize(syn2[0].definition())
            [defs.append(t[0]) for t in pos_tag(def_tokenized) if t[1] in ['NN', 'JJ']]
    # expansion can add some EXCLUDED words back in the query
    defs = set(defs) - set(EXCLUDED)  # removing again
    expanded = ' '.join(defs)
    return expanded


# @profile
def init_db_vectors(tf_file, idf_file):
    """
    This function creates document vectors of tf-idf values as simple dicts

    INPUT:
        tf_file --  filename with .tf extension
        idf_file    --  filename with .idf extension
    OUTPUT:
        docvec  --  a dict of {doc: {term: tfidf, ...}}
        invidx  --  a dict of {term: {doc: tfidf, ...}}
        idfdict  --  a dict of {term: idf, ...}
    """
    # read tf and idf files
    with open(tf_file, 'r') as rfile:
        tfdata = rfile.read()
    with open(idf_file, 'r') as rfile:
        idfdata = rfile.read()
    # create tfdict from tf read data
    tfdict = defaultdict(dict)
    for line in tfdata.split('\n')[:-1]:
        doc, term, tf = line.split('\t')
        tfdict[doc].update({term: float(tf)})
    # create idfdict from idf read data
    idfdict = dict((l.split('\t')[0], float(l.split('\t')[1]))
                   for l in idfdata.split('\n')[:-1])
    # create tfidf dict and inverted index dict
    docvec = defaultdict(dict)
    invidx = defaultdict(dict)
    for doc in tfdict:
        for term in idfdict:
            if tfdict[doc].get(term):
                tfidf = tfdict[doc][term] * idfdict[term]
                docvec[doc].update({term: tfidf})
                invidx[term].update({doc: tfidf})  # inverted dict
    return docvec, invidx, idfdict

# @profile
def calculate_similarity(docdict, invdict, idfdict, query):
    """
    This function calculates cosine similarity between documents in dvecs and
    a user query. It then returns the document with highest sim value.

    INPUT:
        docvec  --  a dict of {doc: {term: tfidf, ...}}
        invdict  --  a dict of {term: {doc: tfidf, ...}}
        idfdict  --  a dict of {term: {doc: tfidf, ...}}
        query   --  user query string
    OUTPUT:
        maxsim  --  tuple with sim score and doc id
    """
    def slow_sim(v1, v2, d):
        """
        This function calculates cosine similarity for the given vectors

        INPUT:
            v1  --  first vector of tfidf values
            v2  --  second vector of tfidf values
            d   --  document id
        OUTPUT:
            float, d   --  tuple of similarity score, document id
        """
        np.seterr(divide='ignore', invalid='ignore')  # in case of NaN
        # query norm
        qnorm = math.sqrt(sum([pow(x, 2) for x in v1]))
        # doc norm
        dnorm = math.sqrt(sum([pow(y[1], 2) for y in docdict[d].items()]))
        return np.dot(v1, v2) / (qnorm * dnorm), d

    # first, we preprocess query and expand it with synonyms
    # query = expand_with_wordnet(query)
    # initializing SnowballStemmer from nltk
    sst = SnowballStemmer('english')
    # taking stopwords from nltk
    stop = stopwords.words('english')
    # we exclude some words that we do not need in the query
    stop += EXCLUDED
    # creating translation table to remove punctuation
    trans = {ord(c): None for c in string.punctuation}
    # normalizing query
    sq = [sst.stem(term) for term in query.lower().translate(trans).split()
          if term not in stop]
    # create query vector
    qcnts = Counter(sq)
    maxqt = qcnts.most_common(1)[0][1]
    # calculating tf values for the query, 0.4+(1-0.4) is smoothing with a=0.4
    qtf = dict((q, (0.4+((1-0.4)*qcnts[q])/maxqt)) for q in sq)
    # fill query vector with tfidf values
    qvec = [(qtf[t] * idfdict[t]) for t in qtf if t in idfdict]
    invdocvecs = defaultdict(list)
    # fill doc vectors with tfidf values only for those terms that are in query
    [invdocvecs[d].append(invdict[t][d]) for t in qtf for d in invdict[t]]
    # balancing document vectors with zeros
    [invdocvecs[d].extend([0 for _ in
                           range(abs(len(qvec)-len(invdocvecs[d])))])
     for d in docdict]
    # find the doc with the highest cos sim
    max_sim = max(slow_sim(qvec, invdocvecs[doc], doc) for doc in invdocvecs)
    return max_sim

# @profile
def process_query(user_query, analyser, verbosity=0):
    """
    Main runner function that calls the required ruitines
    In this function we decide which similarity measures we use
    tf-idf and cosine similarity versus expanding the user query
    with wordnet word definitions and running weighted counts of
    query words occurrences.

    INPUT:
        user_query  --  unformatted user query
        verbosity   --  number of text blocks shown to user
        analyser  --  specifies which similarity model to use (default wordnet)
    OUTPUT:
        std.out --  prints the cocktail advice
    """
    # initializing database
    db_file = os.path.join(os.getcwd(), 'cocktails.xml')
    tf_fpath = os.path.basename(db_file).rsplit('.', 1)[0] + '.tf'
    idf_fpath = os.path.basename(db_file).rsplit('.', 1)[0] + '.idf'
    docs_db = init_cocktails_database(db_file, tf_fpath, idf_fpath)
    # setting default here because aiml returns undetectable empty str ''
    if analyser == '':
        analyser = 'TFIDF'  # default analyser
    if analyser == 'WORDNET':
        # print('USING WORDNET...')
        # 1. WORDNET
        relevant = wordnet_sim(expand_with_wordnet(user_query), docs_db)
        # relevant = wordnet_sim(user_query, docs_db)
        # print('RELEVANT:', relevant)
    elif analyser == 'TFIDF':
        # print('USING TFIDF...')
        # 2. TF-IDF
        # creating document dicts and vectors
        doc_dic, inv_dic, idf_dic = init_db_vectors(tf_fpath, idf_fpath)
        # calculating the most relevant document
        relevant = calculate_similarity(doc_dic, inv_dic, idf_dic, user_query)
        # print('RELEVANT:', relevant)
    if verbosity == 1:
        desc = docs_db[relevant[-1]]['description']
        ing = docs_db[relevant[-1]]['ingredients']
        mix = docs_db[relevant[-1]]['mixing']
        hist = docs_db[relevant[-1]]['history']
        triv = docs_db[relevant[-1]]['trivia']
    else:
        desc = docs_db[relevant[-1]]['description']
        ing = docs_db[relevant[-1]]['ingredients']
        mix = docs_db[relevant[-1]]['mixing']
        hist = ''
        triv = ''
    cocktail = relevant[-1]
    return cocktail, desc, ing, mix, hist, triv


EXCLUDED = ['I', 'want', 'something', 'this', 'it', 'like', 'love', 'drink',
            'color']

if __name__ == '__main__':
    # define database file path below, db file should be in xml format
    process_query(sys.argv[1], sys.argv[2], sys.argv[-1])
