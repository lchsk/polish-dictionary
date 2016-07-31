#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import pymysql.cursors

conn = pymysql.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASS"),
    db=os.getenv("DB"),
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor,
)

try:
    with conn.cursor() as cur:
        cur.execute(
            "select word from pldata where language=%s",
            (u'język polski',)
        )

        words = set()

        for row in cur.fetchall():
            words.add(row['word'])

finally:
    conn.close()

print 'Loaded {} unique words'.format(len(words))

with open('./pl_raw', 'w') as f:
    for word in sorted(words):
        f.write('{}\n'.format(word.encode('utf-8')))
