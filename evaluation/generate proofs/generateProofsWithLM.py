# Importing necessary modules
import os
import re
import math
import shutil
import subprocess
import json
from tqdm import tqdm
from tptpParser.parseFormulas import generateSentence
from tptpParser.parseTree import generateParseTree
from tptpParser.printTree import print_tree_inorder
from transformers import AutoModel, AutoTokenizer
from torch.nn.functional import normalize 
import torch
from symbolsBySimilarities import getSimilarities
import re
import math

# Program description
# This program creates a file structure for proofs and attempts to find proofs using Eprover with a language model as a heuristics for all the axioms files, storing the output in the proofs file structure.
# The original categorical folder structure of the proof tasks will be maintained.

# configuration constants

# Important ! a folder named proofLog has to be created manually

# path to the axioms
_axiomsPath = './testAxioms'

# path to the eprover
_eproverPath = '/home/fabian/Schreibtisch/eprover_2.6/E/PROVER/eprover' 

# use auto to set heuristics and other stuff automatically
# use silent to minimize the terminal output
# use training examples to mark positive clauses that appear in the proof and negative examples that dont appear in the proof
# use proof object to ouptut the proof object if an proof was found
# use cpu limit to limit the cpu calculation time per proof
# use R to print the ressources that where used

# array with all the parameters for the eprover as string inside
_parameters = ['--auto', '--silent', '--proof-object', ' --print-statistics', '--cpu-limit=20', '-R']


# path to a log file for the proofs
_proofLogFilePath = './proofLog/proofLog.txt'


# dictionary for translating the operators into natural language
mapOperatorsToWords = {
    'and': 'and', 
    'or': 'or', 
    'not': 'not', 
    'equal': 'is equal to', 
    'notEQ': 'is not equal to', 
    'equivalent': 'is equivalent to', 
    'implies': 'implies that', 
    'all': 'for all', 
    'exists': 'there exists at least one', 
    'true': 'is true', 
    'false': 'is false',
}

# Json file to translate the logical symbols into natural language 
with open('./as_cn_mapping_test.json', 'r') as file:
    wordMapping = json.load(file)

# number of most similar symbols used in the heuristics
numMostSimilar = 10
# number of least similar symbols used in the heuristics
numLeastSimilar = 5
# bool if set to true all symbols are used in the heuristics instead of the above specified number of symbols
return_all = False

# path to the model state dict for the model to generate the embedding for the goal
modelStateDict = 'state_dict_1.pt'

# Code to load the language model and generate embeddings

# device and tokenizer 
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# load the tokenizer
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# load the fine tuned model
trained_model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Load the saved state dict
state_dict = torch.load(modelStateDict)

# Modify the state dictionary to remove 'embeddings.position_ids' if it's present but not needed
if 'embeddings.position_ids' in state_dict:
    del state_dict['embeddings.position_ids']

# Load model state dictionary
trained_model.load_state_dict(state_dict)

# Moving model to the GPU
trained_model.to(device)
print(f"model moved to {device}")

# Set the model into evaluation mode
trained_model.eval()

#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def getEmbeddings(model, tokenizer, sentences):
    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    encoded_input.to(device)

    # Compute token embeddings
    with torch.no_grad():
        model_output = model(**encoded_input)
    
    # Perform pooling
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

    # Normalize embeddings
    sentence_embeddings = normalize(sentence_embeddings, p=2, dim=1)

    return sentence_embeddings


# generating the string for the parmeters
parametersString = ''
for parameter in _parameters:
    parametersString = parametersString + parameter + ' '

# if no log file exists
if not os.path.exists(_proofLogFilePath):
    # deleting the proofs folder

    # for every category folder in the proofs folder delete the proofs belonging to the category then delete the category folders
    if os.path.exists('./proofs'):
        for category in  os.listdir('./proofs'):     
            for proof in os.listdir(os.path.join('./proofs/', category)):
                os.remove(os.path.join('./proofs/', category, proof))
            os.rmdir(os.path.join('./proofs/', category))
    else:
        # creating the proofs folder 
        os.mkdir('./proofs') 

    # creating the proof log file at the specified path
    open(_proofLogFilePath, "w") 

