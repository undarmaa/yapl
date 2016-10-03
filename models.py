# Copyright 2016 Mayo Yamasaki. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0.
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# ==============================================================================
import os
import sqlite3


class PhraseLexiconModel():
    """A model for handling data on sqlite db."""

    def __init__(self, filename):
        isnt_exist =  not os.path.exists(filename)
        self.conn = sqlite3.connect(filename)
        if isnt_exist:
            self.create_table(filename)
            print('Created new database and define schema.')

    def create_table(self, filename):
        c = self.conn.cursor()
        schema = '''
            CREATE TABLE phrases(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phrase text
            );
        '''
        c.execute(schema)
        index = "CREATE INDEX phrase_index on phrases(phrase);"
        c.execute(index)
        print('Ccreate sqlite dabase and define table schema.')

    def insert_phrases(self, phrases):
        """Require tuple list or iter."""
        c = self.conn.cursor()
        c.executemany('INSERT INTO phrases(phrase) VALUES(?);', phrases)
        c.execute('SELECT count(id) FROM phrases;')
        return c.fetchone()[0]

    def is_phrase(self, phrase):
        """return True if arugment is phrase."""
        c = self.conn.cursor()
        sql = 'SELECT EXISTS(SELECT id FROM phrases WHERE phrase=?);'
        c.execute(sql, (phrase, ))
        return c.fetchone()[0] != 0

    def __del__(self):
        self.conn.commit()
        self.conn.close()
