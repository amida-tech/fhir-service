'''
Created on Nov 18, 2019

@author: gregory
'''

import os
from shutil import copyfile

from util import dedup_medfind

def test_cleanup_html_lookup_file():
    """
    test the cleanup_html_lookup_file to make sure duplicates are removed correctly
    """
    # there are 4 duplicate entries, all having to do with stroke
    expected_lines = 63

    #original location
    test_filename = 'test/fixture/html_lookup_file.txt'
    #create a copy to maintain integrity of file
    test_filename_working = 'test/fixture/html_lookup_file_copy.txt'
    copyfile(test_filename, test_filename_working)

    dedup_medfind.cleanup_html_lookup_file(test_filename_working)
    # no return value, we must open and read the file to assert
    with open(test_filename_working, 'r', encoding='utf-8') as fs:
        lines = fs.readlines()
    # delete our working copy before performing asserts
    os.remove(test_filename_working)
    # finally, we do our asserts based upon the test file we create
    for line in lines:
        print(line.strip())
    assert expected_lines == len(lines)
