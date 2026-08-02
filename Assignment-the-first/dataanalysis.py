#!/usr/bin/env python

import gzip
import bioinfo
import argparse
def get_args():
	parser = argparse.ArgumentParser(description="demux global variables")
	parser.add_argument("-i", "--inpath", help="input filepath", type=str, default="/projects/bgmp/shared/2017_sequencing/")
	parser.add_argument("-f", "--file", help="fastq_filename", type=str, default="R1.test.fastq")
	parser.add_argument("-l", "--length", help="readlength of file", type=int, default="101")
	parser.add_argument("-o", "--outname", help="output file name", type=str, default="test.png")
	return parser.parse_args()
args= get_args()

file=f'{args.inpath}{args.file}'

def init_list(lst: list, value: float=0.0) -> list:
    '''This function takes an empty list and will populate it with
    the value passed in "value". If no value is passed, initializes list
    with 101 values of 0.0.''' 
    for i in range(args.length):
        lst.append(value)
    return lst

my_list: list = []
my_list = init_list(my_list)

def populate_list(file: str) -> tuple[list, int]:
    my_list = init_list([])
    with gzip.open(file,"rt") as f: 
    #with open(file,"rt") as f: ##only used for testing on unzipped files
        i=0
        for line in f:
            i+=1
            line=line.strip('\n')
            if i%4 == 0:
                # print(line)
                for position, score in enumerate(line): 
                    score=bioinfo.convert_phred(score)
                    my_list[position]+=score 
        return my_list, i


my_list, num_lines=populate_list(file)

for i, q_sum in enumerate(my_list):
    my_list[i]=(my_list[i])/(num_lines/4)
    # print(f"{i}\t{my_list[i]}", file=args.tsv)


import matplotlib.pyplot as plt
x= range(len(my_list))
y= my_list
plt.bar(x,y)
plt.title(f'{args.outname} Mean Quality Score vs Base Position')
plt.xlabel('Base Position')
plt.ylabel('Mean Quality Score')
plt.savefig(f'{args.outname}.png')