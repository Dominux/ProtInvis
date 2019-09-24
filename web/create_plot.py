from Bio.SeqUtils.ProtParam import ProteinAnalysis  
from requests_html import HTMLSession
from constants import dyes_list, aa_list
import matplotlib.pyplot as plt
import pandas as pd
import io


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
                        line = line.replace('X', '')
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

def two_dim_electrophoresis(proteome_datas, input_id):
    invis_data = proteome_datas[1][1]
    proteome_datas[1] = proteome_datas[1][0]
    plt.figure(figsize=(19.2, 10.8))
    plt.style.use(['bmh'])
    if len(proteome_datas[1]) < 10:
        alpha = 0.78
        s = 68
    elif len(proteome_datas[1]) < 100:
        alpha = 0.7
        s = 48
    elif len(proteome_datas[1]) < 1000:
        alpha = 0.62
        s = 28
    elif len(proteome_datas[1]) < 10000:
        alpha = 0.54
        s = 20
    else:
        alpha = 0.46
        s = 14
    for data in range(len(proteome_datas)):
        x = [proteome_datas[data][M][2][1] for M in range(len(proteome_datas[data]))]
        y = [proteome_datas[data][M][2][0] for M in range(len(proteome_datas[data]))]
        plt.subplot(1, 2, data + 1)
        plt.scatter(x, y, s=s, c='#cb4bd4', alpha=alpha)
        if data == 0:
            title_name = 'All proteins'
        else:
            title_name = 'Real result'
        plt.title(title_name)
        plt.xlabel('Isoelectric point')
        plt.ylabel('Molecular weight')
        plt.xlim(0, 14)
        plt.ylim(250000, 0)
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image

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
    return two_dim_electrophoresis([data, after_dye(data, the_dye)], input_id)
