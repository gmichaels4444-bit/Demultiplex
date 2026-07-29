#!/usr/bin/env python

import bioinfo
import gzip
import matplotlib as plt
import itertools
import argparse

def get_args():
	parser = argparse.ArgumentParser(description="k-mer global variables")
	parser.add_argument("-ip", "--inpath", help="input filepath", type=str, default="/projects/bgmp/gmich/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ")
	parser.add_argument("-i", "--index", help="index file", type=str, default="indexes.txt")
	parser.add_argument("-f1", "--file1", help="R1 fastq_filename", type=str, default="R1.test.fastq")
	parser.add_argument("-fb", "--fwd_bc", help="R2 fastq_filename", type=str, default="R2.test.fastq")
	parser.add_argument("-rb", "--rev_bc", help="R3 fastq_filename", type=str, default="R3.test.fastq")
	parser.add_argument("-f2", "--file2", help="R4 fastq_filename", type=str, default="R4.test.fastq")
	parser.add_argument("-op", "--outpath", help="index file", type=str, default="index.txt")
	parser.add_argument("-q", "--qcut", help="qscore cutoff", type=str, default="20")
	return parser.parse_args()
args= get_args()

def reverse_comp(sequence: str)-> str:
	'''takes Nucleic acid sequence and outputs the reverse complement'''
	complement_string=""
	reverse_complement_string=""
	bioinfo.validate_base_seq(sequence)
	for  letter in sequence:
		#replace letter with complement in reverse_complement_string; ie
		if letter == "A":
			complement_string+="T"
		if letter == "T":
			complement_string+="A"
		if letter == "G":
			complement_string+="C"
		if letter == "C":
			complement_string+="G"
		if letter == "N":
			complement_string+="N"
	reverse_complement_string = complement_string[::-1]
	return reverse_complement_string
assert reverse_comp("ATGCN")== "NGCAT"

with open(f'{args.ip}{args.index}', "r") as index: 
	for line in index:
		line.split()
	itertools.product(index[5], repeat=1)




#create dictionary from indexes.txt 
#used for counting and verifying matches
indexdict={} #initializing dict
#```keys are barcode pairs, both matched and hopped, and unknown```
with open(f'{args.ip}{args.index}', "r") as index: 
	for barcode in index:
		keyhalf=barcode
			for other_index in index:
				key= append "-"other_index to keyhalf using fstring
				if key in indexdict,
					
				values are set to 0, to be counts of each key pair








#create set of indexes with matched pairs, as well as "unknown" and "mismatch"
#Useful for naming and opening output files and counting later
indexset=set(["unknown","mismatch"]) #Initializing the set with 2 values that are not added in the flow of the loop
for key in indexdict:
	splitkey=key.split("-")
	if splitkey[1] == splitkey[2]:
		indexset+=key

#Open output files (24 fwd by barcode, 24 rev by barcode, 2 index hopped, 2 unknown barcodes (unk)) in write mode
#will open an output file for each read file foe all successful pairings, a mismatch bin file, and unknown indexes
for entry in indexset:
	open(f'{args.file1}_{entry}', "w")
	open(f'{args.file2}_{entry}, "w")



open(args.file1,"r") as fh1, open(args.fwd_bc,"r") as fbc, open(args.rv_bc,"r") as rbc, open(args.file2,"r") as fh2 
While True:
	header1=fh1.readline().strip(\n)
	headerfbc=fwd_bc.readline().strip()
	headerrbc=rv_bc.readline().strip
	header2=fh2.readline().strip

	seq1=fh1.readline().strip
	fbc_seq=fwd_bc.readline().strip
	rbc_seq=rv_bc.readline().strip
	seq2=fh2.readline().strip

	plus1=fh1.readline().strip
	plus2=fwd_bc.readline().strip
	plus3=rv_bc.readline().strip
	plus4=fh2.readline().strip

	qscore1=fh1.readline().strip
	qscore_fbc=fwd_bc.readline().strip
	qscore_rbc=rv_bc.readline().strip
	qscore2=fh2.readline()v


		header1.apppend(seq1)
		Reverse_comp(R3 sequence)
			If R2 or the reverse_comp of R3 is not in indexdict (ie has an "N"): 
					write all 4 lines of R1 to R1 unk file, appending R2 and reverse complemented R3 sequences to header
					write all 4 lines of R4 to R4 unk file, appending R2 and reverse complemented R3 sequences to header
					Add 1 to value of unknown in indexdict
			Else:
				if bioinfo.qualscores(R2 sequence) or bioinfo.qualscores(R3 sequence) is less than the user cutoff args.qscorecutoff
					write all 4 lines of R1 to R1 unk file, appending R2 and reverse complemented R3 sequences to header
					write all 4 lines of R4 to R4 unk file, appending R2 and reverse complemented R3 sequences to header
					Add 1 to unknown indexdict value
				elif R2 sequence line is identical to the reverse complement of R3 and is in indexdict keys
					add 1 to indexdict value
					write all 4 lines of R1 to R1 file for appropriate index, appending R2 and reverse complemented R3 sequences to header
					write all 4 lines of R4 to R4 file for appropriate index, appending R2 and reverse complemented R3 sequences to header
				elif R2 sequence line does not match the reverse complement of R3 and this combination is in indexdict keys
					write all 4 lines of R1 to R1 mismatch file, appending R2 and reverse complemented R3 sequences to header
					write all 4 lines of R4 to R4 mismatch file, appending R2 and reverse complemented R3 sequences to header
					Add 1 to indexdict value 
				else (only occurs if index sequences are not in barcodes)
					write all 4 lines of R1 to R1 unk file, appending R2 and reverse complemented R3 sequences to header
					write all 4 lines of R4 to R4 unk file, appending R2 and reverse complemented R3 sequences to header
					Add 1 to unknown indexdict value
		if header="":
			end


close files



Printing counts commands:
mismatch_count=0
for key in indexdict:
	if key=="unknown" ##doing this first to avoid conflicts with splitting##
		print indexdict key and value (this will print out counts of unknown inidces)
	else: 
		splitkey=split key by "-"
		if splitkey position 1 is the same as splitkey position 2:
			print indexdict key and value (this will print out matched pairs' counts)
		else:
			add indexdict value to mismatch_count (this will sum all of the hopped index counts together)
print mismatch_count (Prints count of all hopped indices collectively)

