#!/bin/sh

python3 yapl/yapl.py \
    --db-path=test_yapl.sqlite\
    --wiki-titles-url=http://localhost/FAKE_PATH/test_wiki-all-titles.gz\
    --wiki-titles-hash=156d47b02ed9ad0ec157016f3636fd7065fd7c8e\
    --wiki-articles-url=http://localhost/FAKE_PATH/test_wiki-pages-articles.bz2\
    --wiki-articles-hash=48eb4d263d798ce1a9a79697e1c85a27afd1b2ef\
    --wiki-extracted-dir=./test_extracted

rm test_yapl.sqlite
