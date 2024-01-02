atom_db = {
    'symbol' : ['H', 'B', 'C', 'N', 'O', 'F', 'Mg', 'P', 'S', 'Cl', 'Br'],
    'valence_number' : [1, 3, 4, 3, 2, 1, 2, 3, 2, 1, 1],
    'atom_weight' : [1, 10.8, 12, 14, 16, 19, 24.3, 31, 32.1, 35.5, 80]
}

all_atom_info = {}
for i, symb in enumerate(atom_db['symbol']):
    all_atom_info[symb] = [atom_db['valence_number'][i], atom_db['atom_weight'][i]]
    
#database prepared

#define error handling cases

class InvalidBond(Exception): pass #Number of bonds will exceed the allowed situations, i.e., no larger than the valence number
class UnlockedMolecule(Exception): pass #Attempt to output properties of molecules without locking it first
class LockedMolecule(Exception): pass #Attempt to modify the molecule that has already been locked.
class EmptyMolecule(Exception): pass #Molecule has no atom left.

#define atom output sequence
atom_op_order = ['C', 'O', 'B', 'Br', 'Cl', 'F', 'Mg', 'N', 'P', 'S', 'H']
formula_op_order = ['C', 'H', 'O', 'B', 'Br', 'Cl', 'F', 'Mg', 'N', 'P', 'S']


class Atom(object):
    
    def __init__ (self, elt, id_):
        self.element = elt #the element of the current atom
        self.id = id_ # the id of the current atom
        self.bonds = [] #all bonded atoms connected the current atom
        
    def __hash__(self):      return self.id
    def __eq__(self, other): return self.id == other.id

    #each atom instance has the following properties that represtns the valence number, atomic weight, number of bonds with other atoms, number of free positions and a boolean that indicates if it is still bondable or not.
    
    @property
    def valence(self): return all_atom_info[self.element][0] #get valence number from db

    @property
    def weight(self): return all_atom_info[self.element][1] # get atomic weight from db

    @property
    def nbonds(self): return len(self.bonds) # num of bonds

    @property
    def free_position(self): return self.valence - self.nbonds #free positions of current atom

    @property
    def available(self): return self.free_position >= 1 #return true or false, current atom is still available for further bondings or not

    #operations on atoms.
    
    def mutate(self, new_elt):
        """
        mutate will change the current element to a new one
        before doing so, the operation needs to be validated in terms of the free positions of the new atom based on current bonding case
        """
        new_val = all_atom_info[new_elt][0]
        if self.nbonds > new_val:
            raise InvalidBond("The number of bonds will exceed the valence number.")
        self.element = new_elt #if error not raised, mutate the current element with the new element
    
    def add_bonds(self, atom):
        """
        add bond information with other atoms
        validate the atoms are bondable or not, including to check if the current atom has free positions and if the bonding is attempted with itself
        """
        if self.free_position == 0:
            raise InvalidBond("No available bonding positions.")
        if self == atom:
            raise InvalidBond("Cannot bond same atom together.")
        self.bonds.append(atom)
        
    def __str__(self):
        """
        This is the output string for each atom instance
        """
        crt_atom_with_id = f"{self.element}.{self.id}"
        #if no bond is connected with this atom, return above only
        if self.nbonds == 0: return f"Atom({crt_atom_with_id})"
        
        #otherwise sort all atoms according to their id and required output sequqnce
        sorted_bonds = sorted(self.bonds, key = lambda atom: atom.id)
        other_atoms = []
        for a in atom_op_order:
            for other_atom in sorted_bonds:
                if other_atom.element == a:
                    other_atoms.append(f"{other_atom.element}{other_atom.id}" if a != 'H' else f"{other_atom.element}")
        return f"Atom({crt_atom_with_id}: {','.join(other_atoms)})"
        
    
    
