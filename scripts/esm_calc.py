
"""
command python esm_calc.py
"""
import torch
from esm import Alphabet, pretrained
import click
import os
import matplotlib.pyplot as plt
import numpy as np


@click.command()
@click.option(
    "--input",
    "input_file",
    required=True,
    multiple=False,
    type=str,
    default="data/input/231111_BAG3_homosapiens_uniprot_O95817_fasta.fa",
    help="fasta file with aa seq",
)
@click.option(
    "--model",
    "modelsToUse",
    multiple=True,
    type=str,
    default=[
        "esm1v_t33_650M_UR90S_1",
        "esm1v_t33_650M_UR90S_2",
        "esm1v_t33_650M_UR90S_3",
        "esm1v_t33_650M_UR90S_4",
        "esm1v_t33_650M_UR90S_5",
    ],
    help="Models for download, default is all 5 models",
)
@click.option(
    "--output_heatmap",
    "output_heatmap",
    required=True,
    type=str,
    default="data/output/output_heatmap_imshow.svg",
    help="Output file",
)
def cli(input_file, modelsToUse, output_heatmap):
    torch.hub.set_dir(os.getcwd()+"/..")
    # process data for esm model
    fasta=open(input_file, "r")
    fasta_entry=fasta.read().split("\n")
    #print (fasta_entry)
    ID, seq = fasta_entry[0], fasta_entry[1]
    data=[]
    data.append((ID, seq))

    all_scores=[]
    for k in range(0, len(modelsToUse), 1):
        torch.cuda.empty_cache()
        model, alphabet = pretrained.load_model_and_alphabet(modelsToUse[k])
        model.eval()  # disables dropout for deterministic results
        batch_converter = alphabet.get_batch_converter()
        if torch.cuda.is_available():
            model = model.cuda()

        # apply es model to sequence, tokenProbs hat probs von allen aa an jeder pos basierend auf der seq in "data"
        if len(data) == 1:
            all_scores=[]
            batch_labels, batch_strs, batch_tokens = batch_converter(data)
            with torch.no_grad():  # setzt irgeineine flag auf false
                token_probs = torch.log_softmax(
                        model(batch_tokens)["logits"], dim=-1
                )  # .cuda() weg um auf cpu laufen zu lassen
            print (token_probs.size())
            token_probs_np=token_probs.numpy()
            token_probs_np=token_probs_np[0 , 1:-1 , 4:24]
            print(token_probs_np.shape[0])
            all_scores.append(token_probs_np)
        

        token_probs_np=False
        token_probs_np=np.mean( np.array([ all_scores ]), axis=0 ) [0, :, :] 
        print(token_probs_np.shape)
        # plot
        plt.figure(figsize=(token_probs_np.shape[0]/5, 20))
        y_list=["L","A","G","V","S","E","R","T","I","D","P","K","Q","N","F","Y","M","H","W","C"]
            
        plt.imshow(np.transpose(token_probs_np) )

        plt.yticks(np.arange(len(y_list)), labels=y_list, fontsize=6) #np.arange(len(y_list)),
        plt.xticks(ticks=np.linspace(0,token_probs_np.shape[0]-1, 50).astype(int), labels=np.linspace(0,token_probs_np.shape[0]-1, 50).astype(int)+1, fontsize=12)
            
        # color bar legend
        cb = plt.colorbar(label="log (ESM-1v)")
        cb.ax.tick_params(labelsize=12)
            

        plt.title("ESM-1v scores")
        plt.xlabel("sequence")
        plt.ylabel("amino acid type")
        #plt.tight_layout()
        #plt.show()
        plt.savefig(output_heatmap)
        plt.close()



                    # test and extract scores from tokenProbs


    #print (data)


if __name__ == "__main__":
    cli()