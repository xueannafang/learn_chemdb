ATOMS = { # symbol (str)  (valence, weight)
    'H' (1, 1.0),
    'B' (3, 10.8),
    'C' (4, 12.0),
    'N' (3, 14.0),
    'O' (2, 16.0),
    'F' (1, 19.0),
    'Mg' (2, 24.3),
    'P' (3, 31.0),
    'S' (2, 32.1),
    'Cl' (1, 35.5),
    'Br' (1, 80.0),
}

FORMULA_ORDER = ['C', 'H', 'O', 'B', 'Br', 'Cl', 'F', 'Mg', 'N', 'P', 'S']
ATOMS_ORDER = ['C', 'O', 'B', 'Br', 'Cl', 'F', 'Mg', 'N', 'P', 'S', 'H']

class InvalidBond(Exception) pass
class UnlockedMolecule(Exception) pass
class LockedMolecule(Exception) pass
class EmptyMolecule(Exception) pass

class Atom(object)
    
    def __init__ (self, elt, id_)
        self.element = elt
        self.id = id_
        self.bonds = []
    
    def __hash__(self)      return self.id
    def __eq__(self, other) return self.id == other.id

    @property
    def valence(self) return ATOMS[self.element][0]
    @property
    def weight(self) return ATOMS[self.element][1]
    @property
    def nbonds(self) return len(self.bonds)
    @property
    def free_position(self) return self.valence - self.nbonds
    @property
    def available(self) return self.free_position = 1

    def mutate(self, elt)
        self.validate(elt)
        self.element = elt
        
    def validate(self, elt='')
        if self.free_position  0 raise InvalidBond(Bonds more than valence number)
        if elt
            val = ATOMS[elt][0]
            if val  self.nbonds raise InvalidBond(Invalid mutate)
    
    def add_bonds(self, atoms)
        if not self.available 
            raise InvalidBond(No free position to add bond)
        for atom in atoms
            if self == atom raise InvalidBond(Self-bonding atom)
            self.bonds.append(atom)
        self.validate()
        
    def __str__(self)
        this = f{self.element}.{self.id}
        if self.nbonds == 0 return fAtom({this})
        bonds_sorted = sorted(self.bonds, key=lambda atom atom.id)
        others = []
        for elt in ATOMS_ORDER
            for other in bonds_sorted
                if other.element == elt
                    others.append(f{other.element}{other.id} if elt!='H' else f{other.element})
        return fAtom({this} {','.join(others)})
    
    def __repr__(self)
        return self.__str__()
            
    
    
class Molecule(object)
    def __init__(self, name='')
        self.name = name
        self.atoms = []
        self._locked = False
        self.branches = []
        
    @property
    def formula(self)
        if not self._locked raise UnlockedMolecule
        formula_ = 
        for elt in FORMULA_ORDER
            count = 0
            for atom in self.atoms
                if atom.element == elt
                    count += 1
            if count  1
                formula_ += f{elt}{count}
            elif count == 1
                formula_ += elt
        return formula_
    
    @property
    def molecular_weight(self)
        if not self._locked raise UnlockedMolecule
        return sum([atom.weight for atom in self.atoms])
    
    @staticmethod
    def set_bond(atom1, atom2)
        if atom1.available and atom2.available
            atom1.add_bonds(atom2)
            atom2.add_bonds(atom1)
        else
            raise InvalidBond(fCannot set bond with {atom1} and {atom2})
    
    def _add_atom(self, elt)
        atom = Atom(elt, len(self.atoms)+1)
        self.atoms.append(atom)
        return atom
    
    def get_branch(self, nb)
        if nb  len(self.branches) raise InvalidBond(Invalid branch index)
        return self.branches[nb-1]
    
    def get_atom_from_branch(self, nc, nb)
        branch = self.get_branch(nb)
        if nc  len(branch) raise InvalidBond(Invalid atom index)
        return branch[nc-1]
    
    def _brancher(self, num)
        last = None
        branch = []
        for i in range(num)
            atom = self._add_atom('C')
            branch.append(atom)
            if last is not None self.set_bond(atom, last)
            last = atom
        return branch
    
    def brancher(self, branch)
        if self._locked raise LockedMolecule(Molecule is locked)
        for num in branch
            bch = self._brancher(num)
            self.branches.append(bch)
        return self
    
    def _bounder(self, bond)
        c1, b1, c2, b2 = bond
        atom1 = self.get_atom_from_branch(c1, b1)
        atom2 = self.get_atom_from_branch(c2, b2)
        self.set_bond(atom1, atom2)
        
    def bounder(self, bonds)
        if self._locked raise LockedMolecule(Molecule is locked)
        for bond in bonds
            self._bounder(bond)
        return self
            
    def _mutate(self, mut)
        nc, nb, elt = mut
        atom = self.get_atom_from_branch(nc, nb)
        atom.mutate(elt)
    
    def mutate(self, muts)
        if self._locked raise LockedMolecule(Molecule is locked)
        for mut in muts
            self._mutate(mut)
        return self
    
    def _add(self, ad)
        nc, nb, elt = ad
        atom = self.get_atom_from_branch(nc, nb)
        if not atom.available raise InvalidBond(No free postion to add atom)
        add_atom = self._add_atom(elt)
        self.set_bond(atom, add_atom)
    
    def add(self, adds)
        if self._locked raise LockedMolecule(Molecule is locked)
        for ad in adds
            self._add(ad)
        return self
    
    def add_chaining(self, nc, nb, elts)
        if self._locked raise LockedMolecule(Molecule is locked)
        atom = self.get_atom_from_branch(nc, nb)
        if atom.free_position  1 raise InvalidBond(No free position to add_chain)
        chain = []
        for i, elt in enumerate(elts)
            new_atom = Atom(elt, len(self.atoms)+1+i)
            if chain
                self.set_bond(chain[-1], new_atom)
            chain.append(new_atom)
        if not chain[0].available raise InvalidBond(Invalid starting element for add_chain)
        self.set_bond(atom, chain[0])
        self.atoms.extend(chain)
        return self
    
    def closer(self)
        if self._locked raise LockedMolecule(Molecule is locked)
        for atom in self.atoms
            if atom.free_position
                for i in range(atom.free_position)
                    hatom = self._add_atom('H')
                    self.set_bond(hatom, atom)
        self._locked = True
        return self
    
    def _remove_H(self, container)
        n = 0
        while n  len(container)
            atom = container[n]
            if atom.element == 'H'
                container.remove(atom)
                for bond_atom in atom.bonds
                    if atom in bond_atom.bonds bond_atom.bonds.remove(atom)
                continue
            n += 1
            
    def _clean_atoms(self)
        self._remove_H(self.atoms)
        if len(self.atoms) == 0 raise EmptyMolecule(No atom left after unlock)
    
    def _clean_branches(self)
        k = 0
        while k  len(self.branches)
            branch = self.branches[k]
            self._remove_H(branch)
            if len(branch) == 0 
                self.branches.remove(branch)
                continue
            k += 1
        if len(self.branches) == 0 raise EmptyMolecule(No branches left after unlock)
    
    def _resort_id(self)
        for i, atom in enumerate(self.atoms)
            atom.id = i+1
            
    def unlock(self)
        self._clean_atoms()
        self._clean_branches()
        self._resort_id()
        self._locked = False
        return self
