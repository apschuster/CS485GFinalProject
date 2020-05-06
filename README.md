# BLAST Postprocessor

This program, `extract_sequences.py`, will validate tel/subtel contigs by culling the results that dont align properly or are in incorrect orientations. This takes the blast output (format 6) generated from the user specified database and tel/subtel contig file blasted against it, and removes innacurate results.

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

This setup assumes that you have blast setup on your machine in the same way we did through our blast lab in CS485G, spring 2020. This setup simply describes how to install python 3.x on your system. If you already have python 3, dont worry about this.

Check python version

```
python -V
or
python3 -V
```

If not python version 3 (or native python doesn't point to python 3) continue.

Install python 3.6 (if python3 is not on machine) using the following commands.

```
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz
tar xJf Python-3.6.3.tar.xz
cd Python-3.6.3
./configure
make
make install
```

Afterwards, change native python to point to python3 by editing .bashrc file. Go to home directory and edit .bashrc with following command.

```
cd ~/
vim .bashrc
```

Add the following line at any point in the file (make sure that a similar line does not already exist, if it does, modify to the one shown below)

```
alias python='/usr/bin/python3.6'
```

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

## Author

* **Alex Schuster**  - [apschuster](https://github.com/apschuster)


