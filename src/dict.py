#!/usr/bin/python
# -*- encoding: utf-8 -*-

import argparse

from scrape.scrape import (
    clean_word,
    remove_within_brackets,
)

parser = argparse.ArgumentParser()

parser.add_argument(
    '--all_words',
    action='store_true',
    help='Generate a single file with all words',
)

parser.add_argument(
    '--all_words_ascii',
    action='store_true',
    help='Generate a single file with all words (ascii)',
)

def get_words():
    words = []

    with open('./db/pl_raw') as f:
        for line in f:
            words.append(line)

    return words

def prepare_word(word):
    return remove_within_brackets(word).strip()

def load_all(words):
    all_words = {}

    for word in words:
        word_p = prepare_word(word)
        all_words[word_p] = set()

        try:
            with open('./tmp/{0}'.format(clean_word(word))) as f:
                for line in f:
                    line_p = prepare_word(line)

                    if line_p:
                        if '/' in line_p:
                            line_p_arr = line_p.split('/')
                            all_words[word_p].add(line_p_arr[0])
                            all_words[word_p].add(line_p_arr[1])
                        else:
                            all_words[word_p].add(line_p)
        except IOError as e:
            print '%s' % e

    print 'Infinitives: %s' % len(all_words)
    print 'Forms: %s' % sum(
        1
        for forms in all_words.values()
        for f in forms
    )

    return all_words

def generate_single_file(all_words, ascii=False):
    output = set()

    for inf, forms in all_words.iteritems():
        output.add(inf)

        for form in forms:
            output.add(form)

    words = sorted(output)

    with open('./pl_all', 'w') as f:
        for word in words:
            f.write('{0}\n'.format(word))

def main():
    args = parser.parse_args()

    if args.all_words:
        all_words = load_all(get_words())
        generate_single_file(all_words)

if __name__ == '__main__':
    main()
