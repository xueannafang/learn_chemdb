# learn_chemdb

Some exploration in cheminformatics!

## File explanation

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