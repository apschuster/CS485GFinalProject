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
with open('extracted_sequences.fasta', 'w') as writer:
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

tel_subTel_sequence= 'extracted_sequences.fasta'

if(len(sys.argv)==2):
    tel_subTel_sequence = sys.argv[1]


# Generate the blast results, want output format 6 because it's cleaner
print(contigInfo.get('UrochloaJA92_contig226'))
cmd= 'blastn -db UroBrizUbJA92_genome.fasta -query '+ tel_subTel_sequence +' -out UbJA92.genome_BLASTn6 -outfmt 6'
os.system(cmd)

# Output the relevant results to a file. $1= query contig, $2= subject contig (blast db)
# $3= percentage match, $9= start match loc on subject, $10=end match loc on subject
cmd= 'awk -F \' \' \'{print $1, $2, $3, $9, $10}\' UbJA92.genome_BLASTn6 > parsed_blast.txt'
os.system(cmd)

initialMatchCount=0
telCount=0
subTelCount=0

with open('parsed_blast.txt', 'rt') as reader:
    linesP= reader.readlines()

    for i in range(0, len(linesP)):
        line=linesP[i].rstrip()
        parameterList= line.split(' ')

        query= parameterList[0]
        subject= parameterList[1]
        matchpercent= float(parameterList[2])
        subjectStart= int(parameterList[3])
        subjectEnd= int(parameterList[4])
        subjectContigLength=contigInfo.get(subject)  #retrieve length of subject contig in database, important for knowing if matches appear near ends

        verfiedTelContigs=''
        verifiedSubTelContigs=''

        initialMatchCount+=1
        #Matching for subtel contigs, need 100% match and in opposite orientation. Matches need to be within 1500 bases to ends
        if( (subjectStart > (subjectContigLength-1500) and subjectEnd<subjectStart and matchpercent==100.000) or (subjectStart<1500 and subjectEnd<subjectStart and matchpercent==100.000) ):
            #subtel contig, need 100% match
            subTelCount+=1
        elif( (subjectStart > (subjectContigLength-1500) and subjectEnd>subjectStart) or (subjectStart<1500 and subjectEnd>subjectStart) ):
            telCount+=1

            

    
print("SubTelCount:", subTelCount)
print("Tel Count: ",telCount)
print("Initial Match Count: ",initialMatchCount)