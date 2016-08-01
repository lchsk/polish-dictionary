#!/usr/bin/python
# -*- encoding: utf-8 -*-

import urllib2
import os
import re

from bs4 import BeautifulSoup

OMIT = [u'–', u'-']
URL = 'https://pl.wiktionary.org/wiki/'

re_no_brackets = re.compile(r'\[.*?\]')
re_no_parens = re.compile(r'\(.*?\)')

def clean_word(word):
    to_remove = ['\t', '\n', '\r']

    for remove in to_remove:
        word = word.replace(remove, '')

    word = word.replace('/', '_')

    return word

def remove_within_brackets(string):
    string = re.sub(re_no_brackets, '', string)
    string = re.sub(re_no_parens, '', string)

    return string

def load_web_soup(word):
    return BeautifulSoup(
        urllib2.urlopen('{0}{1}'.format(URL, word)),
        'html.parser',
    )

def parse(soup):
    tables = soup.find_all(
        'table',
        {'class':['wikitable', 'odmiana']}
    )

    forms = set()

    for table in tables:
        tds = table.find_all('td')

        for td in tds:
            if (
                not td.find('tr') and
                not td.find('th') and
                'forma' not in td.attrs.get('class', [])
            ):
                words = td.text.replace('\n', '').split(',')

                for word in words:
                    if word not in OMIT:
                        forms.add(word.strip())

    return forms

def save(word, forms):
    with open('../tmp/{}'.format(word), 'w') as f:
        for form in forms:
            f.write('{}\n'.format(form.encode('utf8')))

def main():
    words = []

    print 'Loading raw file'

    with open('../db/pl_raw') as f:
        for line in f:
            words.append(line)

    n_words = len(words)

    print 'Loaded %s words' % n_words

    for i, word in enumerate(words):
        word = clean_word(word)

        if os.path.exists('../tmp/{0}'.format(word)):
            print '%s already exists, skip' % word
            continue

        print 'Word %s/%s (%.4f%%). Downloading %s' % (
            i,
            n_words,
            round(i / n_words, 4),
            word,
        )

        try:
            soup = load_web_soup(word)
        except urllib2.HTTPError as e:
            print 'Could not find %s' % word
            continue

        print 'Downloaded %s' % word

        forms = parse(soup)

        save(word, forms)

        print '%s saved' % word

if __name__ == '__main__':
    main()
