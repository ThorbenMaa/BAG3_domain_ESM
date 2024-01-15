# BAG3_domain_ESM
scripts for calculating ESM-1v LLM scores for a protein of interest and visualizing them. Input is aa sequence in fasta format. Output are plots showing esm scores. There are also scripts to analyze score distributions of CADD or esm scores in different domains.

### Clone this repository
Use `git clone https://github.com/ThorbenMaa/BAG3_domain_ESM.git`. Operate from inside the directory.

### Install dependencies
I recommend to use [mamba](https://mamba.readthedocs.io/en/latest/installation.html) to create environments and install dependencies:

```
mamba env create --name CNN_TM --file=./env/esm.yml
```

### run scripts
To calculate esm scores and plot them use:
```
python ./scripts/esm_calc.py \
--input data/input/231111_BAG3_homosapiens_uniprot_O95817_fasta.fa \
--model esm1v_t33_650M_UR90S_1 \
--model esm1v_t33_650M_UR90S_2 \
--model esm1v_t33_650M_UR90S_3 \
--model esm1v_t33_650M_UR90S_4 \
--model esm1v_t33_650M_UR90S_5 \
--output_heatmap data/output/output_heatmap_colormesh.svg \
--plttype imshow
```

To analyse ESM score distributions in different domains, use:
```
python ./scripts/stat_test_esm.py \
--input data/output/output_table.npz \
--region_pos 21-55 \
--region_pos 87-101 \
--region_pos 200-213 \
--region_pos 420-499 \
--region_name WW \
--region_name IPV#1 \
--region_name IPV#2 \
--region_name BAG \
--output_folder data/output
```

To analyse score distributions of CADD scores, you need to score the according variants using the CADD Webserver (https://cadd.bihealth.org/score) and include annotations in the output file.
This files serves as input for the following file. In The example, CADD scores have been calculated for the C-terminal part of the protein starting at amino acid position 400.
The script can be run using the following command:
```
python ./scripts/stat_test_CADD.py \
--input data/input/CADD_1_6_scores.tsv\
--region_pos 420-499 \
--region_name BAG \
--output_folder data/output/
```

Note that the corresponding data tables generated in all sscripts will also end up in the output folder as .tsv files.

