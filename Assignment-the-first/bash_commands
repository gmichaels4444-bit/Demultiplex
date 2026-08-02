#!/usr/bin/bash

#SBATCH --account=bgmp                    # REQUIRED: which account to use
#SBATCH --partition=bgmp                  # REQUIRED: which partition to use
#SBATCH --cpus-per-task=8                 # optional: number of cpus, default is 1
#SBATCH --mem=16GB                        # optional: amount of memory, default is 4GB per cpu


# #commands for read lengths
zcat 1294_S1_L008_R1_001.fastq.gz | head -2 | tail -1 | wc
zcat 1294_S1_L008_R2_001.fastq.gz | head -2 | tail -1 | wc

# #Test commmand for counting "N" indices
# /usr/bin/time -v grep "^+" -B 1 ../TEST-input_FASTQ/R[2-3].test.fastq | grep -v "^+\n" | grep [N] | wc -l
/usr/bin/time -v zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R[2-3]_001.fastq.gz | grep "^+" -B 1 | grep -v "^+\n" | grep [N] | wc -l

#/usr/bin/time -v zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz | grep "^+" -B 1 | grep -v "^+\n" | grep [N] | wc -l
#/usr/bin/time -v zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz | grep "^+" -B 1 | grep -v "^+\n" | grep [N] | wc -l