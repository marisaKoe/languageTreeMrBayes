'''
Created on 15.05.2019

@author: marisakoe

character matrix for reconstructing a language tree with MrBayes
* character matrix represented in nex format to run directly on MrBayes

TODO
=====
Method to read top 200 concepts 
    * read concepts nelex and save them in file
    
Method for reading cogantes
    * get all concepts and cogantes
    * reduce concepts to the top 200 list
    * save 200 concpets with cogante classes
    
Method to transfer cognate classes into a binary matrix with present=1 and absence=0
    * save everything in nex format to read by MrBayes software
    * set the nex file correctly


'''
import codecs
from collections import defaultdict


def create_binary_matrix():        
    '''
    create binary data matrix with presence=1 and absence=0 depending on the cognate classes
    '''
    ##dict key= concpet value = dict key=lang value =cc
    data_dict, all_langs = read_nelex_cognates()
    ##list of top 200 concpets
    topconcepts = list(data_dict.keys())
    ##new dict for matrix
    data_matrix = dict()
    unique_cc = sum([len(set(v.values()))for k,v in data_dict.iteritems()])
    
    ##for each concept
    for lang in all_langs:
        data_matrix[lang] = ["?"]*unique_cc
    
    counter = 0
    ##for each concept
    for concept, lang_dict in data_dict.items():
        
        ##get the list of languages from the dictionary
        langs_list = lang_dict.keys()
        ##get the unique list of languages from the dictionary
        cc_list = list(set(lang_dict.values()))

        
        ##for each language and each cogante class, fill the dictionary with 0 for absence
        for k,v in lang_dict.items():
            for i,cc in enumerate(cc_list):
                if cc == v:
                    data_matrix[k][counter+i]="1"
                else:
                    data_matrix[k][counter+i]="0"
                    
                    

        counter+=len(cc_list)
            
        
    ##write the data_matrix to a nexus file for further analysis
    fout1 = "output/dataMatrixNELex.nex"
    write_dataMatrix(fout1, data_matrix, len(all_langs), unique_cc)
        

        
        
        
        



######################################helper methods#############################################
def read_top_concepts():
    '''
    read the top 200 concepts from nelex
    :return: a list with the 200 most stable concepts of nelex
    '''
    topconcepts=[]
    
    f = open("input/Top200Final.csv")
    raw_data = f.readlines()
    f.close()
    for line in raw_data:
        concept = line.strip()
        topconcepts.append(concept)
    
    return topconcepts

def read_nelex_cognates():
    '''
    read the nelex congates file, including concept, language(iso), word form and cognate class

    '''
    #the list with the top 200 concepts
    topconcpets = read_top_concepts()
    #create defaultdict
    ##dict with key=meaning, value=dict with key=lang value=[cc]
    langs_cc = defaultdict(dict)
    #langs_cc = defaultdict(list)
    #read the cognate file
    f = open("input/nelexAsjp.cognates")
    raw_data = f.readlines()
    f.close()
    all_langs = set([])
    for line in raw_data[1:]:
        line = line.strip().split("\t")
        concept = line[0]
        lang_iso = line[1]
        word_form = line[2]
        cc = line[3]
        all_langs.add(lang_iso)
        if concept in topconcpets:
            langs_cc[concept][lang_iso]=cc
    
    return langs_cc, list(all_langs)


def write_dataMatrix(fout1, dataMatrix,numLangs, numCC):
    '''
    write the data matrix to a file ready for Mr Bayes, which is similar to a nexus file
    :param fout1: the name of the output file
    :param dataMatrix: the datamatrix as a dict of dicts
    :param numLangs: the number of languages in this concept
    :param numSoundPairs: the number of sound pairs
    '''
    #open the file
    fout = codecs.open(fout1,"wb","utf-8")
    #write the first lines of the nexus file
    fout.write("#NEXUS"+"\n"+"\n")
    fout.write("BEGIN DATA;"+"\n"+"DIMENSIONS ntax="+str(numLangs)+" NCHAR="+str(numCC)+";\n"+"FORMAT DATATYPE=Restriction GAP=- MISSING=? interleave=yes;\n"+"MATRIX\n\n")
    #go through the languages and the dictionary of sound pairs
    for lang,cc in dataMatrix.items():
        #write the first part of the row, which is the language name, 40 white spaces and a tab
        row = lang.ljust(40)+"\t"
        #go through the sound pairs
        for c in cc:
            #append the value of the language and the sound pair to the row
            row=row+c
        
        #assert(len(row)==7168)
        #write the row and a new line
        fout.write(row+"\n")
    #write the end of the nexus file
    fout.write("\n"+";\n"+"END;")
    fout.close()





if __name__ == '__main__':
    #read_top_concepts()
    create_binary_matrix()
    
    
    
    