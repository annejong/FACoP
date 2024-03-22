#!/bin/bash

SESSIONDIR=$1
MakeGFF=$2
PROGRAMDIR=/data/FACoPv2


# check code injection
COUNT1=`grep -rnw $SESSIONDIR -e '\?php' | wc -l `
COUNT2=`grep -rnw $SESSIONDIR -e '\?PHP' | wc -l `
if ( (($COUNT1+$COUNT2)) > 0)
then
	echo 'PHP code injection detected'
	echo 'PHP code injection detected' > $SESSIONDIR/00.ppp.log
	exit 1
else
	echo 'clean files'
fi	
 

# Use Prodigal to make a GFF file
if [ "$MakeGFF" = "true" ]; then
	# Call Prodigal
	prodigal -p meta -f gff -i $SESSIONDIR/query.fna | sed 's/ID=/locus_tag=prodigal_/'  | sed 's/CDS\s/gene	/' | sed 's/\"/#/g' > $SESSIONDIR/query.gff
fi


# Genome2d Formatting and Annotation
python3 $PROGRAMDIR/03.FACoPv2_annotate_genomes.py -dbdir $SESSIONDIR -webserver true

echo ls > $SESSIONDIR/sessionfiles.txt
