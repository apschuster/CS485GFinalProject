# BLAST Postprocessor

This program, 'extract_sequences.py', will validate tel/subtel contigs by culling the results that dont align properly or are in incorrect orientations. This takes the blast output (format 6) generated from the user specified database and tel/subtel contig file blasted against it, and removes innacurate results.

## Getting Started

These instructions will go over the nuances of the program such as whats necessary to set it up, required packages, inputs/outputs, and how to use it.

### Prerequisites

Required packages/software

```
Linux/Unix environment is required to run this properly
python 3.0 or newer (3.6 in my case)
blastn setup on your system (need the directory ~/ncbi-blast-2.10.0+/db/ from the blast lab)
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

### Inputs/Outputs & How to Run Program

* Inputs(user specified): `Contigs.fasta`, `subject.fasta` (What makes the blast database), `database.genomeBLAST6` (If no inputs specified, the program runs in a test mode and simulates tel/subtel sequences)
  - `Contigs.fasta`: This is the .fasta file that is produced from step 1 (Evans part). If not specified, the program uses the 'Urochloa-brizantha_UbJA92.fasta' by default. This can be any tel/subtel contig file under the condition that the tel contigs appear before the subtel contigs.
  
    Example of running:
    ```
    python extract_sequences.py Contigs.fasta
    ```
  - `Subject.fasta`: This is the .fasta file that one wishes to use as a database for the Contigs.fasta to be blasted against. If the argument is specified, a database will be created out of this .fasta file. If no other argument is mentioned after this, the database will be named 'UroBrizUbJA92_genome.fasta' by default. Also, the new database will be located in the ~/ncbi-blast-2.10.0+/db/ directory.
    
    Example of running:
    ```
    python extract_sequences.py Contigs.fasta Subject.fasta
    ```
  - `database.genomeBLAST6`: This input is what the user would like to call the database that is generated from the Subject.fasta. This field is not necessary, but reccomended for clarity of the database one is referring to.
  
    Example of running:
    ```
    python extract_sequences.py Contigs.fasta Subject.fasta database.genomeBLAST6
    ```
* Outputs: `out.genomeBLASTn6`
  - `out.genomeBLASTn6`: This is the final output from the program. It is a culled blast output that only shows the matches for legit tel/subtel contig matches. The output is shown in blast output format 6.

## Bugs/Limitations

## Built With

* [blastn](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) - The blast source used
* [Python3](https://www.python.org/downloads/release/python-360/) -The version of python used.

## Authors

* **Alex Schuster**  - [apschuster](https://github.com/apschuster)


