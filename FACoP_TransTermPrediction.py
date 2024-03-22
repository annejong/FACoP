# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 14:14:35 2023

@author: Anne

test to fast parse Fasta
"""




import pandas as pd
import re

# depending one TransTermHP
TransTermHP = '/data/software/transterm_hp_v2.09/transterm'
TransTermHPexptermdat = '/data/FACoPv2_genomes/expterm.dat'


parser = argparse.ArgumentParser(description='GSEApro databases')
parser.add_argument('-s', dest='sessiondir', help='session folder')
parser.add_argument('-fna', dest='fna', help='Fasta nucleotide filename')
parser.add_argument('-gff', dest='gff', help='GFF annotation filename')
parser.add_argument('-out', dest='outfile', help='Transterm output filename')
parser.add_argument('--version', action='version', version='Anne de Jong, version 2.0, Feb 2023')
args = parser.parse_args()



def make_ptt():
	print()


filename = 'G:\My Drive\WERK\Python\\files\\NC_014136.1.g2d.tt'
outfile  = 'G:\My Drive\WERK\Python\\files\\NC_014136.1.g2d.tt.gff'

chrom = 'NC_014136.1'

gff_header = ["chrom","db", "type", "start", "end", "name", "strand", "score", "description"]

FASTA = readMultiFasta(args.fna)

gff_term = pd.DataFrame()
header = ['Location','Strand','Length','PID','Gene','Synonym','Code','COG','Product'] 
row = pd.Series()
for key in FASTA:  # write a ptt file for each fasta entry . This is needed for the old, but good, TranstermHP
	print(key)
	# make the ptt file for TransTermHP
	ptt = pd.DataFrame()
#	ptt['Location']=GFF.loc[GFF['chrom'] == key][["start", "end"]].astype(str).apply("..".join, axis=1)
#	ptt['Strand']  =GFF.loc[GFF['chrom'] == key]['strand']
#	ptt['Length']  =GFF.loc[GFF['chrom'] == key]['end']-genes['start']
#	ptt['Gene']    =GFF.loc[GFF['chrom'] == key]['locus_tag']
#	ptt['Synonym'] =GFF.loc[GFF['chrom'] == key]['locus_tag']
	ptt['Location']='1..'+len(FASTA[key]
	ptt['Strand']  ='+'
	ptt['Length']  =''
	ptt['Gene']    ='-'
	ptt['Synonym'] ='-'
	ptt['PID']     ='-'
	ptt['Code']    ='-'
	ptt['COG']     ='-'
	ptt['Product'] ='-'
	pttfile = args.sessiondir+'/'+key+'.ptt'
	ptt.to_csv(pttfile, index = False, sep ='\t', columns = header)


	cmd = TransTermHP+ ' -p '+TransTermHPexptermdat+' '+fnafilename + ' '+pttfile;
	row = pd.Series()
	s = subprocess.run([cmd], shell=True, universal_newlines=True,capture_output=True).stdout

	for line in s.split('\n'):
		items = re.match("\s+(TERM \d+)\s+(\d+)\s+-\s+(\d+)\s+(.)\s+(.)\s+(\d+)\s+(-?\d+.?\d*)\s+(-?\d+.?\d*)", line)
		if items:
			print(key+';'+items.group(1)+';'+items.group(2)+';'+items.group(3)+';'+items.group(4)+';'+items.group(5)+';'+items.group(6)+';'+items.group(7)+';'+items.group(8))
			row['chrom'] = key
			row['db'] = 'TransTermHP'
			row['type'] = 'Terminator'
			row['start'] = items.group(2)
			row['end'] = items.group(3)
			row['name'] = '.'
			row['strand'] = items.group(4)
			row['score'] = items.group(5)
			description  = 'ID='+items.group(1).replace(" ", "_")
			description += ';locus_tag='+items.group(1).replace(" ", "_")
			row['description'] = description
			gff_term = gff_term.append(row, ignore_index=True)
gff_term.start = gff_term.start.astype(int)
gff_term.sort_values(by=['chrom','start']).to_csv(gff_term_filename, index = False, sep ='\t', columns=gff_header, header=True)

