#this follows the "write_multiple_molecule_into_sdf"
#we want to pick out unique smiles among these substances
#RDkit required
from rdkit import Chem

sdf_file_name = "cid2sids-uracil.sdf"
suppl = Chem.SDMolSupplier(sdf_file_name) #chunk the entire data file into individual substance


#extract isomeric smiles for each molecule, add to the result dictionary that contains the frequency of occurrence for each unique smiles
uniq_smiles = {} #key is unique smiles, value is its fequency
for mol in suppl:
    smiles = Chem.MolToSmiles(mol, isomericSmiles = True) #convert individual molecular strutural data file to isomeric Smiles
    uniq_smiles[smiles] = uniq_smiles.get(smiles, 0) + 1 #write new smiles into the unique smiles dictionary, if smiles not exists, cretate item and set its frequency (dictionary value) as 0, otherwise add 1 to the existing frequency

#let's see how many smiles we got
sort_by_freq = [(fre, sm) for sm, fre in uniq_smiles.items()]
sort_by_freq.sort(reverse = True) #present in the descending order

for fre, sm in sort_by_freq:
    print(fre, sm)

