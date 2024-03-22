# FACoP
Fast Functional Annotation and Classification of Proteins of Prokaryotes

May 2023: new version FACoPv2


1) EDIT 03.FACoPv2_annotate_genomes.py

TransTermHP            = 'transterm'
TransTermHPexptermdat  = 'expterm.dat'
FACoPv2_classification = '/data/FACoPv2/04.FACoPv2_genome_classification.sh'
codon_table_file       = '/data/FACoPv2/codon_table.txt'


1) EDIT 04.FACoPv2_genome_classification.sh:

cpu=2
SCRATCHDIR=/tmp
UNIPROTDIR=/data/FACoPv2_database/databases
PROGRAMDIR=/data/FACoPv2
DIAMOND_DB=$UNIPROTDIR/uniprot_sprot.dmnd

