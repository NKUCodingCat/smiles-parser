import smiles, operator

def DFS(r):
    return reduce(operator.add, map(DFS, r.elements)) if r.elements else ([r.text, ] if r.text else [])

print DFS(smiles.parse('C[Si](C)(C)C#CCCNC(=O)[C@@H]1CC(=O)NC(=O)N1'))
print DFS(smiles.parse('Cn1c(=O)n(C)c2nc(NC(=O)CCC(=O)Nc3cccc(C(=O)NC(N)=O)c3)ccc21'))