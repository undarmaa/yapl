#!/bin/sh

python3 yapl/yapl.py \
    --db-path=test_yapl.sqlite\
    --wiki-titles-url=http://localhost/FAKE_PATH/test_wiki-all-titles.bz2\
    --wiki-titles-hash=66d2c1d26e370c17813366485458bda963679903\
    --wiki-articles-url=http://localhost/FAKE_PATH/test_wiki-pages-articles.bz2\
    --wiki-articles-hash=854629513cfab3dc758f265528269f9507c74b48\
    --wiki-extracted-dir=./test_extracted

