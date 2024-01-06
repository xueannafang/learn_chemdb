# learn_chemdb

This is my playground for some exploration in cheminformatics!

Below are some selection that I found useful and intersting during study.

## File explanation (the learning diary)


- [get_prop_by_smiles_from_PubChem.py](https://github.com/xueannafang/learn_chemdb/blob/main/get_prop_by_smiles_from_PubChem.py)

This is a practice that first covert the given smiles string to CID, followed by searching a given list of properties. Note that properties are joined in one single request for this case and should not be too long (less than 50, ref [here](https://chem.libretexts.org/Courses/Intercollegiate_Courses/Cheminformatics/01%3A_Introduction/1.10%3A_Python_Assignment_1) for required splitting on input request.)



- [get_properties_by_smiles_from_pubchem_searchby_general.py](https://github.com/xueannafang/learn_chemdb/blob/main/get_properties_by_smiles_from_pubchem_searchby_general.py)

This is the general version to understand how PUG-REST works. The URL is chunked into specific searchby criteria (pugin_pre, pugin_searchby), operation (pugoper_pre) and allows multiple search to go by looping over compounds to search (all_comp_to_search) and properties (all_prop_to_search). The test example defined a function to generate simple alkanes by setting the carbon number (gen_comp_by_rule). Each request waits for 1 second that can be modified down to no less than 0.2s per entry (i.e., no more than 5 requests per second) to abide the PubChem usage policy. (Sleep is important!!!)

- [search_mix_with_same_comp.py](https://github.com/xueannafang/learn_chemdb/blob/main/search_mix_with_same_comp.py)

This part can search mixtures that contains multiple compounds of interests. For example, in certain cases we need to find compound mixtures with specific (useful) ingredients. The key step is to add ```?cids_type=component``` after the pugout block.

- [write_multiple_molecule_into_sdf.py](https://github.com/xueannafang/learn_chemdb/blob/main/write_multiple_molecule_into_sdf.py)

This is part of the exercises to understand the difference between "compound" and "substance". One compound can have multiple substances matching. The side job is to learn how to write structural information (as well as full record) of multiple molecules into one sdf file. The process is to first get all SIDs based on the given CID, followed by chunking all SIDs into blocks of no more than 50 entries. Finally, request sdf for each entry and write into our target combined sdf file (named after "cid2sids_cid_#.sdf"). Some other operations can be done based on the as-generated multi-entry sdf file..

Expected outcome is stored [here](https://github.com/xueannafang/learn_chemdb/blob/main/practice_from_cheminfo_with_filled_notebook/lec_4/cid2sids-uracil.sdf) under filled_notebook -> lec_4.

And to read sdf  for futher operation, we may need [RDkit](https://www.rdkit.org/docs/GettingStartedInPython.html).

```
from rdkit import Chem

sdf_file_name = "filename.sdf"
suppl = Chem.SDMolSupplier(sdf_file_name)

```

Further operation can be done based on ```suppl```.


- [Deal_with_missing_structural_data.py](https://github.com/xueannafang/learn_chemdb/blob/main/deal_with_missing_structural_data.py)

In the case when structural data is missing, which we would get an empty smiles string, this can find the auto_structure information from the sdf based on the substance id.


- [draw_mol_by_smiles.py](https://github.com/xueannafang/learn_chemdb/blob/main/draw_mol_by_smiles.ipynb)

Based on a given list of smiles (that could contain empty string), plot the chemical scheme in a batch.

- [identical_property_search.ipynb](https://github.com/xueannafang/learn_chemdb/blob/main/identical_property_search.ipynb)

Search for compounds with same features, such as connectivity. Important step is to add ```fast##``` (keyword) in the pugin block, and ```?identity_type=``` plus the corresponding type of identity search in the pugout part.

- [structural_similarity.ipynb](https://github.com/xueannafang/learn_chemdb/blob/main/structural_similarity.ipynb)

Search for compounds with 2D similarity over given threshold or 3D similarity higher than default settings. 

- [Fingerprints](https://github.com/xueannafang/learn_chemdb/blob/main/fingerprint.ipynb)

Understand how molecular structures are hashed via different pathway. When comparing two structures, using fingerprints (a bit vector) can significantly help with the efficiency of matching. Important concepts are:

 MACCSKeys - a 166 bit vector with each position representing the existence of a specific chemical feature, such as is_aromatic, is_a_ring, 3_membered_ring, contains_atom_number_x, contain_substructure_a, etc.
 
 MorganFingerprint - based on radius from heavy atoms; analogous to the extended-connectivity fingerprint - ECFP and Funtional-Class Fingerprints - FCFP, whose followed number reflects the diameter instead of radius. These three are all "circular fingerprints"..... tbc

 Why FPs are useful?

 Despite the same FP might still match some variations of structures, if the FP between two molecules are already different, they are for sure different, and therefore no need to look at deeper level of structural data.



---------------

- [codewar_full_chem.py](https://github.com/xueannafang/learn_chemdb/blob/main/codewar_full_chem.py)

This is my attempted test on a level 2 keta on [CodeWar](https://www.codewars.com/kata/5a27ca7ab6cfd70f9300007a). The aim is to build an organic molecule based on given length of carbon backbone with branches, followed by a seris of operations, such as atom mutation (e.g., change carbon to sulfur), add atoms/branches, add and remove explicit hydrogen atoms. Basic information of the molecule, such as the molecular weight, molecular formula, can be presented when calling corresponding functions.

This is a great practice to better understand how computer represent molecules and key connection information, as well as how to modify the structure of the molecule of interests. It is also a good practice to learn OOP. More introduction is on the original keta link above.

Key functions and how to use:

```
your_molecule= Molecule("YourMoleculeName")

#Add branch of carbon length x, y, z, ... at backbone index (based on its sequence, all are 1-indexed)
your_molecule.brancher(x, y, z, ...)

#Create bond between given atom index on given branch index, could have multiple inputs
your_molecule.bounder((atom1, branch1, atom2, branch2), (atom3, branch3, atom4, branch4), ...)

#Change current atom to a different one, we need to indicate the location of the current atom on the carbon backbone and on the branch
your_molecule.mutate((carbon_index, on_the_branch_index, new_element), (), (), ...)

#Add atom at given location
your_molecule.add((carbon_index, on_the_branch_index, element_to_add), (), (), ...)

#Add chain at given location
your_molecule.add_chaining(carbon_index, on_the_branch_index, element1_to_add, element_2_to_add, ...)

#Lock the molecule and add hydrogens, you can get properties after locking the molecule, but not able to modify it.
your_molecule.closer()

#Unlock the molecule, remove explict hydrogens, and continue editing.
your_molecule.unlock()

#Get molecular formula
your_molecule.formula

#get molecular weight
your_molecule.molecular_weight

#get all atoms
your_molecule.atoms

#get the name of this molecule
your_molecule.name

```


# References

Everything in this playground is some practice and reflection based on the training provided by:

- [Codewars](https://www.codewars.com/)
- [ChemLibreTexts ChemInformatics](https://chem.libretexts.org/Courses/Intercollegiate_Courses/Cheminformatics)

