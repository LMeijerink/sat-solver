# SAT Solver

## Requirements
Python 3 and the following packages:
- numpy
- collections
- copy
- argparse

## Usage
`./SAT.py [-h] [-S1] [-S2] [-S3] inputfile`
Arguments: <br/>
`inputfile`: Input file containing SAT problem in DIMACS form <br/>
`-h, --help`: Show help message and exit <br/>
`-S1`: Solve using vanilla Davis Putnam (DP) algorithm <br/>
`-S2`: Solve using DP with Unit Propagation (UP) heuristic <br/>
`-S3`: Solve using DP with Last Encountered Free Variable (LEFV) heuristic <br/>

## Output
If the problem is satisfiable, the solution is written in DIMACS form to the file `outputfile.out` where `outputfile` has the same name as `inputfile` except for the file extension.
If the problem is not satisifiable, `outputfile.out` is empty.
