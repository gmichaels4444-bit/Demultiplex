shebang python

import bioinfo.py as bioinfo
import argparse
	add argument: ("-i", "--index", help="index file", type=str, default="index.txt")
	add argument: ("-f1", "--file1", help="fastq_filename", type=str, default="contigs.fasta")
	add argument: ("-fb", "--fwd_bc", help="fastq_filename", type=str, default="contigs.fasta")
	add argument: ("-rb", "--rev_bc", help="fastq_filename", type=str, default="contigs.fasta")
	add argument: ("-f2", "--file2", help="fastq_filename", type=str, default="contigs.fasta")

create dictionary of indexes.txt 
indexdict={} initializing dict
	keys are barcode pairs, both matched and mismatched, and unknown
open args.index (index.txt file)
	for barcode in index:
		keyhalf=barcode
			for other_index in index
				key= append "-"other_index to keyhalf using fstring
				values are set to 0, to be counts of each key pair

create set of indexes with matched pairs, as well as "unknown" and "mismatch"
indexset=set("unknown","mismatch")
for key in indexdict:
	splitkey=split key by "-"
	if splitkey position 1== splitkey position 2:
		add key to indexset
	else:
		continue looping


define reverse_comp(sequence => string):
	reverse_complement_string=empty
	for letter in string:
		replace letter with complement in reverse_complement_string; ie
			if letter is "A"
				replace with "T" in reverse_complement_string
			if letter is "T"
				replace with "A" in reverse_complement_string
			if letter is "G"
				replace with "C" in reverse_complement_string
			if letter is "C"
				replace with "G" in reverse_complement_string
	match_string=flip the positions of reverse_complement_string
	return match_string
Input: "ATGC"
Expected output: "GCAT"

Open output files (24 fwd by barcode, 24 rev by barcode, 2 index hopped, 2 unknown barcodes (unk)) in write mode
for entry in indexset
	open file named fstring {args.file1}_{indexset entry}
	open file named fstring {args.file2}_{indexset entry}
will open an output file for each read file foe all successful pairings, a mismatch bin file, and unknown indexes


with open args.file1, args.fwd_bc, args.rv_bc, args.file2 in read mode 
	loop through all 4 fastq lines per file (While loop): use file#.readline
		Header (all 4 files)
			Only need to store for 1 file
		Sequence (all 4 files)
		Plus (all 4 files)
			do not need to store this for more than 1 file
		QScores (all 4 files)
		Reverse_comp(R3 sequence)
			If R2 or the reverse_comp of R3 is not in indexdict (ie has an "N"): 
					write all 4 lines of R1 to R1 unk file, appending R2 and reverse complemented R3 sequences to header
					write all 4 lines of R4 to R4 unk file, appending R2 and reverse complemented R3 sequences to header
					Add 1 to value of unknown in indexdict
			Else:
				if bioinfo.qualscores(R2 sequence) or bioinfo.qualscores(R3 sequence) is less than the user cutoff args.qscorecutoff
					write all 4 lines of R1 to R1 unk file, appending R2 and reverse complemented R3 sequences to header
					write all 4 lines of R4 to R4 unk file, appending R2 and reverse complemented R3 sequences to header
					Add 1 to mismatch indexdict value
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
					Add 1 to mismatch indexdict value
		if header is empty, end loop
close files


Printing counts commands:
mismatch_count=0
for key in indexdict:
	if key=="unknown" ##doing this first to avoid conflicts with splitting##
		print indexdict key and value (this will print out counts of unknown inidces)
	else: 
		splitkey=split key by "-"
		if splitkey position 1== splitkey position 2:
			print indexdict key and value (this will print out matched pairs' counts)
		else:
			add indexdict value to mismatch_count (this will sum all of the mismatched index counts together)
print mismatch_count 
