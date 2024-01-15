
"""
command python esm_calc.py
"""

from turtle import color
import click
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import pandas as pd


@click.command()
@click.option(
    "--input",
    "input_file",
    required=True,
    multiple=False,
    type=str,
    default="data/output/output_table.npz",
    help="npz file with esm scores",
)
@click.option(
    "--region_pos",
    "region_pos",
    required=True,
    multiple=True,
    type=str,
    default=["21-55", "87-101", "200-213", "420-499"],
    help="Output file",
)
@click.option(
    "--region_name",
    "region_name",
    required=True,
    multiple=True,
    type=str,
    default=["WW", "IPV #1", "IPV #2", "BAG domain"],
    help="Output file",
)
@click.option(
    "--output_folder",
    "output_folder",
    required=True,
    type=str,
    default="data/output/",
    help="Output folder",
)
def cli(input_file, region_pos, region_name, output_folder):
    scores=np.load (input_file)
    scores= scores.f.arr_0
    scores=scores.astype(np.float32)
    scores=np.transpose(scores)
    print (scores.shape)

    # generate data bins using regions
    if len (region_pos) != len(region_name):
        raise ValueError('region_ name and region_pos have to be of same length')

    score_array=[]
    for i in range (0, len(region_pos)):
        print (region_pos[i])
        region_pos_temp=region_pos[i].split("-")
        start, stop = int(region_pos_temp[0]), int(region_pos_temp[1])+1
        score_array.append(scores[:, start:stop])
        print(score_array[-1].shape)
    
    control_scores=scores
    score_array.append(control_scores)
    



    # prepare for plotting
    score_array_plotting=[]
    quantiles=[]
    for i in range (0, len(score_array), 1):
        score_array_plotting.append(score_array[i].flatten())
        print(score_array_plotting[-1].shape)
        quantiles.append([])
    
    # prepare y ticks
    region_name_list=[]
    for i in range (0, len(region_name), 1):
        region_name_list.append(region_name[i])
    region_name_list.append("all")


    #print (score_array_plotting)
    #print (score_array_plotting.shape())
 
    # statistical testing
    stats_list=[]
    comp=[]
    height=1
    for i in range (0, len(score_array_plotting)-1, 1):
        comp.append(region_name_list[i]+" vs all")
        p_val=stats.kruskal(score_array_plotting[i], score_array_plotting[-1])[1]
        stats_list.append(p_val)
        plt.hlines(y=height, xmin=i+1, xmax=len(score_array_plotting), color="black")
        plt.text(i+1, height+1, format(p_val, ".1E") , ha='center', va='center')
        height = height + 1    
    print (stats_list)
    df =  pd.DataFrame({"p-val":stats_list, "comparison":comp})
    df.to_csv(output_folder+"kruskal_test_esm.tsv", sep="\t")


    violin_parts = plt.violinplot(score_array_plotting, points=100, showextrema=False, quantiles=quantiles)
    for pc in violin_parts['bodies']:
        pc.set_facecolor('grey')
        pc.set_edgecolor('black')
        pc.set_alpha(1)

    plt.xticks(np.arange(1, len(region_name_list)+1), labels=region_name_list, fontsize=10)

    


    plt.ylabel("lg(ESM-1v score)")
    #plt.xlabel("Domain")
    plt.ylim(-25, 3+height)
    plt.tight_layout()
    plt.savefig(output_folder+"/violin_plots_with_kruskal_esm.svg")
    plt.show()
    
            

       

if __name__ == "__main__":
    cli()