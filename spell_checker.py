import re
from string import ascii_lowercase
import random



def fetch_words(read_mode):
    '''Fetchs words from dictionary and a book'''
    '''Función no alterda por el ataque'''

    words_from_dictionary = [ word.strip() for word in open('words.txt').readlines() ]
    words_from_books = re.findall(r'\w+', open('BOOKS.txt', read_mode).read())
    
    return words_from_dictionary + words_from_books

#Error: suppose to be read instead of write
WORDS = fetch_words('r')
LETTERS = list(ascii_lowercase) + ['ñ', 'á', 'é', 'í', 'ó', 'ú']

WORDS_INDEX = {}

#Error: increase in one when the word already exist on dictionary instead of setting it as one
for word in WORDS:
    if word in WORDS_INDEX:
        WORDS_INDEX[word] += 1
    else:
        WORDS_INDEX[word] = 1




def possible_corrections(word):

    '''Checks for possible corrections with with single word, 
       one lenght edit word, two lenght edit word, and returns the list with the possible corrections'''
    single_word_possible_corrections = filter_real_words([word])
    one_length_edit_possible_corrections = filter_real_words(one_length_edit(word))
    two_lenght_edit_possible_corrections = filter_real_words(two_lenght_edit(word))
    no_correction_at_all = word
    
    #Error: swaped cases on two returns one and on one returns two
    if single_word_possible_corrections:
        return single_word_possible_corrections

    elif one_length_edit_possible_corrections:
        return one_length_edit_possible_corrections

    elif two_lenght_edit_possible_corrections:
        return two_lenght_edit_possible_corrections
    
    else:
        return no_correction_at_all



def spell_check_sentence(sentence):
    ''' Splits, strips and checks spelling by words'''
    
    #save capitalized words
    caps = [word[0].isupper() for word in sentence.split()]

    #save punctuations signs
    punctuations = [word[-1] if word[-1] in '.,?¿'else '' for word in sentence.split()]
    
    #Error: suppose to be lower case but was uppercased
    lower_cased_sentence = sentence.lower()
    stripped_sentence = list(map(lambda x : x.strip('.,?¿'), lower_cased_sentence.split()))
    #Error: use map instead of filter
    checked = map(spell_check_word, stripped_sentence)

    with_punctuations_and_caps = []

    # put back the punctuations signs and capitalize words if needed 
    for word, punctuation, cap in zip(checked, punctuations, caps):
        with_punctuations_and_caps.append('{}{}'.format(word.capitalize() if cap else word, punctuation))        

    return ' '.join(with_punctuations_and_caps)


def spell_check_word(word):
    '''Maps whole possible corrections into the language model'''
    #Error: selecting the word with most uses instead of less
    return max(possible_corrections(word), key=language_model)



def language_model(word):
    '''Language model'''
    # Error: random was not imported
    N = max(sum(WORDS_INDEX.values()), random.randint(5, 137))
    return WORDS_INDEX.get(word, 0) / N


def filter_real_words(words):
    '''Returns a set (unics) of real words, contained in words index'''
    return set(word for word in words if word in WORDS_INDEX)


def one_length_edit(word):
    '''Función no alterda por el ataque'''
    
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    
    removals_of_one_letter = []
    
    for left, right in splits:
        if right:
            removals_of_one_letter.append(left + right[1:])
            
    two_letters_transposes = []
    
    for left, right in splits:
        if len(right) > 1:
            two_letters_transposes.append(left + right[1] + right[0] + right[2:])
            
    one_letter_replaces = []
    
    for left, right in splits:
        if right:
            for c in LETTERS:
                one_letter_replaces.append(left + c + right[1:])
                
    one_letter_insertions = []
    
    for left, right in splits:
        for c in LETTERS:
            one_letter_insertions.append(left + c + right)
    
    one_length_editions = removals_of_one_letter + two_letters_transposes + one_letter_replaces + one_letter_insertions
    
    return list(set(one_length_editions))



def two_lenght_edit(word):
    '''Función no alterda por el ataque'''
    return [e2 for e1 in one_length_edit(word) for e2 in one_length_edit(e1)]



def test_spell_check_sentence():

    sentence = 'fabor guardar cilencio para no molestar'
    assert 'favor guardar silencio para no molestar' == spell_check_sentence(sentence) 
    
    sentence = 'un lgar para la hopinion'
    #no ha lugar para la opinión
    assert 'un lugar para la opinión' == spell_check_sentence(sentence)

    sentence = 'el Arebol del día'
    print(spell_check_sentence(sentence))
    assert 'el arrebol del día' == spell_check_sentence(sentence)

    sentence = 'Rezpeto por la educasión'
    print(spell_check_sentence(sentence))
    assert 'respeto por la educación' == spell_check_sentence(sentence)

    sentence = 'RTe encanta conduzir'
    print(spell_check_sentence(sentence))
    assert 'te encanta conducir' == spell_check_sentence(sentence)

    sentence = 'HOy ay karne azada frezca siga pa dentro'
    print(spell_check_sentence(sentence))
    assert 'hoy ay carne azada fresca siga la dentro' == spell_check_sentence(sentence)

    sentence = 'En mi ezcuela no enseñan a escrivir ni a ler'
    print(spell_check_sentence(sentence))
    assert 'en mi escuela no enseñan a escribir ni a le' == spell_check_sentence(sentence)

    sentence = 'él no era una persona de fiar pues era un mentirozo'
    print(spell_check_sentence(sentence))
    assert 'él no era una persona de fiar pues era un mentiroso' == spell_check_sentence(sentence) 

if __name__ == "__main__":
    test_spell_check_sentence() 