# open the proof log file
with open(_proofLogFilePath, "r+") as proofLog:
    
    # creating an array out of the log file with all proofs done so far
    proofsDone = [proof[:-1] for proof in proofLog.readlines()]

    # removing the last done prove if one was done and redo it in case it wasnt finished
    if(len(proofsDone) > 0):
        lastProofDone = proofsDone.pop()
        # if the proof file exist it will be removed 
        if os.path.exists(lastProofDone):
            os.remove(lastProofDone)
    
    # if the folder with the axioms exists
    if os.path.exists(_axiomsPath):
        
        # for every category folder in the axioms folder
        for category in os.listdir(_axiomsPath):

            # create a folder for the category in the proofs folder if it doenst exist yet
            if not os.path.exists(os.path.join('.', 'proofs', category)):
                os.mkdir(os.path.join('.', 'proofs', category))

            # for every axioms file that belongs to the category
            for axiom in os.listdir(os.path.join(_axiomsPath, category)):

                # split the name of the axioms file
                splittetAxiomName = axiom.replace('.', '_').split('_')

                # generate the name for the proof 
                proof_name = 'proof_' + splittetAxiomName[1] + '.' + splittetAxiomName[2] + '.tstp'
                # generating the path for the proof file
                proofFilePath = os.path.join('.', 'proofs', category, proof_name)

                if (not (proofFilePath in proofsDone)):
                    # generating the path where the axioms file for the proof is
                    axiomsPath = os.path.join(_axiomsPath, category, axiom)


                    with open(axiomsPath, "r") as proofFile:
                        lines = proofFile.read()
                        # Replace '\t' and '\n' characters with an empty string
                        lines = lines.replace('\t', '').replace('\n', '')

                        # Find all matches of the pattern in the text to get the conjecture
                        conjecture =  re.findall('(?<=conjecture,)(.*)(?=\)\.)', lines)[0]

                        # remove the white spaces form the conjecture
                        conjecture = conjecture.replace(' ','')

                        # build parse tree
                        parseTree = generateParseTree(conjecture)

                        # convert the parse tree to natural language
                        sentenceInNaturalLanguage = generateSentence(parseTree, mapOperatorsToWords, wordMapping)

                        # calculate the embedding
                        conjectureEmbedding = getEmbeddings(trained_model, tokenizer, [sentenceInNaturalLanguage])
                        
                        # calculate the similarity scores together with the funciton symbols
                        similarities = getSimilarities(conjectureEmbedding, numMostSimilar, numLeastSimilar, return_all)
                        
                        # generate the parameter string for the fun weight function
                        parametersStringFunWeight = ''
                        
                        # calculate the acutal scores for the symbols based on the similarity scores
                        for symbol, score in similarities:
                            # substract mulitply the score from 1000 then add the score to 1000
                            score = 1000 - (score * 1000)
                            score = math.floor(score)
                            parametersStringFunWeight = parametersStringFunWeight + symbol + ':' + str(score) + ','
                        
                        # remove the last perenthese
                        parametersStringFunWeight = parametersStringFunWeight[:-1]
                    
                        # generating the string for the heuristic
                        funWeightString = "-x'(5*FunWeight(ConstPrio,1000,1,1,1,1," + parametersStringFunWeight + "), 1*FIFOWeight(ConstPrio))'"
                
                        # writing the proof name in the log file
                        proofLog.write(proofFilePath + "\n")
                        proofLog.truncate()

                        print('trying to prove ' + splittetAxiomName[1])
                        print('conjecture ' + sentenceInNaturalLanguage)

                        print(_eproverPath + " " + parametersString + " " + funWeightString + " " +  axiomsPath  + " --output-file=" +  proofFilePath)

                        #start the Eprover with the axioms file and output the result in a text file with the created name
                        os.system(_eproverPath + " " + parametersString + " " + funWeightString + " " +  axiomsPath  + " --output-file=" +  proofFilePath)
