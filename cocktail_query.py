#!/usr/bin/env python3
"""
This script reads cocktail database and retrieves various information from it
"""
import cocktail_ir
import argparse
import ast
import random
import os
import sys


def get_trivia(db):
    """
    This function returns a random trivia block for one of the cocktails.    
    """
    # retrieve all trivia blocks
    trivias = dict((key, val['trivia']) for key, val in db.items())
    choice = random.choice(list(trivias.keys()))
    print('>>>', choice, '<<<')
    print(trivias[choice])
    

def process_query(db, argz):
    """
    This function retrieves the required info from the db

    INPUT:
        db  --  database full path
        que --  string that represents a tuple or a list
    """
    if argz.query:
        cocktail_ir.process_query(argz.query)
    elif argz.trivia:
        get_trivia(db)
    elif argz.direct:
        dquery = ast.literal_eval(argz.direct)
        result = db.get(dquery[0]).get(dquery[-1])
        if result:
            print('\n')
            print(result)
            return
        else:
            print("Can't find what you want, hmm...")
        

def connect_db(dbfile, query):
    """
    This function uses cocktail_ir xml parser to get the db dict object
    """
    data = cocktail_ir.init_cocktails_database(dbfile)
    process_query(data, query)


if __name__ == '__main__':
    DB_FILE = os.path.join(os.getcwd(), 'cocktails.xml')
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
    arguments = prs.parse_args()
    connect_db(DB_FILE, arguments)
