#!/usr/bin/env python

import bioinfo
import gzip
import itertools
import argparse
import matplotlib.pyplot as plt

def get_args():
	parser = argparse.ArgumentParser(description="k-mer global variables")
	parser.add_argument("-ip", "--inpath", help="input filepath", type=str, default="/projects/bgmp/gmich/bioinfo/Bi622/Demultiplex/TEST-input_FASTQ/")
	parser.add_argument("-i", "--index", help="index file", type=str, default="indexes.txt")
	parser.add_argument("-f1", "--file1", help="R1 fastq_filename", type=str, default="R1.test.fastq")
	parser.add_argument("-fb", "--fwd_bc", help="R2 fastq_filename", type=str, default="R2.test.fastq")
	parser.add_argument("-rb", "--rev_bc", help="R3 fastq_filename", type=str, default="R3.test.fastq")
	parser.add_argument("-f2", "--file2", help="R4 fastq_filename", type=str, default="R4.test.fastq")
	parser.add_argument("-op", "--outpath", help="output filepath", type=str, default="./testruns/")
	parser.add_argument("-q", "--qcut", help="qscore cutoff", type=int, default="0") #optional
	return parser.parse_args()
args= get_args()

def reverse_comp(sequence: str)-> str:
	'''takes Nucleic acid sequence and outputs the reverse complement'''
	complement_string=""
	reverse_complement_string=""
	# bioinfo.validate_base_seq(sequence)
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
# if __name__ == "__main__":
# 	assert reverse_comp("ATGCN") == "NGCAT"
# 	print("reverse_comp works")

def read_record(fh: list)->list:
	####not used in this script, for future use###
	'''function for looping over a fastq file within a while True loop'''
	record=[]
	for i in range(4):
		record.append(fh.readline().strip("\n"))
	return record

# #create dictionary from indexes.txt 
# #used for counting and verifying matches
barcodes=[]
with open(f'{args.inpath}{args.index}', "r") as index: 
	for line in index:
		line=line.strip("\n")
		splitline=line.split("\t")
		if "index" not in splitline:
			barcodes.append(str(splitline[4]))

indexdict={"unknown": 0} #initializing dict
for pair in itertools.product(barcodes, repeat=2):
	dashpair=f'{pair[0]}-{pair[1]}'
	indexdict[dashpair]=0
#print(indexdict)
#```keys are barcode pairs writen as "barcode1-barcode2", both matched and hopped, and unknown```

#create set of filehandles with matched pairs, as well as "unknown" and "hopped"
#Useful for naming and opening output files and counting later
#```keys are barcode pairs writen as "barcode1-barcode2", MATCHED ONLY, hopped bin, and unknown bin```
filedict={"unknown":[open(f'{args.outpath}unknown_R1.fastq',"w"),open(f'{args.outpath}unknown_R2.fastq',"w")],"hopped":[open(f'{args.outpath}hopped_R1.fastq',"w"),open(f'{args.outpath}hopped_R2.fastq',"w")]}		#Initializing the dict with 2 values that are not added in the flow of the loop
for barcode in barcodes:
	filedict[barcode]=[open(f'{args.outpath}{barcode}-{barcode}_R1.fastq',"w"),open(f'{args.outpath}{barcode}-{barcode}_R2.fastq',"w")]
#Open output files (24 fwd by barcode, 24 rev by barcode, 2 index hopped, 2 unknown barcodes (unk)) in write mode
#will open an output file for each read file for all successful pairings, a hopped bin file, and unknown indices

