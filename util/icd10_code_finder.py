'''
Created on Oct 16, 2019

@author: gregory
'''

from bs4 import BeautifulSoup
from time import sleep
import urllib.parse
from urllib.request import urlopen

output_dict = dict()

def ingest_output_data(output_file):
    with open(output_file, 'r', encoding='utf-8') as fs:
        lines = fs.readlines()

    for line in lines:
        parts = line.split('\t')
        condition = parts[0].lower()
        related_data = parts[0:]
        output_dict[condition] = related_data

def main(input_tsv_file, base_URL, output_tsv_file):
    ingest_output_data(input_tsv_file)
    with open(output_tsv_file, 'w', encoding='utf-8') as fs:
        for user_query in output_dict.keys():
            # let's me nice
            sleep(0.05)
            print(user_query)
            user_query_url = urllib.parse.quote(user_query)
            URL = base_URL + user_query_url
            try:
                f = urlopen(URL)
                myfile = f.read()
                soup = BeautifulSoup(myfile, 'html.parser')
                matches = soup.find_all('div', {"class": "searchPadded"})
                for match in matches:
                    # malformed html on their part, not my doing
                    if match.div is None:
                        continue
                    mchild = match.div.text
                    if mchild.lower() == user_query.lower():
                        sib = match.find_next_sibling()
                        id_code = sib.find('span', {"class": "identifier"})
                        id_text = id_code.text
                        fs.write(user_query + '\t' + id_text + '\n')
                        break
                else:
                    fs.write(user_query + '\t' + 'NO EXACT MATCH' + '\n')
                    continue
            except Exception as e:
                print(e)
                print('error')
                fs.write(user_query + '\t' + 'NO EXACT MATCH' + '\n')                   

if __name__ == '__main__':
    input_tsv_file = '../data/output.tsv'
    icd10_site = 'https://www.icd10data.com/search?s='
    output_tsv_file = '../data/output2.tsv'
    main(input_tsv_file, icd10_site, output_tsv_file)