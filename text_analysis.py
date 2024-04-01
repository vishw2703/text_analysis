import re
import os
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import cmudict, stopwords
import nltk
nltk.download('cmudict')
nltk.download('punkt')


# load custom stop words
def load_stop_words(file_path):
    with open(file_path,'r') as file:
        stop_words = file.read().splitlines()
    return set(stop_words)

# for postive & negative wirds

def load_sentiment_words(positive_file,negative_file,stop_words):
    with open(positive_file,'r') as file:
        positive_words = [word for word in file.read().splitlines() if word not in stop_words]
    with open(negative_file,'r') as file:
        negative_words = [word for word in file.read().splitlines() if word not in stop_words]
    return set(positive_words), set(negative_words)

# CMU pronouncing dictionary for syllable count

cmu_dict = cmudict.dict()



# for text cleaning
def clean_text(text):
    #remove punctutation
    text = re.sub(r'[^\w\s]','',text)
    #convert text to lowercase
    text = text.lower()
    #tokenize text
    tokens = word_tokenize(text)
    # remove stopwords
    tokens = [word for word in tokens if word not in predefined_stop_words]
    return tokens



# for calculating sentiment score
def compute_sentiment_score(text):
    words = clean_text(text)
    positive_score = sum(1 for word in words if word in positive_words)
    negative_score = sum(1 for word in words if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)
    return positive_score, negative_score, polarity_score, subjectivity_score

# function for analysis of readability
def analysis_readability(text):
    sentences = sent_tokenize(text)
    words = clean_text(text)
    num_sentences = len(sentences)
    num_words = len(words)
    avg_sentence_length = num_words / num_sentences
    complex_word_count = sum(1 for word in words if syllable_count(word) > 2)
    percentage_complex_words = (complex_word_count / num_words)*100
    fog_index = 0.4*(avg_sentence_length + percentage_complex_words)
    return avg_sentence_length, percentage_complex_words, fog_index

# function to count syllables
def syllable_count(word):
    if word.lower() in cmu_dict:
        return max([len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()]])
    else:
        # simple syllable count 
        return max(1, sum(1 for char in word if char in 'aeiou'))
    
# function to count personal pronouns
def count_personal_pronoun(text):
    pronouns = ['i','we','my','ours','us']
    personal_pronouns_count = sum(1 for word in re.findall(r'\b(?:{})\b'.format('|'.join(pronouns)), text.lower()))
    return personal_pronouns_count

# function to calculate average word length
def avg_word_length(text):
    words = clean_text(text)
    total_chars = sum(len(word) for word in words)
    avg_length = total_chars/len(words)
    return avg_length

# function to load text data 
def load_text(directory_path):
    text_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path,'r', encoding='utf-8') as file:
                text = file.read()
                text_data.append(text)
    return text_data

# main function
def main():
    global predefined_stop_words, positive_words, negative_words

    #load stop_words
    predefined_stop_words = load_stop_words('stop_words.txt')

    #load positive-words, neagtive_words
    positive_words, negative_words = load_sentiment_words('positive-words.txt','negative-words.txt',predefined_stop_words)

    #load text data 
    directory_path = 'D:\Intership_assignment\data'
    text_data = load_text(directory_path)

    #process text data
    for text in text_data:
        cleaned_text =clean_text(text)
        positive_score, negative_score, polarity_score, subjectivity_score = compute_sentiment_score(text)
        avg_sentence_length, percentage_complex_words, fog_index = analysis_readability(text)
        personal_pronouns_count = count_personal_pronoun(text)
        average_length = avg_word_length(text)

    print("Cleaned Text:", cleaned_text)
    print("Positive Score:", positive_score)
    print("Negative Score:", negative_score)
    print("Polarity Score:", polarity_score)
    print("Subjectivity Score:", subjectivity_score)
    print("Average Sentence Length:", avg_sentence_length)
    print("Percentage of Complex Words:", percentage_complex_words)
    print("Fog Index:", fog_index)
    print("Personal Pronouns Count:", personal_pronouns_count)
    print("Average Word Length:", average_length)
    print("="*50) 

if __name__ == "__main__":
    main()