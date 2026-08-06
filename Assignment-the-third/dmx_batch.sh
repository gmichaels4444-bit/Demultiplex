#!/usr/bin/bash

#SBATCH --account=bgmp                    # REQUIRED: which account to use
#SBATCH --partition=bgmp                  # REQUIRED: which partition to use
#SBATCH --cpus-per-task=8                 # optional: number of cpus, default is 1
#SBATCH --mem=16GB                        # optional: amount of memory, default is 4GB per cpu

#For early testing and validation:
#/usr/bin/time -v ./demultiplex.py -ip ../TEST-input_FASTQ/ -i indexes.txt -f1 R1.test.fastq -fb R2.test.fastq -rb R3.test.fastq -f2 R4.test.fastq -op ./testruns/ -q 20
#will no longer work; code is for zipped files

#For testing on 1 million line/0.25 million record files for final validation and data analysis:
#/usr/bin/time -v ./demultiplex.py -ip ../big_tests/ -i indexes.txt -f1 1294_S1_L008_R1_001_test.fastq.gz -fb 1294_S1_L008_R2_001_test.fastq.gz -rb 1294_S1_L008_R3_001_test.fastq.gz -f2 1294_S1_L008_R4_001_test.fastq.gz -op ./testruns/ -q 10

#final run with no qscore cutoff and cutoff of 25:
/usr/bin/time -v ./demultiplex.py -ip /projects/bgmp/shared/2017_sequencing/ -i indexes.txt -f1 1294_S1_L008_R1_001.fastq.gz -fb 1294_S1_L008_R2_001.fastq.gz -rb 1294_S1_L008_R3_001.fastq.gz -f2 1294_S1_L008_R4_001.fastq.gz -op /scratch/bgmp/gmich/demux/ -q 25
/usr/bin/time -v ./demultiplex.py -ip /projects/bgmp/shared/2017_sequencing/ -i indexes.txt -f1 1294_S1_L008_R1_001.fastq.gz -fb 1294_S1_L008_R2_001.fastq.gz -rb 1294_S1_L008_R3_001.fastq.gz -f2 1294_S1_L008_R4_001.fastq.gz -op /scratch/bgmp/gmich/demux/ -q 0
