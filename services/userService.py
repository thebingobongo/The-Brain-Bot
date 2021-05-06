# user_service.py
import os

import psycopg2

from dotenv import load_dotenv
load_dotenv()

def add_user(user_information=None):
    conn = get_connexion()
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute()
    # connection usage
    finally:
        conn.close()
    db = database.connect()
    db.insert(user_information)

def update_user(user_information=None):
    db = database.connect()
    db.update(user_information["user_id"], user_information)
    # this is a test

def delete_user(user_id=None):
    db = database.connect()
    db.delete(user_id)


def get_connexion():
    return psycopg2.connect(os.getenv('DATABASECONNEXIONSTRING'))
