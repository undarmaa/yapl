# Copyright 2016 Mayo Yamasaki. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0.
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# ==============================================================================


import hashlib
import os
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


if __name__ == '__main__':
    titles_url = 'https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-all-titles.gz'
    titles_hash = '9d9aea6dac7d12659f08505988db9e36920c8b58cd6468b2ccf5e0605d96de5d'
    pages_url = 'https://dumps.wikimedia.org/enwiki/20160920/enwiki-20160920-page.sql.gz'
    pages_hash = '2f6b27c02852f3bb21b5034afdbe5e596163c216fb89971ad9ac8ca74dee592d'

    filename = maybe_download(titles_url, titles_hash)
