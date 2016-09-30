# Copyright 2016 Mayo Yamasaki. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0.
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# ==============================================================================
import gzip
import hashlib
import os
import re
import urllib

from models import WordAndPhraseDictModel


def maybe_download(url, expected_hash):
    """Download a file from url if not present, and make sure it's sha256 hash. """
    try:
        filename = url.split('/')[-1]
    except:
        raise Exception('Failed to extract filename from url.')

    if not os.path.exists(filename):
        filename, _ = urllib.request.urlretrieve(url, filename)

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

    ignore_pattern = (
        re.compile('_\(.*\)$'),
        re.compile('^[a-zA-z0-9|!-\/:-@\[-`\{-~]*$'),
        re.compile('(disambiguation)'),
        re.compile('^Lists_of'),
    )

    replace_pattern = (
        (re.compile('^_|_$|,'), ''),
        (re.compile('_'), ' '),
    )

    def is_ignore(phrase):
        for ptn in ignore_pattern:
            if ptn.match(phrase):
                return False
        return True

    def sanitize(phrase):
        for ptn, repl in replace_pattern:
            phrase =  ptn.sub(repl, phrase)
        return phrase

    with gzip.open(filename, 'rt', encoding='utf-8') as f:
        _ = f.readline() # pass sql table name.
        striped_phrases = map(lambda row: row.rstrip('\n'), f)
        ignored_phrases = filter(is_ignore, striped_phrases)
        sanitized_phrases = map(sanitize, ignored_phrases)
        phrases = map(lambda x: (x, ), sanitized_phrases)
        return wp_dict.insert_phrases(phrases)


if __name__ == '__main__':

    titles_url = 'https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-all-titles.gz'
    titles_hash = '9d9aea6dac7d12659f08505988db9e36920c8b58cd6468b2ccf5e0605d96de5d'

    sqlite3_filename = 'wp_dict.db'
    wp_dict = WordAndPhraseDictModel(sqlite3_filename)
    titles_filename = maybe_download(titles_url, titles_hash)
    total_cnt = insert_pagetitles_to_sqlite3(titles_filename, wp_dict)
    print('Inserted {} enwiki pagetitle.'.format(total_cnt))
    print('done!')
