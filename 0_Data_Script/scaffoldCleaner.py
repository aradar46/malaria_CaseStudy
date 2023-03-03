#!/usr/bin/python3
# %%
import sys
'''
This script takes 3 arguments:
    1. file with list of scaffolds to be removed
    2. fasta file
    3. output file name
    
usage: python3 scaffoldCleaner.py scaffold_list.txt input.fasta outputname

'''

file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]
if len(sys.argv) < 4:
    print('Please provide 3 arguments: 1. list of scaffolds to be removed 2. fasta file 3. output file')
    sys.exit()


# scaffold list to be removed
scaffolds = []
fasta = {}

# open files to read and write
with open(file1, 'r') as f1:
    with open(file2, 'r') as f2:
        with open(file3, 'w') as f3:

            # read scaffold file and store in list
            for line in f1:
                scaffolds.append(line.strip())

            # reading fasta file and store in dictionary
            for q in f2:
                if q.startswith('>'):
                    key = q.strip()
                    fasta[key] = ''
                else:
                    fasta[key] += q.strip()

            # check if scaffold is in scaffold list and write to file3
            for key, value in fasta.items():
                if key.split('scaffold=')[1].split()[0] not in scaffolds:
                    # write the key and value to file3
                    f3.write(key + '\n' + value + '\n')
