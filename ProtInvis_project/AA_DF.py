from Bio.SeqUtils.ProtParam import ProteinAnalysis  
from requests_html import HTMLSession
import matplotlib.pyplot as plt
import pandas as pd


session = HTMLSession()

aa_list_global = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
dyes = {
        ('Кумасси бриллиантовый синий'): ['K', 'R', 'H'],
        ('Окрашивание серебром'): ['N', 'Q', 'C'],
        ('Амидо черный'): ['K', 'R', 'H'],
        ('Бромфеноловый синий'): ['K', 'R', 'H'],
        ('Пирогаллоловый красный'): ['K'],
        ('Sypro Ruby'): ['K', 'R', 'H'],
        ('Stain-free'): ['W'],
        ('Zn-имидазольное негативное окрашивание'): ['H', 'C', 'Q', 'N'],
}

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
                        uniprot_id = line[4:10]
                        protein_dict[uniprot_id] = str()
                    else:
                        line = line.replace('X', '')
                        protein_dict[uniprot_id] += line
                return protein_dict
        except:
            pass

def aa_percent(aa_seq):                                  
    aa_list = aa_list_global.copy()
    protein_aa = dict()
    for aa in aa_list:
        aa_index = aa_list.index(aa)
        aa_list[aa_index] = (aa, list(aa_seq).count(aa) / len(aa_seq))
        protein_aa[aa] = (round(aa_list[aa_index][1] * 100, 2))
    return protein_aa

def get_x_y(aa_seq):
    return [ProteinAnalysis(aa_seq).molecular_weight(), 
            ProteinAnalysis(aa_seq).isoelectric_point()]

def after_dye(data, the_dye):
    new_data = data.copy()
    for protein in data:
        if [protein[1][aa] for aa in the_dye if protein[1][aa] > 0] == []:
            new_data.remove(protein)
    return new_data

def two_dim_electrophoresis(proteome_datas, input_id):
    for data in range(len(proteome_datas)):
        x = [proteome_datas[data][M][2][1] for M in range(len(proteome_datas[data]))]
        y = [proteome_datas[data][M][2][0] for M in range(len(proteome_datas[data]))]
        plt.subplot(1, 2, data + 1)
        plt.scatter(x, y, s=20, c='#2300A8', alpha=0.5)
        plt.xlabel('Isoelectric point')
        plt.ylabel('Molecular weight')
        plt.gca().invert_yaxis()
    plt.show()

def ploter(input_id, the_dye, session=session):
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


input_id = 'F0NH14 F0NEJ8 C3NC73 C4KLB2 P39180 P01089 P18640'
the_dye = dyes[('Кумасси бриллиантовый синий')]
ploter(input_id, the_dye)


# ids = 'P39180 P01089 P18640'
# proteome_id = 'UP000007662'
# proteome_id = 'UP000007021'
# proteome_id = 'UP000001974'
# proteome_id = 'UP000008827'
