from requests_html import HTMLSession
import pandas as pd

session = HTMLSession()

def get_seq(uniprot_id, session):                                              # \\ get_seq получает fasta по uniprot_id и вырезает из неё лишь последовательность
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
                print(uniprot_id)
                return ''.join(str(line) for line in list(result.text[start:].split('\n')))
        except:
            pass

def get_proteome(proteome_id, session):                                   # \\ get_proteome принимает proteome_id и выдаёт список uniprot_id
    URL = 'https://www.uniprot.org/proteomes/' + proteome_id
    while True:
        try:
            result = session.get(URL)
            if result.ok:
                href = [x for x in list(result.html.absolute_links) if x.startswith('f')][-1]
                table = pd.read_csv(href, compression='gzip', sep='\n', header=None)
                table_new = table[~table.iloc[:,0].str.contains('>', na=False)]
                return ''.join(str(line) for line in table_new.iloc[:,0].tolist())
        except:
            pass

def aa_percent(total_seq):                                            # \\ aa_percent получает на вход последовательность и считает процентное соотношение аминокислот в ней    
    total_percent = 0
    aa_list = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    for aa in aa_list:
        aa_index = aa_list.index(aa)
        aa_list[aa_index] = (aa, list(total_seq).count(aa) / len(total_seq))
        print(aa_list[aa_index][0] + ': ' + str(aa_list[aa_index][1] * 100) + '%')
        total_percent += aa_list[aa_index][1]
    print('Сумма процентов: ' + str(total_percent * 100) + '%')
    print('Количество аминокислот: ' + str(len(total_seq)))

def main(input_id):                                                    # \\ main - выполнение всего скрипта
    if input_id.startswith('U'):
        id_list = get_proteome(input_id, session)
        aa_percent(id_list)  
    else:
        id_list = list(input_id.split())
        aa_percent(''.join(get_seq(seq, session) for seq in id_list))

main('UP000008827')

# ids = 'P39180 P01089 P18640'
# proteome_id = 'UP000007662'
