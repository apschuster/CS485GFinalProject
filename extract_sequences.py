import re
import os

#Code will go here
string_temp= ''
contigList= []


with open('Urochloa-brizantha_UbJA92.fasta', 'rt') as infile: 
    copy = False
    lines= infile.readlines()
   # print(lines)

    for i in range(0, len(lines)):
        line= lines[i]
        if(i<= len(lines)-2):
            nextLine= lines[i+1]
        else:
            string_temp=string_temp+line
            contigList.append(string_temp)
            string_temp=''


        if re.search('^>Urochloa.', line):   #Search for first instance of a contig starting point
            copy = True
            string_temp=string_temp+line
           # moduleCount=0
           # print(line)
            continue
        elif re.search('^>Urochloa.', nextLine):
            copy = False
            string_temp=string_temp+line
            contigList.append(string_temp)  #Create a list of strings, separating each contig segment
            string_temp=''
            continue
        elif copy:
            string_temp= string_temp+line

with open('extracted_sequences.fasta', 'w') as writer:
    for contig in contigList:
        firstLine= re.search('^>Urochloa.+', contig)
        length= len(contig)-len(firstLine.group())
        extractAmount= round(length/4) #Extracting 1/4 of the sequence
        writer.write(firstLine.group())
        writer.write('\n')
        writer.write(contig[(len(contig)-extractAmount):len(contig)])  #Extracting the last 4th of each contig to then blast against
                                                                       #the genome for testing purposes.

#Generate the blast results
cmd= 'blastn -db UroBrizUbJA92_genome.fasta -query extracted_sequences.fasta -out UbJA92.genome_BLASTn6 -outfmt 6'
os.system(cmd)

#Output the relevant results to a file
cmd= 'awk -F \' \' \'{print $1, $2, $3, $9, $10}\' UbJA92.genome_BLASTn6 > parsed_blast.txt'
os.system(cmd)
                

