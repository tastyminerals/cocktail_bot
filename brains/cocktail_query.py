#!/usr/bin/env python3
"""
This script reads cocktail database and retrieves various information from it
"""
import argparse
import ast
import random
import re
import os
import sys
sys.path.append(os.path.join(os.getcwd(), r'brains'))
from cocktail_ir import init_cocktails_database, process_query


def prettify(message):
    """
    This function formats the message so that if would look nice in console.

    INPUT:
        string
    OUTPUT:
        list
    """
    # assuming the message contains sentence per line
    return [line.lstrip(' ') for line in message.split('\n') if line]


def tell_trivia(db):
    """
    This function returns a random trivia block for one of the cocktails.
    """
    # retrieve all trivia blocks
    trivias = dict((key, val['trivia']) for key, val in db.items() if val)
    choice = random.choice(list(trivias.keys()))
    print('"{0}".'.format(choice))
    print(prettify(trivias[choice]))
    print('\n')


def prettify(description):
    """
    This function removes empty spaces from escription string.

    INPUT:
        description -- description string coming from cocktails.xml
    OUTPUT:
        pretty -- prettified description string
    """
    single_spaces = re.compile(r'[\n]?[ ]+')
    return single_spaces.sub(' ', description)


def make_query(db, argz):
    """
    This function retrieves the required info from the db

    INPUT:
        db  --  database full path
        que --  string that represents a tuple or a list
    """
    if argz.query:
        results_tuple = process_query(argz.query, argz.analyser)
        cocktail, desc, ing, mix, hist, triv = results_tuple
        # pretty print the advise
        print('"{0}"'.format(cocktail))
        print(prettify(desc))
        print(ing)
        print(mix)
        if hist:
            print('HISTORY:')
            print(single_spaces.sub(' ', hist))
        if triv:
            print('TRIVIA:')
            print(single_spaces.sub(' ', triv))
        print('\n')


def connect_db(argz):
    """
    This function uses cocktail_ir xml parser to get the db dict object
    """
    data = init_cocktails_database(DB_FILE)
    if argz.cocktails:
        print(', '.join(data.keys()))
    elif argz.howmany:
        print(len(data), end='')
    elif argz.direct:
        try:
            print(prettify(data[argz.direct]['description']))
            print(prettify(data[argz.direct]['ingredients']))
        except KeyError:
            print("Well, I don't know anything about it. Sorry.")
    elif argz.trivia:
        tell_trivia(data)
    else:
        make_query(data, argz)


DB_FILE = os.path.join(os.getcwd(), 'cocktails.xml')


if __name__ == '__main__':
    # DB_FILE = os.path.join(os.getcwd(), 'cocktails.xml')
    prs = argparse.ArgumentParser()
    prs.add_argument('-q', '--query',
                     help='Specify you query which shall be analysed for\
                     similarity.',
                     required=False)
    prs.add_argument('-d', '--direct',
                     help='This option is to access db dict representation\
                     directly.',
                     required=False)
    prs.add_argument('-t', '--trivia', action='store_true',
                     help='Return a random trivia about one of the cocktails.',
                     required=False)
    prs.add_argument('-cocktails', '--cocktails', action='store_true',
                     help='Return all cocktails currently available.',
                     required=False)
    prs.add_argument('-howmany', '--howmany', action='store_true',
                     help='Return number of cocktails currently available.',
                     required=False)
    prs.add_argument('-a', '--analyser', default='TFIDF',
                     help='Specify which similarity analyzer to use: TFIDF or\
                     WORDNET',
                     required=False)
    arguments = prs.parse_args()
    connect_db(arguments)
