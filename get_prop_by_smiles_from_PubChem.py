import requests

#initialise smiles and required properties
#check here for property table: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest#section=Compound-Property-Tables

sm = "C1=CC(=C(C=C1Cl)O)OC2=C(C=C(C=C2)Cl)Cl"
all_prop = ['HBondAcceptorCount', 'HBondDonorCount', 'XLogP', 'TPSA']
prolog = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug'

def get_cid_by_smiles(sm, prolog):
    
    """
    Get CID first
    """
    get_cid_part_url = "/compound/smiles/cids/txt"
    url = prolog + get_cid_part_url
    struct = {'smiles': sm}
    res = requests.get(url, params = struct)
    cid = res.text
    return cid

def form_prop_url(cid, prolog, all_prop):
    """
    construct property url part from the property list
    """
    join_prop = ','.join(all_prop)
#     print(join_prop)
    prop_url = prolog + '/compound/cid/' + str(cid) + '/property/' + join_prop + '/CSV'
    return prop_url

def prop_t2dict(prop_text):
    """
    reformat the result text into dict
    """
    full_prop_list = prop_text.split('\n')
#     print(full_prop_list)
    prop_dict = {}
    title_line = full_prop_list[0]
    all_prop_name = title_line.split(',')
    data_line = str(full_prop_list[1])
    all_data = data_line.split(',')
#     print(all_prop_name)#
#     print(all_data)
    for i, elt in enumerate(all_prop_name):
        prop_dict[elt] = all_data[i]
    print(prop_dict)
    return prop_dict
            
def get_prop_by_smiles(sm, prolog, all_prop):
    """
    get property data by smiles
    """
    cid = get_cid_by_smiles(sm, prolog).rstrip() #note that the cid text has whitespace in the end
    prop_url = form_prop_url(cid, prolog, all_prop)
    print(prop_url)
    prop_res = requests.get(prop_url)
    prop_res_text = prop_res.text
    print(prop_res_text)
    prop_dict = prop_t2dict(prop_res_text)
    return prop_dict

get_prop_by_smiles(sm, prolog, all_prop)
    
    
