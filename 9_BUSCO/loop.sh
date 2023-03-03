#!/bin/bash

# Loop through every *_new.faa file in the directory
for file in ../7_gft2fasta_NEW/*_new.faa; do
    # Extract the base file name without the '_new.faa' suffix
    base=$(basename "$file" _new.faa)

busco -i "$file" -o "$base" -m prot -l apicomplexa -f
done
