'''
Created on Oct 16, 2019

@author: gregory
'''

def cleanup_html_lookup_file(filename):
    with open(filename, 'r', encoding='utf-8') as fs:
        lines = list(set(fs.readlines()))
    
    # while we are at it, let us alphabetize the entries by query
    lines.sort(key=str.lower)
    
    with open(filename, 'w', encoding='utf-8') as fs:
        for line in list(lines):
            fs.write(line)

if __name__ == '__main__':
    synonym_file = '../data/medfind.txt'
    cleanup_html_lookup_file(synonym_file)