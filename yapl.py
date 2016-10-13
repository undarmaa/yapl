import argparse
import bz2
from collections import Counter, defaultdict
import gzip
import glob
import hashlib
from html.parser import HTMLParser
from models import PhraseLexiconModel
from nltk.tokenize import word_tokenize
import os
import re
import subprocess
import urllib.request


def maybe_download(url, expected_hash):
    """Download a file from url if not present, and make sure it's sha1 hash. """
    try:
        filename = url.split('/')[-1]
    except:
        raise Exception('Failed to extract filename from url.')

    if not os.path.exists(filename):
        print('Downlod', url, '...')
        filename, _ = urllib.request.urlretrieve(url, filename)
        print('Downloded.')

    sha1 = hashlib.sha1()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(2048 * sha1.block_size), b''):
            sha1.update(chunk)
    checksum = sha1.hexdigest()
    if checksum == expected_hash:
        print('Found and verified', filename)
    else:
        print(checksum)
        raise Exception('Failed to verify' + filename + '. Can you check url.')
    return filename


def insert_pagetitles_to_sqlite3(filename, wp_dict):
    """Insert enwiai pagetitles into sqlite3"""
    if type(wp_dict) != PhraseLexiconModel:
        raise Exception('Falied to access db.')

    def isnt_ignore(phrase):
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
        ignored_phrases = filter(isnt_ignore, striped_phrases)
        sanitized_phrases = map(sanitize, ignored_phrases)
        phrases = map(lambda x: (x, ), sanitized_phrases)
        return wp_dict.insert_phrases(phrases)


def make_phrase_candidate(articles_filename):
    TXTS_DIR = 'wikiextractor/extracted'
    # extract text from xml using wikiextractor
    cmd_to_extract_text = [
        'python3',
        'wikiextractor/WikiExtractor.py',
        './enwiki-20160920-pages-articles.xml.bz2',
        '-c',
        '-o', 'this', #TODO
        '-q'
    ]
    print('Extracting text from wiki xml ...')
    #subprocess.call(cmd_to_extract_text) TODO

    unigrams = Counter()
    bigrams = defaultdict(lambda :defaultdict(int))
    print('Search phrase candidates ...')
    for articlefile in  glob.glob('./wikiextractor/extracted/*/*.bz2'):
        print(articlefile)
        with gzip.open(articlefile, 'rt', encoding='utf-8') as f:
            txt = f.readlines()[1:-1] # pass <doc *> and </doc> tags.
        tokens = word_tokenize(txt)
        unigrams += Counter(tokens)
        for t1, t2 in zip(tokens, tokens[1:]):
            bigrams[t1][t2] += 1


def main():
    parser = argparse.ArgumentParser(description='A Handler for Word And Phrae Dictonray.')
    parser.add_argument('--db-path',
                action='store',
                type=str,
                default='yapl.sqlite',
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
                default='12c769accf4dbbe928562035fb8f3f45acf0e935',
                help='wikimedia page titles sha1 hash for validation.',
            )

    parser.add_argument('--wiki-articles-url',
                action='store',
                type=str,
                default='https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-pages-articles.xml.bz2',
                help='wikimedia pages articles url for downloading.',
            )
    parser.add_argument('--wiki-articles-hash',
                action='store',
                type=str,
                default='ffd929d8e3a1a48ced4785cc7726a6eaca8e3a6b',
                help='wikimedia page articles sha1 hash for validation.',
            )
    args = parser.parse_args()

    lexicon = PhraseLexiconModel(args.db_path)

    #titles_filename = maybe_download(args.wiki_titles_url, args.wiki_titles_hash)
    #total_cnt = insert_pagetitles_to_sqlite3(titles_filename, lexicon)
    #print('Inserted {} enwiki pagetitle.'.format(total_cnt))

    articles_filename = maybe_download(args.wiki_articles_url, args.wiki_articles_hash)
    make_phrase_candidate(articles_filename)

    print('done!')


if __name__ == '__main__':
    main()
