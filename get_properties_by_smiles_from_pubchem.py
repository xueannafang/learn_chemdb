import time
import requests

#url = pugrest/pugin_pre/pugin_searchby/pugin_to_search/pugoper_pre/pugoper_to_search/pugout

pugrest = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
pugin_pre = 'compound'
pugin_searchby = 'smiles' #directly add smiles to url sometimes can cause error, try dictionary method
pugoper_pre = 'property'
pugout = 'txt'

def gen_comp_by_rule(up_num_c):
    """
    generate a series of alkanes by the number of carbons
    """
    all_comp = ['C'*num_c for num_c in range(1, up_num_c +1)]
    return all_comp

all_comp_to_search = gen_comp_by_rule(4) #here the comp is represented by smiles
#all_comp_to_search = ['water', 'ethanol', 'methanol', 'butanol']
all_prop_to_search = ['XLogP', 'MolecularWeight'] #'HBondAcceptorCount', 'HBondDonorCount'


all_rst = []
for comp in all_comp_to_search:
    crt_comp = {}
    crt_comp[pugin_searchby] = comp
    struct = {pugin_searchby : comp}
    for pugoper_searchby in all_prop_to_search:
        url = '/'.join([pugrest, pugin_pre, pugin_searchby, pugoper_pre, pugoper_searchby, pugout])
        
        crt_prop = requests.get(url, params = struct)
        time.sleep(1)
        print(url)
        crt_comp[pugoper_searchby] = crt_prop.text.rstrip()

        #crt_comp[pugoper_searchby] = crt_prop.text
    all_rst.append(crt_comp)
    print(crt_comp)
