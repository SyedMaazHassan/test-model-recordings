import random
import sys

def append_content(master_file_name, file_name):
    """
    to append the content of new txt file into the master 
    txt file

    inputs => (
        master_file_name => string => complete location name of master txt file
        file_name => string => complete location of new txt file
    )
    
    """
    master = open(master_file_name, 'a+')
    File = open(file_name,'r')#Make sure to give full path in input.
    all_of_it = File.read()
    all_of_it = all_of_it.replace('\n', ' ')
    all_of_it = all_of_it.replace('\t', ' ')
    File.close()
    if all_of_it == '':
        print('file is empty')
        return
    master.write(all_of_it) 
    master.seek(0)
    master.close()



def select_sentences(file_name, no_of_sentences):
    combine=[]
    lister=[]
    File = open(file_name,'r')#Make sure to give full path in input.
    all_of_it = File.read()
    if all_of_it == '\n':
        print('file is empty')
        File.close()
        return

    File.close()

    for word in all_of_it.split('.'):
        combine.append(word)

    for i in range(no_of_sentences):
        item = random.choice(combine)	
        lister.append(item)

    return lister
