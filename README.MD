# Case Study: The Origin of Human Malaria

Malaria is caused by parasites belonging to the phylum *Apicomplexa*. One of the more well known genera causing malaria is *Plasmodium*. The species of this genus infect not only humans, but also other mammals, birds and reptiles. The single one species that causes most malaria infections in humans is *Plasmodium falciparum*. This is also the most serious of malaria infections. Many genomes of *Plasmodium* have been sequenced. Recently the first genome of an avian (bird) malaria parasite has been sequenced. The species' name is *Haemoproteus tartakovskyi*.

The genomes we will work with are:

|   | Species                                                              | Host     | Genome                                   | Gene Prediction |  |  |
| - | -------------------------------------------------------------------- | -------- | ---------------------------------------- | --------------- | - | - |
| 1 | Plasmodium berghei                                                   | rodents  | Provided by the instructor on the server |                 |  |  |
| 2 | Plasmodium cynomolgi                                                 | macaques | Provided by the instructor on the server |                 |  |  |
| 3 | Plasmodium falciparum                                                | humans   | Provided by the instructor on the server |                 |  |  |
| 4 | Plasmodium knowlesi                                                  | lemures  | Provided by the instructor on the server |                 |  |  |
| 5 | Plasmodium vivax                                                     | humans   | Provided by the instructor on the server |                 |  |  |
| 6 | Plasmodium yoelii                                                    | rodents  | Provided by the instructor on the server |                 |  |  |
| 7 | [Haemoproteus](https://en.wikipedia.org/wiki/Haemoproteus) tartakovskyi | birds    | Provided by the instructor on the server |                 |  |  |
| 8 | Toxoplasma gondii (outgroup)                                         | humans   | Provided by the instructor on the server |                 |  |  |

## Research Questions

## Workflow

    ![img](0_Data_Script/pics/workflow.png "Workflow")

## Softwares

## 1 - Gene Prediction

### **1.1 Gene Pridiction for *Plasmodium* & *Toxoplasma* Species**

Gene prediction using GeneMark (the program name is `gmes_petap.pl` ) was performed on **Plasmodium** species' genomes. Since prediction takes time, Students were assigned one genome each, and the resulting gff-files were shared on the course server. The gff-file for Toxoplasma was downloaded from the course website under the name Tg.gff as it takes too long to run.

```

$ gmes_petap.pl --ES --sequence <seq.raw.genome>

# --ES : To run GeneMark-ES self-training algorithm
# --sequence : Input genome sequence

```

### 1.2 Gene Pridiction for *Haemoproteus tartakovskyi*

The *H. tartakovskyi* genome was sequenced by the 454 technology. Both shotgun and paired end sequencing were used. The scaffold file is found on the course server and has the name **Haemoproteus_tartakovskyi.genome**. Since the input reads *derive **both from the bird and the parasite, bird scaffolds should be removed***.

![img](0_Data_Script/pics/htGCbefore.png "GC% after removing bird scaffolds")

* GC% before removing bird scaffolds*

#### 1.2.1 Cleaning the *H. tartakovskyi* genome sequence

The GC content of *H. tartakovskyi* genome sequence is 26%. To remove scaffolds above this threshold and scaffolds that were less than 3000 nucleotides `01_Script/removeScaffold.py` was used.

```

$ python3 removeScaffold.py Haemoproteus_tartakovskyi.raw.genome 26 H_tartakovskyi.fasta 3000

# This script accept four argument:
# [1] is input fasta file name
# [2] is threshold GC content as integer
# [3] is the output file
# [4] is the minimum length for scaffolds to keep

```

We can examine the GC% after removal of birds scaffols

> Oneliner for multi line fasta to one line fasta
>
> ```
> awk '/^>/ {printf("%s%s\n",(N>0?"\n":""),$0);N++;next;} {printf("%s",$0);} END {printf("\n");}' htupper.fasta > htupper1.fasta
>
> ```
>
> Oneliner for convering fasta format to fastq
>
> ```
> $ cat H_tartakovskyi_remove.fasta | paste - - | perl -ne 'chomp; s/^>/@/; @v = split /\t/; printf("%s\n%s\n+\n%s\n", $v[0], $v[1], "B"x length($v[1]))' > fake.fastq
>
> ```
>
> Using fastqc for visualization
>
>
> ```
> $ fastqc fake.fastq 
> $ firefox fake_fastq.html
> ```

![img](0_Data_Script/pics/htGCAfter.png "GC% after removing bird scaffolds")

    GC% after removing bird scaffolds

#### 1.2.2 Gene Prediction

```

$ gmes_petap.pl --ES --sequence Data/H_tartakovskyi_remove.fasta --min_contig 3000


# --ES : To run GeneMark-ES self-training algorithm
# --sequence : Input genome sequence
# --min_contig: This specifies the minimum contig length to consider for gene prediction. Contigs shorter than this length will be ignored.

```

Now we have a gene prediction file for HT

#### 1.2.3 Creating fasta sequences from the cleaned gff file of *H. tartakovskyi*

To create fasta sequences from the gff file and the genome file use gffParse.pl found at the course server. It’s recommended that you use the -c option.

```

$ perl gffParse.pl -c -g Ht2.gff -i Data/H_tartakovskyi_remove.fasta -p -F <gff file>

```

This didn’t work!
Compare the first column in the gff-file with the headers in the genome fasta file. Do you see what is wrong? Try to adjust it, otherwise the solution is here:

```

cat Haemoproteus.gff | sed "s/ GC=.*\tGeneMark.hmm/\tGeneMark.hmm/" > Ht2.gff
# Haemoproteus.gff should be changed to the name you use for cleaned HT gff

```

Which of the two programs, in your opinion, is to blame?

```
python3 Script/datParser.py backup_results/Ht.blastout/Ht.blastp fasta/gffParse.fna Data/taxonomy.dat Data/uniprot_sprot.dat > scaffolds.txt

```
