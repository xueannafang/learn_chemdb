#followed by "unique_smiles_in_sdf", there are possibilities to have structural data missing
#structural data can be generated by matching synonomes with same CID by PubChem

#again, get molecule data separated first...
from rdkit import Chem

sdf_file_name = "cid2sids-uracil.sdf"
suppl = Chem.SDMolSupplier(sdf_file_name) #chunk the entire data file into individual substance

for mol in suppl:
    smiles = Chem.MolToSmiles(mol, isomericSmiles = True)

    if smiles == "":
        this_sid = mol.GetProp("PUBCHEM_SUBSTANCE_ID")
        this_auto_struct = mol.GetProp("PUBCHEM_SUBS_AUTO_STRUCTURE")
        print(this_sid, " : ", this_auto_struct)


#what it actually does here is to find <PUBCHEM_SUBS_AUTO_STRUCTURE> and <PUBCHEM_SUBSTANCE_ID> in the sdf record.
#We can take a look at the original sdf file we submit at the beginning and manually find those entries too.
        