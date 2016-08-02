#!/usr/bin/python
# -*- encoding: utf-8 -*-

import argparse

from slugify import slugify

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
    help='Generate a single file with all words (lower-case, ascii)',
)

parser.add_argument(
    '--inflections',
    action='store_true',
    help='Generate a single file with infinitives and inflections',
)

parser.add_argument(
    '--inflections_ascii',
    action='store_true',
    help='Generate a single file with infinitives and inflections '
    '(lower-case, ascii)',
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

def output_fmt(word, only_ascii=False):
    if only_ascii:
        return slugify(
            unicode(word, 'utf8'),
            lower=True,
            only_ascii=True,
            spaces=True,
        )

    return word

def generate_single_file(filename, all_words, only_ascii=False):
    """Produces a single list of words, separated by newlines."""

    output = set()

    for inf, forms in all_words.iteritems():
        output.add(output_fmt(inf, only_ascii))

        for form in forms:
            output.add(output_fmt(form, only_ascii))

    words = sorted(output)

    with open(filename, 'w') as f:
        for word in words:
            f.write('{0}\n'.format(word))

def generate_single_file_infl(filename, all_words, only_ascii=False):
    """Produces a list of entries such as:
    word=inflected_1, ..., inflected_n. """

    with open(filename, 'w') as f:
        for inf, forms in all_words.iteritems():

            forms_output = [
                output_fmt(form, only_ascii)
                for form in forms
            ]

            f.write('{inf}={forms}\n'.format(
                inf=output_fmt(inf, only_ascii),
                forms=','.join(forms_output),
            ))

def main():
    args = parser.parse_args()

    all_words = load_all(get_words())

    if args.all_words:
        generate_single_file(
            './pl_all',
            all_words,
            only_ascii=False,
        )
    elif args.all_words_ascii:
        generate_single_file(
            './pl_all_ascii',
            all_words,
            only_ascii=True,
        )
    elif args.inflections:
        generate_single_file_infl(
            './pl_infl',
            all_words,
            only_ascii=False,
        )
    elif args.inflections_ascii:
        generate_single_file_infl(
            './pl_infl_ascii',
            all_words,
            only_ascii=True,
        )

if __name__ == '__main__':
    main()