class Molecule(object):
    def __init__(self, name = ''):
        self.name = name
        self.branches = []
        self.atoms = []
        self.locked = False #after locked, the molecule will no longer be modifible and Hs will be added to the backbone
    
    # The Molecule instance have the following properties, including the formula and the molecular weight
    @property
    def formula(self):
        if not self.locked: raise UnlockedMolecule("Molecule must be locked before getting its formula.") # properties can only be calculated for a closed molecule.
        mol_form = ""
        for ele in formula_op_order:
            atm_cnt = 0
            for atm in self.atoms:
                if atm.element == ele:
                    atm_cnt += 1
            if atm_cnt > 1:
                mol_form += f"{ele}{atm_cnt}"
            elif atm_cnt == 1:
                mol_form += ele
        return mol_form
    
    @property
    def molecular_weight(self):
        if not self.locked: raise UnlockedMolecule("Molecule must be locked before calculating the molecular weight.")
        return sum([atom.weight for atom in self.atoms])
    
    @staticmethod
    def set_bond(atom1, atom2):
        """
        set bond between two atoms
        first need to check both atoms are valid to form new bond
        """
        if atom1.available and atom2.available:
            atom1.add_bonds(atom2)
            atom2.add_bonds(atom1)
        else:
            raise InvalidBond(f"Bond cannot be formed between {atom1} and {atom2}.")
        
    
    def get_branch(self, branch_idx):
        """
        get the branch by branch_idx
        """
        if branch_idx > len(self.branches): raise Exception("Branch index exceeds total branch number.")
        return self.branches[branch_idx-1] #because the branch is 1-indexed
    
    def get_atom_from_branch(self, atom_on_the_branch_idx, branch_idx):
        """
        note that the atom_idx here is the idx on the given branch
        """
        branch = self.get_branch(branch_idx)
        if atom_on_the_branch_idx > len(branch): raise Exception("Atom on the branch index exceeds total number of atoms on the branch.")
        return branch[atom_on_the_branch_idx-1] #again, the atom is also 1-indexed
    
    def _add_atom(self, elt):
        """
        create atom and append into the atom list
        return the atom instance
        """
        atom = Atom(elt, len(self.atoms)+1) #create an Atom instance with element and id defined by the sequence of addition
        self.atoms.append(atom) 
        return atom
    
    def brancher(self, *branch):
        """
        the input is a series of number that represent the length of each branch, could be one number or more, therefore, a star is required
        """
        if self.locked: raise LockedMolecule("You can't add branch to a locked molecule.") 
        for branch_len in branch:
            this_branch = self._brancher(branch_len)
            self.branches.append(this_branch)
        return self
    
    def _brancher(self, branch_len):
        """
        create the new branch based on the given length, branch_len
        """
        last_atom = None
        this_branch = []
        for i in range(branch_len):
            this_atom = self._add_atom('C')
            this_branch.append(this_atom)
            if last_atom is not None:
                self.set_bond(this_atom, last_atom)
            last_atom = this_atom
        return this_branch
        
    
    def bounder(self, *bonds):
        """
        see comment in _bounder
        this function creates bonds between given atom on given branch
        """
        if self.locked: raise LockedMolecule("Bonds cannot be created on a locked molecule.")
        
        for bond in bonds:
            self._bounder(bond)
        return self
            
    def _bounder(self, bond):
        """
        the bounder is misspelt by the kata supplier, the real meaning is bond
        the input bond is a tuple of carbon_idx_1, branch_idx_1, carbon_idx_2, branch_idx_2
        """
        c1, b1, c2, b2 = bond
        atom1 = self.get_atom_from_branch(c1, b1)
        atom2 = self.get_atom_from_branch(c2, b2)
        self.set_bond(atom1, atom2)
    
    def mutate(self, *muts):
        """
        muts has the structure of current_carbon_idx, current_branch_idx, element to replace
        """
        if self.locked: raise LockedMolecule("Mutate cannot happen on a locked molecule.")
        for mut in muts:
            self._mutate(mut)
        return self
    
    def _mutate(self, mut):
        """
        get the current atom from branch and change the element but remain the idx, special treatment is required for protons 
        """
        nc, nb, elt = mut
        atom = self.get_atom_from_branch(nc, nb)
        atom.mutate(elt)
    
    
    def add(self, *adds):
        """
        add atom at given carbon idx at branch idx
        """
        if self.locked: raise LockedMolecule("Atoms cannot be added on a locked molecule.")
        for to_add in adds:
            self._add(to_add)
        return self
    
    def _add(self, to_add):
        """
        to_add is a set of number with given carbon index, branch index and element to add
        """
        nc, nb, elt = to_add
        atom = self.get_atom_from_branch(nc, nb)
        if not atom.available: raise InvalidBond("Not enough position to add the new atom")
        added_atom = self._add_atom(elt)
        self.set_bond(atom, added_atom)
    
    def add_chaining(self, nc, nb, *elts):
        """
        create a chain at given carbon index and branch index, with a seris of elements
        """
        if self.locked: raise LockedMolecule("New chain cannot be added to a locked molecule.")
        atom = self.get_atom_from_branch(nc, nb)
        if atom.free_position < 1: raise InvalidBond("Not enough position to add the new chain.")
        new_chain = []
        for i, elt in enumerate(elts):
            new_atom = Atom(elt, len(self.atoms)+1+i)#the index of the new atom would be based on current total atoms and the sequence on the chain
            if new_chain:
                self.set_bond(new_chain[-1], new_atom)
            new_chain.append(new_atom)
        if not new_chain[0].available: raise InvalidBond("The atom to be attached on the existing chain has no available position to form new bonds.")
        self.set_bond(atom, new_chain[0])
        self.atoms.extend(new_chain)
        return self
        
    def closer(self):
        """
        Lock the molecule, add hydrogens at available free positions
        """
        if self.locked: raise LockedMolecule("Molecule is already locked.")
        for atom in self.atoms:
            if atom.free_position:
                for i in range(atom.free_position):
                    hydrogen = self._add_atom('H')
                    self.set_bond(hydrogen, atom)
        self.locked = True
        return self
    
    def unlock(self):
        """
        unlock the current molecule, remove redundant hydrogens and free atoms, reset ids
        """
        self._clean_atoms()
        self._clean_branches()
        self._reset_id()
        self.locked = False
        return self
    
    def _clean_atoms(self):
        """
        remove hydrogens and check if the molecule is empty or not
        """
        self._remove_H(self.atoms)
        if len(self.atoms) == 0: raise EmptyMolecule("No atom left in this molecule.")
    
    
    def _remove_H(self, atom_container):
        """
        remove hydrogens from the entire molecule and each branch
        """
        n = 0
        while n < len(atom_container):
            atom = atom_container[n]
            if atom.element == 'H':
                atom_container.remove(atom)
                for bond_atom in atom.bonds:
                    if atom in bond_atom.bonds: bond_atom.bonds.remove(atom)
                continue
            n += 1
    
    def _clean_branches(self):
        """
        go through each branch
        """
        k = 0
        while k < len(self.branches):
            branch = self.branches[k]
            self._remove_H(branch)
            if len(branch) == 0:
                self.branches.remove(branch)
                continue
            k += 1
        if len(self.branches) == 0: raise EmptyMolecule("No branches left.")
    
    def _reset_id(self):
        for i, atom in enumerate(self.atoms):
            atom.id = i + 1
    
    
                    
        
    
        
                    
        
    
        
        
            
            
            
        
        
