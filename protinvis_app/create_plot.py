from Bio.SeqUtils.ProtParam import ProteinAnalysis  
from requests_html import HTMLSession
from .constants import dyes_list, aa_list, a_replace
import plotly
from plotly import graph_objs as go
import pandas as pd
import json


session = HTMLSession()

def get_seq(uniprot_id, session=session):                                
    URL = f'https://www.uniprot.org/uniprot/{uniprot_id}.fasta'
    while True:
        try:
            result = session.get(URL)
            if result.ok:
                start = 0
                for aa in result.text:
                    start += 1
                    if aa == '\n':
                        break
                aa_seq = str()
                for line in list(result.text[start:].split('\n')):
                    for amino in a_replace:
                        line = line.replace(amino, a_replace[amino])
                    aa_seq += line
                return aa_seq
            elif result.status_code == 404:
                return uniprot_id
        except:
            pass

def get_proteome(proteome_id, session=session):                                 
    URL = f'https://www.uniprot.org/proteomes/{proteome_id}'
    while True:
        try:
            result = session.get(URL)
            if result.ok:
                for href in list(result.html.absolute_links):
                    if href.startswith('f'):
                        if href.split('/')[8] == "reference_proteomes":
                            break
                table = pd.read_csv(href, compression='gzip', sep='\n', header=None, na_filter=False)
                protein_dict = dict()
                for line in table.iloc[:,0]:
                    if line.startswith('>'):
                        uniprot_id = line.split('|')[1]
                        protein_dict[uniprot_id] = str()
                    else:
                        for amino in a_replace:
                            line = line.replace(amino, a_replace[amino])
                        protein_dict[uniprot_id] += line
                return protein_dict
            elif result.status_code == 404:
                return proteome_id
        except:
            pass

def aa_percent(aa_seq):                                  
    aa_list_local = aa_list.copy()
    protein_aa = dict()
    for aa in aa_list_local:
        aa_index = aa_list_local.index(aa)
        aa_list_local[aa_index] = (aa, list(aa_seq).count(aa) / len(aa_seq))
        protein_aa[aa] = (round(aa_list_local[aa_index][1] * 100, 2))
    return protein_aa

def get_x_y(aa_seq):
    return (ProteinAnalysis(aa_seq).molecular_weight(), 
            ProteinAnalysis(aa_seq).isoelectric_point())

def after_dye(data, the_dye):
    invis_data = list()
    new_data = data.copy()
    for protein in data:
        if [protein[1][aa] for aa in the_dye if protein[1][aa] > 0] == []:
            invis_data.append(protein)
            new_data.remove(protein)
    return (invis_data, new_data)

def make_scatter(proteome_datas, max_mol):
    fig = go.Figure()
    for data in range(len(proteome_datas)):
        iter_data = proteome_datas[data]
        x = [iter_data[M][2][1] for M in range(len(iter_data))]
        y = [iter_data[M][2][0] for M in range(len(iter_data))]
        text = [iter_data[M][0] for M in range(len(iter_data))]
        if data == 0:
            color = 'red'
            legend_name = f'Invisible: {len(text)}'
            marker_line_width = 0
        else:
            color = 'limegreen'
            legend_name = f'Visible: {len(text)}'
            marker_line_width = 1
        fig.add_trace(go.Scatter(
                            x=x, 
                            y=y,
                            text=text,
                            hoverinfo="text",
                            name=legend_name,
                            mode='markers',
                            marker=dict(
                                    color=color, 
                                    line=dict(width=marker_line_width),
                                    size=8
                                    ), 
                        ))
    fig.update_layout(
                autosize=False, 
                height=1000,
                width=1300,
                template="plotly_dark",
                plot_bgcolor='rgba(247, 247, 247, 1)',
                paper_bgcolor='rgba(17, 17, 17, 1)',
                xaxis=dict(title='Isoelectric point', range=[0, 14]),
                yaxis=dict(title='Molecular weight', range=[max_mol*1.1, 0]),
            )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def ploter(input_id, the_dye, session=session, dyes_list=dyes_list):
    the_dye = dyes_list[the_dye]
    if input_id.startswith('U'):
        proteome = get_proteome(input_id, session)
        if proteome == input_id:
            return input_id
    else:
        proteome = dict()
        for uniprot_id in set(input_id.split()):
            seq = get_seq(uniprot_id)
            if seq == uniprot_id:
                return uniprot_id
            proteome[uniprot_id] = seq
    data = [(uniprot_id, aa_percent(proteome[uniprot_id]), 
            get_x_y(proteome[uniprot_id])) for uniprot_id in proteome.keys()]
    max_mol = max([_[2][0] for _ in data])
    return make_scatter(after_dye(data, the_dye), max_mol)
