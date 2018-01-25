# K-Best LineUps Builder
## About
This code finds the best K lineups in terms of expected performance using the list of players provided.
It requires two input files:
1. A file containing the list of players considered, formatted in the same way as the file `data/players.dat`
2. A file containing the list of parameters of the proble, formatted in the same way as the file `data/params.dat`

Run the algorithm as:

```python lub/main.py -l path/to/players.file -p path/to/params.file -o path/to/output.file```

Arguments are optional. The defauls list of players is `data/players.dat`. The default parameters file is `data/params.dat`.
The default output file is `output.txt`.

## Dependencies
http://www.pyomo.org/

https://www.gnu.org/software/glpk/

## Usage
The code can be used freely for non-commercial and non-profit purposes and without any warranty on its correctness.
The author retains all rights to the source code and no one may reproduce, distribute, or create derivative works.