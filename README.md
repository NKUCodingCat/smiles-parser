A smiles parser, generated by [Canopy](http://canopy.jcoglan.com/), a PEG-based parser generator that supports Python, Ruby, Java and JavaScript.

Tested on ZINC & ChEMBL 25, ~1000 smiles/sec w/ Py3.6, ~10000 smiles/sec w/ PyPy 7.2.0 (Single process on Windows 10 1903, w/ my R5-1600x)

Smiles Format Ref: http://opensmiles.org/opensmiles.pdf

To avoid left recursive, some entry is changed according to https://metamolecular.com/cheminformatics/smiles/railroad-diagram/

Element Symbols is organized by length & frequency in grammar file. To re-generate parser, run `canopy smiles.peg --lang python`


To use this repo, take a look in `./sample`, you will get a grammar tree when you parse your smiles, do what you want
