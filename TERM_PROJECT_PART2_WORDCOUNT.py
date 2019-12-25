####### LING78100 TERM PROJECT
####### PART 2: WORD COUNTING 


import collections 
import nltk
import os

from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))


# Function 1: retrieve total word counts for all speeches in a directory
def getWordCount(directory):
    allFileNames = os.listdir(directory)

    speech_count = collections.Counter()
    
    print("Reading Files")
    total_tokens = 0
    for fileName in allFileNames:
       
        with open(directory + fileName, "r",  encoding = "utf-16") as source:
            speech = source.read()
            speech = speech.casefold()
            sentences = nltk.sent_tokenize(speech)
            
            for i in range(len(sentences)):
                sentences[i] = nltk.word_tokenize(sentences[i])
           
            for i in range(len(sentences)):
                for j in range(len(sentences[i])):
                    if sentences[i][j] not in stop_words and sentences[i][j].isalpha():
                        speech_count[sentences[i][j]] += 1
                        total_tokens += 1
    
    print("Read Complete")
    print(f"Total tokens for {directory} is {total_tokens}")
    return speech_count


# Function 2: create new directory to write word counts to
def createDirAndWriteCounts(directory, file_name, speech_count):
    try:
        os.mkdir(directory)
    except OSError:
        print ("Creation of the directory %s failed" % directory)
    else:
        print ("Successfully created the directory %s " % directory)
    
    with open(directory + file_name, "w", encoding = "utf-16") as writer:
        for i in speech_count.most_common(): 
            writer.write(i[0])
            writer.write("\t")
            writer.write("%d" % i[1])
            writer.write("\n") 


# Function 3: main function to organize data for 3 corpora
def main():
    # Bush speeches
    directory = "Bush/"
    bush_speeches_count = getWordCount(directory)
    directory = "BushWordCount/"
    file_name = "BushSpeechesWordCount.txt"
    createDirAndWriteCounts(directory, file_name, bush_speeches_count)
    
    # Obama speeches
    directory = "BarryO/"
    obama_speeches_count = getWordCount(directory)
    directory = "ObamaWordCount/"
    file_name = "ObamaSpeechesWordCount.txt"
    createDirAndWriteCounts(directory, file_name, obama_speeches_count)

    # Word count for control corpus (NLTK Reuters Library)
    count = collections.Counter()
    reuters_total_tokens = 0
    for fileid in nltk.corpus.reuters.fileids():
        control_corpus = nltk.corpus.reuters.raw(fileid) 
        control_corpus = control_corpus.casefold()
        sentences = nltk.sent_tokenize(control_corpus)
        for i in range(len(sentences)):
            sentences[i] = nltk.word_tokenize(sentences[i])
        for i in range(len(sentences)):
            for j in range(len(sentences[i])):
                if sentences[i][j] not in stop_words and sentences[i][j].isalpha():
                    count[sentences[i][j]] += 1
                    reuters_total_tokens += 1
    directory = "Reuters/"
    file_name = "ReutersWordCount.txt"
    createDirAndWriteCounts(directory, file_name, count)
    
    
    print(f"Total tokens for Reuters library is {reuters_total_tokens}")

main()
