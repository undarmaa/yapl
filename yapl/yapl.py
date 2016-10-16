import argparse
import bz2
from collections import Counter, defaultdict
import gzip
import glob
import hashlib
from html.parser import HTMLParser
from itertools import chain
import math
import os
import re
import subprocess
import urllib.request

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from models import PhraseLexiconModel


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
        raise Exception('Failed to verify ' + filename + '. Can you check url.')
    return filename


def insert_pagetitles_to_lexicon(filename, lexicon):
    """Insert enwiai pagetitles into sqlite3 via lexicon model"""
    if type(lexicon) != PhraseLexiconModel:
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
        return lexicon.insert_phrases(phrases)


def insert_articles_to_lexicon(articles_filename, extracted_dir, lexicon):
    """get phrases from wikimedia articles"""
    if type(lexicon) != PhraseLexiconModel:
        raise Exception('Falied to access db.')

    # extract text from xml using wikiextractor
    cmd_to_extract_text = [
        'python3',
        './yapl/wikiextractor/WikiExtractor.py',
        articles_filename,
        '-o', extracted_dir,
        '-q'
    ]
    if not os.path.exists(extracted_dir):
        print('Extracting text from wiki xml ...')
        subprocess.call(cmd_to_extract_text)
    else:
        print('Found extracted text')

    print('Search phrase candidates ...')
    mystopwords = ',.()[]{}:;\'"+=_-^&*%$#@!~`|\\<>?/'
    sw = stopwords.words("english") + list(mystopwords)
    phrases = []
    threshold = 1000
    unigrams = Counter()
    bigrams = defaultdict(lambda :defaultdict(int))
    for articlefile in  glob.glob(extracted_dir + '/*/*'):
        with open(articlefile, 'r', encoding='utf-8') as f:
            txt = f.readlines()[1:-1] # pass <doc *> and </doc> tags.
        tokens = list(map(lambda t: t.lower(),
                          chain.from_iterable(map(word_tokenize, txt))))
        unigrams += Counter(tokens)
        for t1, t2 in zip(tokens, tokens[1:]):
            bigrams[t1][t2] += 1
    phrase_candidates = []
    count_all_tokens = sum(unigrams.values())
    for token1, subtree in bigrams.items():
        count_cond_tokens = sum(subtree.values())
        for token2, count in subtree.items():
            # pmi = log p_xy / p_x
            pmi = (count / count_cond_tokens) / (unigrams[token1] / count_all_tokens)
            if pmi >= threshold and token1 not in sw and token2 not in sw:
                phrases.append(token1 + ' ' + token2)
    return lexicon.insert_phrases(map(lambda x: (x, ), phrases))


def main():
    parser = argparse.ArgumentParser(description='A Script for Create Phrae Lexicon Databse')
    parser.add_argument('--db-path',
                action='store',
                type=str,
                help='sqlite3 databese path.',
            )
    parser.add_argument('--wiki-titles-url',
                action='store',
                type=str,
                help='wikimedia page titles url for downloading.',
            )
    parser.add_argument('--wiki-titles-hash',
                action='store',
                type=str,
                help='wikimedia page titles sha1 hash for validation.',
            )

    parser.add_argument('--wiki-articles-url',
                action='store',
                type=str,
                help='wikimedia pages articles url for downloading.',
            )
    parser.add_argument('--wiki-articles-hash',
                action='store',
                type=str,
                help='wikimedia page articles sha1 hash for validation.',
            )
    parser.add_argument('--wiki-extracted-dir',
                action='store',
                type=str,
                help='directory path of extracted xml using wikiextractor',
            )
    args = parser.parse_args()

    lexicon = PhraseLexiconModel(args.db_path)

    titles_filename = maybe_download(args.wiki_titles_url, args.wiki_titles_hash)
    print('start insertng enwiki pagetitles...')
    total_cnt = insert_pagetitles_to_lexicon(titles_filename, lexicon)

    articles_filename = maybe_download(args.wiki_articles_url, args.wiki_articles_hash)
    print('start making phrases from articles...')
    total_cnt = insert_articles_to_lexicon(articles_filename, args.wiki_extracted_dir, lexicon)

    print('inserted {} pagetitles'.format(total_cnt))
    print('done!')


if __name__ == '__main__':
    main()
