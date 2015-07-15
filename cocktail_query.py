#!/usr/bin/env python3
"""
This script reads cocktail database and retrieves various information from it
"""
import cocktail_ir
import ast
import os
import sys


def process_query(db, que):
    """
    This function checks if query is correct and retrieves the required info
    from the db

    INPUT:
        db  --  database full path
        que --  string that represents a tuple or a list
    """
    query = ast.literal_eval(que)
    if len(query) == 2:
        result = db.get(query[0]).get(query[-1])
        if result:
            print('')
            print(result)
            return
    else:
        result = db.get(query[0])
        if result:
            print('')
            print(result['description'])
            print(result['history'])
            print(result['ingredients'])
            print(result['mixing'])
            return
    print('Uuups, something got broken...')


def connect_db(dbfile, query):
    """
    This function uses cocktail_ir xml parser to get the db dict object
    """
    data = cocktail_ir.init_cocktails_database(dbfile)
    process_query(data, query)


if __name__ == '__main__':
    DB_FILE = os.path.join(os.getcwd(), 'cocktails.xml')
    connect_db(DB_FILE, sys.argv[1])
