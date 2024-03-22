#!/bin/bash
# FACoP NCBI genome download
# 2023-02

DB_DIR=/data/FACoPv2_genomes
PROGRAM_DIR=/data/FACoPv2_genomes

echo "Download latest summary files, contains all genome information\n" ;
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_refseq.txt  -O $DB_DIR/assembly_summary_refseq.txt
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/assembly_summary_genbank.txt -O $DB_DIR/assembly_summary_genbank.txt

echo "Download CheckM_report_prokaryotes.txt  \n" ;
wget ftp://ftp.ncbi.nlm.nih.gov/genomes/ASSEMBLY_REPORTS/CheckM_report_prokaryotes.txt -O $DB_DIR/CheckM_report_prokaryotes.txt


# Download Refseq
python3 $PROGRAM_DIR/02.FACoPv2_download_genomes.py -dbdir $DB_DIR -db assembly_summary_refseq.txt
# Download Genbank
python3 $PROGRAM_DIR/02.FACoPv2_download_genomes.py -dbdir $DB_DIR -db assembly_summary_genbank.txt


# Update RefSeq
python3 $PROGRAM_DIR/03.FACoPv2_annotate_genomes.py -db refseq
# Update Genabnk
python3 $PROGRAM_DIR/03.FACoPv2_annotate_genomes.py -db genbank


# check folder size: 
find $DB_DIR/refseq/  -maxdepth 1 -type d -print| wc -l
# check folder size: 
find $DB_DIR/genbank/ -maxdepth 1 -type d -print| wc -l

# list all files
ls -aR /data/FACoPv2_genomes/representative/*/*.gz | wc -l 
ls -aR /data/FACoPv2_genomes/representative/*/*.fna | wc -l 