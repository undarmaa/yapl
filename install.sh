#!/bin/sh

python3 yapl/yapl.py \
    --db-path=yapl.sqlite\
    --wiki-titles-url=https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-all-titles.gz\
    --wiki-titles-hash=12c769accf4dbbe928562035fb8f3f45acf0e935\
    --wiki-articles-url=https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-pages-articles.xml.bz2\
    --wiki-articles-hash=ffd929d8e3a1a48ced4785cc7726a6eaca8e3a6b\
    --wiki-extracted-dir=./yapl/wikiextractor/extracted
