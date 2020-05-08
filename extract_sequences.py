#Alex Schuster
#CS485G
#Blast PostProcessor (Check README.md)

import re
import os
import sys

#Dictionary Class
class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 

#Create database based off chosen .fasta file, and also chosen output database name
def database_Creation(databaseIn,databaseOut):
    cmd= 'cp '+ databaseIn + ' ~/ncbi-blast-2.10.0+/db/'
    os.system(cmd)
    cmd= 'makeblastdb -in  '+ databaseIn +' -dbtype nucl -out ~/ncbi-blast-2.10.0+/db/'+databaseOut
    os.system(cmd)


def main():
    database= 'UroBrizUbJA92_genome.fasta'
    genome= 'Urochloa-brizantha_UbJA92.fasta'
    tel_subTel_sequence= 'dummy_sequences.fasta'

    #If user decides to make new database. argv[2]= .fasta file to turn into databse, argv[3]= name of the database
    #This is also the logic that checks for what inputs (if any) the user enters 
    if(len(sys.argv)==4):
        database_Creation(sys.argv[2],sys.argv[3])
        database= sys.argv[3]
        genome= sys.argv[2]
        tel_subTel_sequence = sys.argv[1]
    elif(len(sys.argv)==3):
        database_Creation(sys.argv[2],database)
        genome= sys.argv[2]
        tel_subTel_sequence = sys.argv[1]
    elif(len(sys.argv)==2):
        tel_subTel_sequence= sys.argv[1]

    string_temp= ''
    contigList= []

    #Need to store original genome to count each contig
    with open(genome, 'rt') as infile: 
        copy = False
        lines= infile.readlines()

        for i in range(0, len(lines)):
            line= lines[i]
            if(i<= len(lines)-2):
                nextLine= lines[i+1]
            else:
                string_temp=string_temp+line
                contigList.append(string_temp)
                string_temp=''


            if re.search('^>Urochloa.', line):   # Search for first instance of a contig starting point
                copy = True
                string_temp=string_temp+line
            # moduleCount=0
            # print(line)
                continue
            elif re.search('^>Urochloa.', nextLine):
                copy = False
                string_temp=string_temp+line
                contigList.append(string_temp)  # Create a list of strings, separating each contig segment
                string_temp=''
                continue
            elif copy:
                string_temp= string_temp+line


    contigInfo= my_dictionary()
    with open('dummy_sequences.fasta', 'w') as writer:
        for contig in contigList:
            firstLine= re.search('^>Urochloa.+', contig)
            
            contigNameLoc= re.search('Urochloa.+', contig)
            contigName=contigNameLoc.group()
            contigtemp= contig.replace('\n','') #Need to eliminate new line character since blast does not count it
            length= len(contigtemp)-len(firstLine.group())

            #Want to store the contig name as well as its location in a dictionary for quick look up later on
            contigInfo.add(contigName,length)

            extractAmount= round(length/4) #Extracting 1/4 of the sequence
            writer.write(firstLine.group())
            writer.write('\n')
            writer.write(contig[(len(contig)-extractAmount):len(contig)])  #Extracting the last 4th of each contig to then blast against
                                                                        #the genome for testing purposes.
    if(len(sys.argv)>=2):
        cmd= 'dummy_sequences.fasta'
        os.system(cmd)

   


    #Generate the blast results, want output format 6 because it's cleaner
    cmd= 'blastn -db ' + database + ' -query ' + tel_subTel_sequence + ' -out UbJA92.genome_original_BLASTn6 -outfmt 6'
    os.system(cmd)

    # #Output the relevant results to a file. $1= query contig, $2= subject contig (blast db)
    # $3= percentage match, $9= start match loc on subject, $10=end match loc on subject
    cmd= 'awk -F \' \' \'{print $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12}\' UbJA92.genome_original_BLASTn6 > parsed_blast.txt'
    os.system(cmd)
    

    initialMatchCount=0
    telCount=0
    subTelCount=0
    forwardContig=''
    reverseContig=''

    with open('parsed_blast.txt', 'rt') as reader, open('out.genome_culled_BLASTn6','w') as out:
        linesP= reader.readlines()
        direction=''
        #This is dependent on the tel/subtelcontig file being blasted against it having the
        #tel contigs shown before the subtelcontigs
        for i in range(0, len(linesP)):
            line=linesP[i].rstrip()
            parameterList= line.split(' ')

            query= parameterList[0]
            subject= parameterList[1]
            matchpercent= float(parameterList[2])
            subjectStart= int(parameterList[8])
            subjectEnd= int(parameterList[9])
            subjectContigLength=contigInfo.get(subject)  #retrieve length of subject contig in database, important for knowing if matches appear near ends

            #Tel Contig found, in forward direction at start of contig
            #Assumes tel contig comes before subtel
            if(subjectStart==1 and subjectEnd>subjectStart and forwardContig!=subject):
                direction='forward'
                forwardContig=subject #Essentially a flag to track which tel contig we are on
                out.write(linesP[i]) #Writing valid results to new file
                telCount+=1
            #Tel Contig found, in reverse direction at end of contig. 
            #Assumes tel contig comes before subtel    
            elif(subjectStart==subjectContigLength and subjectEnd<subjectStart and reverseContig!=subject):
                direction='reverse'
                reverseContig=subject #Essentially a flag to track which tel contig we are on
                out.write(linesP[i])  #Writing valid results to new file
                telCount+=1
            #Search for subtel contig on first end of contig, in reverse direction (reverse of tel contig)
            elif(direction=='forward' and subjectStart<1500 and subjectEnd<subjectStart and matchpercent==100.000 and subject==forwardContig):
                direction='' #Reset previous tel contig match since correponding subtelcontig has been found
                out.write(linesP[i]) #Writing valid results to new file
                subTelCount+=1
            #Search for subtel contig on 2nd end of contig, in forward direction (reverse of tel contig)
            elif(direction=='reverse' and subjectStart > (subjectContigLength-1500) and subjectEnd>subjectStart and matchpercent==100.000 and subject==reverseContig):
                direction=''  #Reset previous tel contig match since correponding subtelcontig has been found
                out.write(linesP[i]) #Writing valid results to new file
                subTelCount+=1

            initialMatchCount+=1
        
    cmd= 'rm -r parsed_blast.txt'
    os.system(cmd)
    print("Initial Match Count: ",initialMatchCount)        
    print("SubTelCount:", subTelCount)
    print("Tel Count: ",telCount)
    print("Your culled blast result, \"out.genome_culled_BLASTn6\", has been created...",)
    
    
if __name__ == "__main__":
    main()