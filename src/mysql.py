#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import MySQLdb

db = MySQLdb.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    passwd=os.getenv("PASS"),
    db=os.getenv("DB"),
    charset='utf8',
)

cur = db.cursor()

cur.execute(
    "select word from pldata where language=%s",
    ('język polski',)
)

words = set()

for row in cur.fetchall():
    words.add(row[0])

with open('./pl_raw', 'w') as f:
    for word in sorted(words):
        f.write('{}\n'.format(word))

db.close()
