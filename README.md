# BAG3_domain_ESM
scripts for calculating ESM-1v LLM scores for a protein of interest and visualizing them. Input is aa sequence in fasta format. Output are plots showing esm scores.

### Clone this repository
Use `git clone https://github.com/ThorbenMaa/BAG3_domain_ESM.git`. Operate from inside the directory.

### Install dependencies
I recommend to use [mamba](https://mamba.readthedocs.io/en/latest/installation.html) to create environments and install dependencies:

```
mamba env create --name CNN_TM --file=./env/esm.yml
```

### run scripts
There are 2 scripts doing more or less the same thing. The only difference is that by using `esm_calc_colormesh_instead_of_imshow.py` the output svg file is more editable in subsequent graphoc proccesing prgrams such as inkscape. Use either:
```
python ./scripts/esm_calc_colormesh_instead_of_imshow.py \
--input data/input/231111_BAG3_homosapiens_uniprot_O95817_fasta.fa \
--model esm1v_t33_650M_UR90S_1 \
--model esm1v_t33_650M_UR90S_2 \
--model esm1v_t33_650M_UR90S_3 \
--model esm1v_t33_650M_UR90S_4 \
--model esm1v_t33_650M_UR90S_5 \
--output_heatmap data/output/output_heatmap_colormesh.svg
```

or
```
python ./scripts/esm_calc.py \
--input data/input/231111_BAG3_homosapiens_uniprot_O95817_fasta.fa \
--model esm1v_t33_650M_UR90S_1 \
--model esm1v_t33_650M_UR90S_2 \
--model esm1v_t33_650M_UR90S_3 \
--model esm1v_t33_650M_UR90S_4 \
--model esm1v_t33_650M_UR90S_5 \
--output_heatmap data/output/output_heatmap_imshow.svg
```
