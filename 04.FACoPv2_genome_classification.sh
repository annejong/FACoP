#!/bin/bash


cpu=2
SCRATCHDIR=/tmp
UNIPROTDIR=/data/FACoPv2_database/databases
PROGRAMDIR=/data/FACoPv2
DIAMOND_DB=$UNIPROTDIR/uniprot_sprot.dmnd
DIAMOND=/data/software/diamond/diamond/diamond

# the full path genome filename is the protein fasta name without the .faa extension. 
# The .faa will be added by DIAMOND
# e.g., /data/home/anne/PROJECTS/JanMaarten/genomes/Acinetobacter_baumannii_ATCC17978wt18_Rodrigo/Acinetobacter_baumannii_ATCC17978wt18_Rodrigo.g2d


# /data/FACoPv2/04.FACoPv2_genome_classification.sh /data/g2d_mirror_genbank/Escherichia_coli_O25b:H4-ST131_EC958/GCA_000285655.3_EC958.v1_genomic.g2d

genome=$1


function classify_genome {		
	# Add classification data to the all proteins
	python3 $PROGRAMDIR/diamond_format_results.py -diamond $genome.diamond.tab -db $UNIPROTDIR/uniprot_sprot.description -out $genome.description
	cp $genome.description $genome.FACoP.table
	python3 $PROGRAMDIR/classify_genome.py -diamond $genome.diamond.tab -db $UNIPROTDIR/uniprot_sprot.GO      -class $UNIPROTDIR/go-basic.obo.description    -out $genome.FACoP.GO
	python3 $PROGRAMDIR/classify_genome.py -diamond $genome.diamond.tab -db $UNIPROTDIR/uniprot_sprot.IPR     -class $UNIPROTDIR/IPR.description             -out $genome.FACoP.IPR
	python3 $PROGRAMDIR/classify_genome.py -diamond $genome.diamond.tab -db $UNIPROTDIR/uniprot_sprot.eggNOG  -class $UNIPROTDIR/eggNOG_COG.description      -out $genome.FACoP.eggNOG_COG
	python3 $PROGRAMDIR/classify_genome.py -diamond $genome.diamond.tab -db $UNIPROTDIR/uniprot_sprot.COG     -class $UNIPROTDIR/COG.description             -out $genome.FACoP.COG
	python3 $PROGRAMDIR/classify_genome.py -diamond $genome.diamond.tab -db $UNIPROTDIR/uniprot_sprot.PFAM    -class $UNIPROTDIR/PFAM.description            -out $genome.FACoP.Pfam
	python3 $PROGRAMDIR/classify_genome.py -diamond $genome.diamond.tab -db $UNIPROTDIR/uniprot_sprot.Keyword -class $UNIPROTDIR/KEYWORD.description         -out $genome.FACoP.KEYWORDS
	python3 $PROGRAMDIR/classify_genome.py -diamond $genome.diamond.tab -db $UNIPROTDIR/uniprot_sprot.KEGGPATHWAY -class $UNIPROTDIR/KEGGPATHWAY.description -out $genome.FACoP.KEGG
}

function check_seq {
	# to prevent errors in DIAMOND etc.. check the input
	if [ -f $genome.faa ]; then
		python3 $PROGRAMDIR/CheckFastA.py -i $genome.faa 
	fi	
}

function my_diamond_faa {
	# diamond is used to function map the proteins of the genome on the basis of the Uniprot_sprot database
	# 2 options 1 for webserver and one for G2D database
	if [ -f $genome.faa ]; then
		$DIAMOND blastp --unal 1 --threads $cpu --tmpdir $SCRATCHDIR --query $genome.faa --db $DIAMOND_DB --out $genome.diamond.tab --evalue 0.1 --max-target-seqs 1
	fi
	if [ -f $genome.g2d.faa ]; then
		$DIAMOND blastp --unal 1 --threads $cpu --tmpdir $SCRATCHDIR --query $genome.g2d.faa --db $DIAMOND_DB --out $genome.diamond.tab --evalue 0.1 --max-target-seqs 1
	fi
	
}

# =================================================================== Main =============================================================================

## the genome is the protein fasta name without the .faa extension. The .faa will be added by DIAMOND
#testing: genome=/data/p127804/GSEApro/genomes/ASM1000v1_genomic.g2d
#testing: genome=/data/g2d_mirror_genbank/Salmonella_enterica_subsp_enterica_serovar_Typhimurium_R181078.g2d

check_seq
if [ ! -f $genome.diamond.tab ]; then
	my_diamond_faa  # DIAMOND is used to find the best hit in Uniprot ==> results is $genome.diamond.tab
fi
classify_genome
