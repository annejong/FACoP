"""
Anne de Jong
2023 Feb

python3 /data/FACoPv2_genomes/02.FACoPv2_download_genomes.py -dbdir /data/FACoPv2_genomes -db refseq


"""

import sys
import pandas as pd
import argparse 
import subprocess
import os


parser = argparse.ArgumentParser(description='GSEApro databases')
parser.add_argument('-db', dest='db', help='refseq or genbank')
parser.add_argument('-dbdir', dest='dbdir', help='folder for database')
parser.add_argument('--version', action='version', version='Anne de Jong, version 2.0, Feb 2023')
args = parser.parse_args()

# 1. Read NCBI assembly_summary file
print("Reading summary file")
colNames=["assembly_accession","bioproject","biosample","wgs_master"       \
,"refseq_category","taxid","species_taxid","organism_name"                 \
,"infraspecific_name","isolate","version_status","assembly_level"          \
,"release_type","genome_rep","seq_rel_date","asm_name"                     \
,"submitter","gbrs_paired_asm","paired_asm_comp","ftp_path"                \
,"excluded_from_refseq","relation_to_type_material","asm_not_live_date"]

summary = pd.read_csv(args.dbdir+'/assembly_summary_'+args.db+'.txt',sep='\t', comment='#', names=colNames)
print("\tEntries in Summary="+str(summary.shape[0]))



# 2. Read CheckM_report_prokaryotes
print("Reading CheckM_report_prokaryotes file")
colNames=["genbank-accession","refseq-accession","taxid","species-taxid","organism-name","species-name","assembly-name","checkm-completeness","checkm-contamination","checkm-marker-set"]
CheckM = pd.read_csv(args.dbdir+'/CheckM_report_prokaryotes.txt',sep='\t', comment='#', names=colNames)
print("\tEntries in CheckM="+str(CheckM.shape[0]))




# 2. Filter on complete genomes only
#SelectedGenomes = summary[summary['assembly_level']=="Complete Genome"]
#print("Entries in Complete Genome="+str(SelectedGenomes.shape[0]))
#
#SelectedGenomes = summary[summary['refseq_category']=="reference genome"]
#print("Entries in reference genome="+str(SelectedGenomes.shape[0]))

SelectedGenomes = summary[ (summary['refseq_category']=="representative genome") & (summary['assembly_level']=="Complete Genome") ]
print("\tEntries in representative genome="+str(SelectedGenomes.shape[0]))

# Use CheckM to select Prokaryotes only
ProkaryoteGenomes = pd.merge(CheckM, SelectedGenomes, left_on='refseq-accession', right_on='assembly_accession', how='inner')

print("Entries in Prokaryote Genomes="+str(ProkaryoteGenomes.shape[0]))




unwanted = "'[]/+.!@#$;:!*%)(&^~="
for index, row in ProkaryoteGenomes.iterrows():

	if (pd.isna(row['ftp_path']) == False): # Check if FTP link exists
		# 3. Create a Human readable strain name
		Strain=''
		if (pd.isna(row['infraspecific_name']) == False): 
			Strain=row['infraspecific_name'].replace('strain=','')
			if (Strain in row['organism_name']) : Strain='';
		GenomeName=row['organism_name'] + '_' + Strain + '_' +row['asm_name'] 
		GenomeName=GenomeName.replace(' ','_')
		GenomeName = ''.join( c for c in GenomeName if c not in unwanted )

		# 4. Create Genome Folder
		#folder=args.dbdir + '/' + args.db + '/' +GenomeName
		folder=args.dbdir + '/representative/' +GenomeName
		if os.path.isfile(folder+'/G2D.genome_info.txt'):
			print('GenomeName exists  = '+GenomeName)
		else:	
			print('GenomeName download= '+GenomeName)
			print("\t\t"+row['ftp_path'])
			cmd = "mkdir "+folder
			s = subprocess.run([cmd], shell=True, universal_newlines=True,capture_output=True).stdout
			row.to_csv(folder+'/G2D.genome_info.txt', sep ='\t')
			#extensions=["_genomic.gff.gz","_genomic.gbff.gz","_genomic.fna.gz","_protein.faa.gz"]
			extensions=["_genomic.fna.gz"]
			ftpName=row['assembly_accession']+'_'+row['asm_name']  # Nomenclature of NCBI
			
			for extension in extensions:  # download all extensions
				ftp=row['ftp_path'] + '/' + ftpName + extension
				cmd = "wget " + ftp + " -O "+folder+'/'+GenomeName+extension
				s = subprocess.run([cmd], shell=True, universal_newlines=True,capture_output=True).stdout