### good to here###
totalrecs=0
with gzip.open(f'{args.inpath}{args.file1}',"rt") as fh1, gzip.open(f'{args.inpath}{args.fwd_bc}',"rt") as fbc, gzip.open(f'{args.inpath}{args.rev_bc}',"rt") as rbc, gzip.open(f'{args.inpath}{args.file2}',"rt") as fh2:
	while True:
		header1=fh1.readline().strip('\n')
		headerfbc=fbc.readline().strip('\n')
		headerrbc=rbc.readline().strip('\n')
		header2=fh2.readline().strip('\n')

		seq1=fh1.readline().strip('\n')
		seq_fbc=fbc.readline().strip('\n')
		seq_rbc=rbc.readline().strip('\n')
		seq2=fh2.readline().strip('\n')

		plus1=fh1.readline().strip('\n')
		plus2=fbc.readline().strip('\n')
		plus3=rbc.readline().strip('\n')
		plus4=fh2.readline().strip('\n')

		qscore1=fh1.readline().strip('\n')
		qscore_fbc=fbc.readline().strip('\n')
		qscore_rbc=rbc.readline().strip('\n')
		qscore2=fh2.readline().strip('\n')
		if header1=="":
			break
		bcpair=f'{seq_fbc}-{reverse_comp(seq_rbc)}'
		R1outheader=f'{header1}_{bcpair}'
		R2outheader=f'{header2}_{bcpair}'
		#appending barcode pair to each header before identifying file to write to
		if bcpair not in indexdict: #ie Ns or incorrect reads present
				filedict["unknown"][0].write(f'{R1outheader}\n{seq1}\n{plus1}\n{qscore1}')
				filedict["unknown"][1].write(f'{R2outheader}\n{seq2}\n{plus4}\n{qscore2}')
				indexdict["unknown"]+=1
				totalrecs+=1
		else:
			totalrecs+=1
			written=False
			for pos, base in enumerate(qscore_fbc):
				if bioinfo.convert_phred(base)<args.qcut or bioinfo.convert_phred(qscore_fbc[pos])<args.qcut:
					filedict["unknown"][0].write(f'{R1outheader}\n{seq1}\n{plus1}\n{qscore1}')
					filedict["unknown"][1].write(f'{R2outheader}\n{seq2}\n{plus4}\n{qscore2}')
					indexdict["unknown"]+=1
					written=True
					break
			if not written:
				if seq_fbc==reverse_comp(seq_rbc):
					filedict[seq_fbc][0].write(f'{R1outheader}\n{seq1}\n{plus1}\n{qscore1}')
					filedict[seq_fbc][1].write(f'{R2outheader}\n{seq2}\n{plus4}\n{qscore2}')
					indexdict[bcpair]+=1
				elif seq_fbc!=reverse_comp(seq_rbc):
					filedict["hopped"][0].write(f'{R1outheader}\n{seq1}\n{plus1}\n{qscore1}')
					filedict["hopped"][1].write(f'{R2outheader}\n{seq2}\n{plus4}\n{qscore2}')
					indexdict[bcpair]+=1

for barcode in filedict:
	filedict[barcode][0].close()
	filedict[barcode][1].close()

statsdict={"Hopped":0}
match_count=0
#will only have counts for matched index, hopped bin, and unknown bin
with open(f'Demultiplex_stats_cutoff={args.qcut}.tsv', "w") as stats:
	print(f'Index Pair\tPair Condition\tCount\tMatched Percent', file=stats)
	for bcpair in indexdict:
		if bcpair=="unknown":
			print(f'{bcpair}\tUnknown\t{indexdict[bcpair]}\t{100*indexdict[bcpair]/totalrecs}', file=stats)
			statsdict["Unknown"]=indexdict["unknown"]
		else:
			barcodes=bcpair.split("-")
			if barcodes[0]==barcodes[1]:
				match_count+=indexdict[bcpair]
				statsdict[barcodes[0]]=indexdict[bcpair]
				print(f'{bcpair}\tMatched\t{indexdict[bcpair]}\t{100*indexdict[bcpair]/totalrecs}', file=stats)
			else:
				statsdict["Hopped"]+=indexdict[bcpair]
				print(f'{bcpair}\tHopped\t{indexdict[bcpair]}\t{100*indexdict[bcpair]/totalrecs}', file=stats)
	print(f'Matched Reads\t{match_count}\nHopped Reads\t{statsdict["Hopped"]}\nUnknown Reads\t{statsdict["Unknown"]}', file=stats)

#pie chart of matched, hopped, and unknown
plt.figure(1)
plt.title(f'Percentages by Condition with Cutoff of {args.qcut}')
labels = 'Matched', 'Hopped', 'Unknown'
sizes = [match_count, statsdict["Hopped"],statsdict["Unknown"]]
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.savefig(f'Demultiplex_bin_percents_cutoff={args.qcut}.png')
plt.close(f'Demultiplex_bin_percents_cutoff={args.qcut}.png')

#bar chart of read counts by matched pair, hopped, and unknown
plt.figure(2)
plt.bar(list(statsdict.keys()),list(statsdict.values()))
plt.title(f'Number of Reads by Index Pair with Cutoff of {args.qcut}')
plt.xlabel('Matched Index')
plt.ylabel('Count')
plt.xticks(fontsize=12, rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'Demultiplex_counts_cutoff={args.qcut}.png')
plt.close(f'Demultiplex_counts_cutoff={args.qcut}.png')

#bar chart of read percentages by matched pair, hopped, and unknown
plt.figure(3)
plt.bar(list(statsdict.keys()),list(100*(value/totalrecs) for value in statsdict.values()))
plt.title(f'Percent of Reads by Index Pair with Cutoff of {args.qcut}')
plt.xlabel('Matched Index')
plt.ylabel('Percent of Reads')
plt.xticks(fontsize=12, rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'Demultiplex_percents_cutoff={args.qcut}.png')
plt.close(f'Demultiplex_percents_cutoff={args.qcut}.png')