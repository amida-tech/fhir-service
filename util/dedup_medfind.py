'''
Created on Oct 16, 2019

@author: gregory
'''

def cleanup_html_lookup_file(filename):
    """
    remove duplicates from file and sort the findings into the same file

    @param: filename: the input (and output) file's name
    """
    with open(filename, 'r', encoding='utf-8') as fs:
        lines = list({item.strip().lower() for item in fs.readlines()})

    # while we are at it, let us alphabetize the entries by query
    lines.sort(key=str.lower)

    with open(filename, 'w', encoding='utf-8') as fs:
        for line in list(lines):
            # make sure end of line consistency
            fs.write(line + '\n')

if __name__ == '__main__':
    SYNONYM_FILENAME = '../data/medfind.txt'
    cleanup_html_lookup_file(SYNONYM_FILENAME)
