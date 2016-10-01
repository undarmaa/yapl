# Copyright 2016 Mayo Yamasaki. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0.
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# ==============================================================================
import argparse
import gzip
import hashlib
import os
import re
import urllib.request

from models import WordAndPhraseDictModel


def maybe_download(url, expected_hash):
    """Download a file from url if not present, and make sure it's sha256 hash. """
    try:
        filename = url.split('/')[-1]
    except:
        raise Exception('Failed to extract filename from url.')

    if not os.path.exists(filename):
        print('Downlod', url, '...')
        filename, _ = urllib.request.urlretrieve(url, filename)
        print('Downloded.')

    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(2048 * sha256.block_size), b''):
            sha256.update(chunk)
    checksum = sha256.hexdigest()
    if checksum == expected_hash:
        print('Found and verified', filename)
    else:
        print(checksum)
        raise Exception('Failed to verify' + filename + '. Can you check url.')
    return filename


def insert_pagetitles_to_sqlite3(filename, wp_dict):
    """Insert enwiai pagetitles into sqlite3"""
    if type(wp_dict) != WordAndPhraseDictModel:
        raise Exception('Falied to access db.')

    def is_ignore(phrase):
        # /_\(.*\)$/
        if phrase[-1] == ')' and '_(' in phrase: return False
        # /^[a-zA-z]$/
        chars = list('abcdefghijklmnopqrstuvwxyz')
        if len(phrase) == 1 and phrase in chars: return False
        # /^[0-9|!-\/:-@\[-`\{-~]*$/
        chars = set('0123456789!-/:-@[-`{~')
        if len(set(phrase).difference(chars)) == 0: return False
        # /(disambiguation)/
        if '(disambiguation)' in phrase: return False
        # /^Lists_of/
        if 'Lists_of' == phrase[:8]: return False
        return True

    def sanitize(phrase):
        return phrase.lstrip('_').rstrip('_').replace('_', ' ')

    with gzip.open(filename, 'rt', encoding='utf-8') as f:
        _ = f.readline() # pass sql table name.
        striped_phrases = map(lambda row: row.rstrip('\n').lower(), f)
        ignored_phrases = filter(is_ignore, striped_phrases)
        sanitized_phrases = map(sanitize, ignored_phrases)
        phrases = map(lambda x: (x, ), sanitized_phrases)
        return wp_dict.insert_phrases(phrases)


def main():
    parser = argparse.ArgumentParser(description='A Handler for Word And Phrae Dictonray.')
    parser.add_argument('--db-path',
                action='store',
                type=str,
                default='wp_dict.db',
                help='sqlite3 databese path.',
            )
    parser.add_argument('--wiki-titles-url',
                action='store',
                type=str,
                default='https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-all-titles.gz',
                help='wikimedia page titles url for downloading.',
            )
    parser.add_argument('--wiki-titles-hash',
                action='store',
                type=str,
                default='9d9aea6dac7d12659f08505988db9e36920c8b58cd6468b2ccf5e0605d96de5d',
                help='wikimedia page titles sha256 hash for validation.',
            )
    args = parser.parse_args()

    wp_dict = WordAndPhraseDictModel(args.db_path)
    titles_filename = maybe_download(args.wiki_titles_url, args.wiki_titles_hash)
    total_cnt = insert_pagetitles_to_sqlite3(titles_filename, wp_dict)
    print('Inserted {} enwiki pagetitle.'.format(total_cnt))
    print('done!')


if __name__ == '__main__':
    main()
