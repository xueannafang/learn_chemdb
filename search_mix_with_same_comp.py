#search mixtures that contains multiple compounds of interests

#First, construct the compound list
#compounds to contain
things_to_contain = ['aspirin', 'tylenol', 'advil']

#Step 2: Find the CIDs for each of these compounds
import requests
import time

prolog    = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"


all_cids = []
for name in things_to_contain:
    url = prolog + "/compound/name/" + name + "/cids/txt"
    res = requests.get(url)
    print(url)
    time.sleep(0.2)
    component_cid = res.text.rstrip()
    # print("name:", name)
    # print("Number of component:", len(component_cid))
    print(component_cid)
    all_cids.append(component_cid)


#step 3: For each compound, find all mixtures that contains corresponding compound, key step is highlighted below
all_mix = []
for cid in all_cids:
    this_comp = {}
    this_comp['cid'] = cid
    this_comp['mix_cid'] = component_cids
    
    url = prolog + "/compound/cid/" + cid + "/cids/txt?cids_type=component" #key step
    res = requests.get(url)
    time.sleep(0.2)
    component_cids = res.text.split()
    print( "CID:", cid)
    print( "Number of Components", len(component_cids))
    # print( component_cids )

    all_mix.append(this_comp)

print(all_mix)

#step 4: take the intersection of each mixture list
int_set = set(all_mix[0]['mix_cid'])
for i, drug in enumerate(all_mix):
    if i > 0:
        int_set = set(drug['mix_cid']).intersection(set(all_mix[i-1]['mix_cid']))

print(len(int_set))