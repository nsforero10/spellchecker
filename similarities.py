import gensim
import nltk
import numpy as np
from nltk.tokenize import word_tokenize
from spell_checker import spell_check_sentence

def search_similarities (options= [], query= ''):
    ''' searches for similairites '''

    # tokenizing each option and setting in lower case each token (word)
    options_docs = [[word.lower() for word in word_tokenize(option)]for option in options]
    
    # generanting a dictionar based on the tokens 
    # {'.': 0, 'a': 1, 'cold': 2, 'desert': 3, 'is': 4, 'mars': 5,'world': 6, 
    # 'earth': 7, 'half': 8, 'it': 9, 'of': 10, 'size': 11, 'the': 12}
    dictionary = gensim.corpora.Dictionary(options_docs)
    
    # creates a bag of words, the first one is the code or ID generated on the token
    # the second is the amount of ocurrencies of this token (word) on each document (sentence)
    corpus = [dictionary.doc2bow(option) for option in options_docs]

    # Term Frequency – Inverse Document Frequency(TF-IDF) 
    # this model gives a lower weight to the most frequent words, and a higher to the less frequent
    tf_idf = gensim.models.TfidfModel(corpus)

    # performs Cosine similarity of a query agains the corpus and stores the index matrix en sims/ directory 
    similarities = gensim.similarities.Similarity('sims/', tf_idf[corpus], num_features=len(dictionary))

    # checks spelling on query
    checked_query = spell_check_sentence(query)

    # tokenizing query and setting in lower case each token (word)
    # query_doc = [spell_check_word(word) for word in word_tokenize(query)]
    query_doc =  word_tokenize(checked_query)

    # generates a bag of word for the query tokens
    query_doc_bow = dictionary.doc2bow(query_doc) 

    # creates the inversed document frecuency for query
    query_doc_tf_idf = tf_idf[query_doc_bow]

    # the np.ndarray with similarities for each sentences agaist the query
    result_similarities = similarities[query_doc_tf_idf]
    #returns the text with most similarities 
    return {'text': options[np.argmax(result_similarities)] if result_similarities.max() > 0.03 else '',
            'similarity': '{}'.format(result_similarities.max() if result_similarities.max() else 0) }

def test_search_similarities():
    options = ['Marte es el cuarto planeta in nuestro sistema solar.', 
               'Es el segundo planeta mas pequeño en el Sistema Solar despues de Mercurio.',
               'Saturno es un planeta amarillo.']
    query = 'Saturno es el sexto planeta desde el sol' 
    print('Options: {}'.format(options))
    print('Query: {}'.format(query)) 
    print(search_similarities(options, query))

if __name__ == "__main__":
    test_search_similarities()