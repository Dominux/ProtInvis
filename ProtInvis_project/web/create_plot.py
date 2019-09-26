from Bio.SeqUtils.ProtParam import ProteinAnalysis  
from requests_html import HTMLSession
<<<<<<< HEAD
from constants import dyes_list, aa_list, a_replace
=======
from constants import dyes_list, aa_list
>>>>>>> 33bda76ad6a59478773d9cf10be959aec9e6e565
import plotly
from plotly import graph_objs as go
import pandas as pd
import json


session = HTMLSession()

def get_seq(uniprot_id, session=session):                                
    URL = 'https://www.uniprot.org/uniprot/' + uniprot_id + '.fasta'
    while True:
        try:
            result = session.get(URL)
            if result.ok:
                start = 0
                for aa in result.text:
                    start += 1
                    if aa == '\n':
                        break
                return ''.join(str(line.replace('X', '')) for line in list(result.text[start:].split('\n')))
        except:
            pass

def get_proteome(proteome_id, session=session):                                 
    URL = 'https://www.uniprot.org/proteomes/' + proteome_id
    while True:
        try:
            result = session.get(URL)
            if result.ok:
                href = [x for x in list(result.html.absolute_links) if x.startswith('f')][-1]
                table = pd.read_csv(href, compression='gzip', sep='\n', header=None, na_filter=False)
                protein_dict = dict()
                for line in table.iloc[:,0]:
                    if line.startswith('>'):
                        name_terminator = line.find('|', 4)
                        uniprot_id = line[4:name_terminator]
                        protein_dict[uniprot_id] = str()
                    else:
<<<<<<< HEAD
                        for amino in a_replace:
                            line = line.replace(amino, a_replace[amino])
=======
                        line = line.replace('X', '')
>>>>>>> 33bda76ad6a59478773d9cf10be959aec9e6e565
                        protein_dict[uniprot_id] += line
                return protein_dict
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
    return [ProteinAnalysis(aa_seq).molecular_weight(), 
            ProteinAnalysis(aa_seq).isoelectric_point()]

def after_dye(data, the_dye):
    invis_data = list()
    new_data = data.copy()
    for protein in data:
        if [protein[1][aa] for aa in the_dye if protein[1][aa] > 0] == []:
            invis_data.append(protein)
            new_data.remove(protein)
    return new_data, invis_data

def make_scatter(proteome_datas, input_id):
    invis_data = proteome_datas[1][1]
    proteome_datas[1] = proteome_datas[1][0]
    fig = go.Figure()
    for data in range(len(proteome_datas)):
        iter_data = proteome_datas[data]
        x = [iter_data[M][2][1] for M in range(len(iter_data))]
        y = [iter_data[M][2][0] for M in range(len(iter_data))]
        text = [iter_data[M][0] for M in range(len(iter_data))]
        if data == 0:
            color = 'red'
            legend_name = 'Invisible'
            marker_line_width = 0
        else:
            color = 'limegreen'
            legend_name = 'Visible'
            marker_line_width = 1
        fig.add_trace(go.Scatter(
                            x=x, 
                            y=y,
                            text=text,
                            name=legend_name,
                            mode='markers',
                            marker=dict(
                                    color=color, 
                                    line=dict(width=marker_line_width),
                                    size=8), 
                        ))
    fig.update_layout(
                autosize=False, 
                height=1000, 
                width=1000,
                xaxis=dict(title='Isoelectric point'),
                yaxis=dict(title='Molecular weight', autorange='reversed'),
            )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def ploter(input_id, the_dye, session=session, dyes_list=dyes_list):
    the_dye = dyes_list[the_dye]
    if input_id.startswith('U'):
        proteome = get_proteome(input_id, session)
        data = [(uniprot_id, aa_percent(proteome[uniprot_id]), 
            get_x_y(proteome[uniprot_id])) for uniprot_id in proteome.keys()]
    else:
        data = list()
        for uniprot_id in list(input_id.split()):
            proteome = get_seq(uniprot_id)
            data.append((uniprot_id, aa_percent(proteome), get_x_y(proteome)))
    return make_scatter([data, after_dye(data, the_dye)], input_id)
