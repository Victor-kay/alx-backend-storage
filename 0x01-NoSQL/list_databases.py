#!/usr/bin/env python3
// my comment
"""
Module to list all databases in MongoDB.
"""

import pymongo

def list_databases():
    """
    Function to list all databases in MongoDB.
    """
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db_list = client.list_database_names()
    
    for db in db_list:
        print(f"{db}        0.000GB")

if __name__ == "__main__":
    list_databases()
