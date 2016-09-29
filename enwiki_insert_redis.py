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
import redis
import urllib


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


def insert_pagetitles_to_redis(filename, host, port, db):
    """Insert enwiki pagetitles into redis server"""
    r = redis.StrictRedis(host=host, port=port, db=db)
    with gzip.open(filename, 'rt', encoding='utf-8') as f:
        _ = f.readline() # pass sql table name.
        for idx, row in enumerate(f):
            tokens = row.rstrip('\n')
            try:
                r.set(tokens, idx)
            except:
                raise Exception('Failed to connect Redis server.')
    return idx+1


if __name__ == '__main__':

    titles_url = 'https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-all-titles.gz'
    titles_hash = '9d9aea6dac7d12659f08505988db9e36920c8b58cd6468b2ccf5e0605d96de5d'

    redis_host = 'localhost'
    redis_port = 6379
    redis_db = 0

    titles_filename = maybe_download(titles_url, titles_hash)
    token_cnt = insert_pagetitles_to_redis(titles_filename, redis_host, redis_port, redis_db)
    print(token_cnt)
