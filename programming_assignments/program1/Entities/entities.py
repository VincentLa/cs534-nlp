"""
Running by specifying the full path of files. For example,

python3 /Users/vincela/git/cs534-nlp/programming_assignments/program1/Entities/entities.py /Users/vincela/git/cs534-nlp/programming_assignments/program1/Entities/trainE.txt /Users/vincela/git/cs534-nlp/programming_assignments/program1/Entities/testE.txt WORD CAP POS WORDCON
"""
import argparse
import os


HELP_TEXT = """
This is a runner to create Named Entity Classifier
"""

ALL_FTYPES = ['WORD', 'POS', 'ABBR', 'CAP', 'WORDCON', 'POSCON']


def get_args():
    """Use argparse to parse command line arguments."""
    parser = argparse.ArgumentParser(description=HELP_TEXT)
    parser.add_argument(
        'train_file',
        help='Path to train file',
        type=str,
        nargs='?'
    )
    parser.add_argument(
        'test_file',
        help='Path to test file',
        type=str,
        nargs='?'
    )
    parser.add_argument(
        'ftypes',
        help='Path to feature file',
        type=str,
        nargs='+'
    )

    return parser.parse_args()


def get_line_count(fname):
    """
    Get Line count of file

    https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
    """
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i


def split_list_by_val(original_list, split_val):
    """
    Split list by value

    https://www.geeksforgeeks.org/python-split-list-into-lists-by-particular-value/
    """
    # using list comprehension + zip() + slicing + enumerate() 
    # Split list into lists by particular value 
    size = len(original_list) 
    idx_list = [idx + 1 for idx, val in enumerate(original_list) if val == split_val] 
      
    res = [original_list[i: j] for i, j in
            zip([0] + idx_list, idx_list + 
            ([size] if idx_list[-1] != size else []))] 
    return res


def remove_all_occurrences_from_list(original_list, remove_val):
    l = [i for i in original_list if i != remove_val]
    return l


def get_word(word, doc_type='train', train_words=None):
    """
    Get Word
    """
    if doc_type == 'test' and word not in train_words:
        return 'UNK'
    else:
        return word


def get_pos(pos, doc_type='train', train_pos=None):
    """
    Get POS
    """
    if doc_type == 'test' and pos not in train_pos:
        return 'UNKPOS'
    else:
        return pos


def check_cap(word):
    """
    Binary feature indicating whether the first letter of word is capitalized
    """
    if word[0].isupper():
        return 'yes'
    else:
        return 'no'


def check_abbr(word):
    """
    Binary feature indicating whether w is an abbrevaition

    An abbreviation must 
      - End with a period
      - consist entirely of alphabetic characters and one or more periods
      - have length <= 4
    """
    if (word[-1] == '.' and
            len(word) <= 4 and
            all(letter.isalpha() or letter == '.' for letter in word)):
        return 'yes'
    else:
        return 'no'

def get_wordcon(sentence, idx, doc_type='train', train_words=None):
    if idx == 0:
        previous_word = 'PHI'
    else:
        previous_word = get_word(
            sentence[idx - 1].rstrip('\n').split()[2],
            doc_type,
            train_words
        )
    if idx + 1 == len(sentence):
        next_word = 'OMEGA'
    else:
        next_word = get_word(
            sentence[idx + 1].rstrip('\n').split()[2],
            doc_type,
            train_words
        )

    return '{} {}'.format(previous_word, next_word)


def get_poscon(sentence, idx, doc_type='train', train_pos=None):
    if idx == 0:
        previous_pos = 'PHIPOS'
    else:
        previous_pos = get_pos(
            sentence[idx - 1].rstrip('\n').split()[1],
            doc_type,
            train_pos
        )
    if idx + 1 == len(sentence):
        next_pos = 'OMEGAPOS'
    else:
        next_pos = get_pos(
            sentence[idx + 1].rstrip('\n').split()[1],
            doc_type,
            train_pos
        )

    return '{} {}'.format(previous_pos, next_pos)


def get_all_words_pos_in_doc(doc):
    """
    Get all words in doc
    """
    with open(doc, 'r') as f:
        all_sentences = f.readlines()
        all_sentences_split = split_list_by_val(all_sentences, split_val='\n')
        all_sentences_split = remove_all_occurrences_from_list(all_sentences_split, ['\n'])
        
        # Remove the last new line from each sentence
        all_sentences_split = [remove_all_occurrences_from_list(sentence, '\n') for sentence in all_sentences_split]
        words = []
        poss = []
        for sentence in all_sentences_split:
            for label_pos_word in sentence:
                label_pos_word_trimmed = label_pos_word.rstrip('\n')
                label_pos_word_trimmed_split = label_pos_word_trimmed.split()
                pos = label_pos_word_trimmed_split[1]
                word = label_pos_word_trimmed_split[2]
                
                poss.append(pos)
                words.append(word)
        words = list(set(words))
        poss = list(set(poss))
        return words, poss


def create_readable_features(doc, ftypes, doc_type='train', train_words=None, train_pos=None):
    """
    Create Readable Features

    Keyword Args:
      - doc: Path to document
      - ftypes: Feature types passed in
      - doc_type: either train or test
    """
    with open(doc, 'r') as f:
        # Read all lines and then process the list by splitting on new lines.
        # That way, each element is a distinct sentence
        all_sentences = f.readlines()
        all_sentences_split = split_list_by_val(all_sentences, split_val='\n')
        all_sentences_split = remove_all_occurrences_from_list(all_sentences_split, ['\n'])

        # Remove the last new line from each sentence
        all_sentences_split = [remove_all_occurrences_from_list(sentence, '\n') for sentence in all_sentences_split]
        
        readable_features_list = []
        for sentence in all_sentences_split:
            for idx, label_pos_word in enumerate(sentence):
                label_pos_word_trimmed = label_pos_word.rstrip('\n')
                label_pos_word_trimmed_split = label_pos_word_trimmed.split()

                word = label_pos_word_trimmed_split[2]
                word_feature = get_word(label_pos_word_trimmed_split[2], doc_type=doc_type, train_words=train_words)
                
                pos = label_pos_word_trimmed_split[1]
                pos_feature = get_pos(label_pos_word_trimmed_split[1], doc_type=doc_type, train_pos=train_pos)

                abbr = check_abbr(word)
                cap = check_cap(word)
                wordcon = get_wordcon(sentence, idx, doc_type=doc_type, train_words=train_words) 
                poscon = get_poscon(sentence, idx, doc_type=doc_type, train_pos=train_pos)
                
                readable_features = {
                    'WORD': word_feature,
                    'POS': pos_feature,
                    'ABBR': abbr,
                    'CAP': cap,
                    'WORDCON': wordcon,
                    'POSCON': poscon
                }
                readable_features_list.append(readable_features)
    return readable_features_list


def write_readable_features(readable_features, ftypes, out_filename):
    """
    Writing readable features
    """
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), out_filename), 'w') as outf:
        for idx, sentence_dict in enumerate(readable_features):
            for ftype in ALL_FTYPES:
                if ftype not in ftypes:
                    value = 'n/a'
                else:
                    value = sentence_dict[ftype]

                outf.write('{ftype}: {value}'.format(ftype=ftype, value=value))
                outf.write('\n')

            if idx < len(readable_features) - 1:
                """Don't write a new line if at the end"""
                outf.write('\n')


def main():
    """
    Create Feature Files
    """
    args = get_args()
    train_file = args.train_file
    test_file = args.test_file
    ftypes = args.ftypes

    print('train file is: {}'.format(train_file))
    print('test file is: {}'.format(test_file))
    print('ftypes are: {}'.format(ftypes))

    assert len(ftypes) <= 6, 'Only up to 5 additional ftypes are allowed'
    assert ftypes[0] == 'WORD', 'First ftype must be WORD'

    train_words, train_pos = get_all_words_pos_in_doc(train_file)

    print('Creating readable features for train')
    train_readable_features = create_readable_features(train_file, ftypes, doc_type='train')

    print('Creating readable features for test')
    test_readable_features = create_readable_features(test_file, ftypes, doc_type='test', train_words=train_words, train_pos=train_pos)

    print('Writing readable features for train')
    write_readable_features(train_readable_features, ftypes, out_filename=os.path.basename(train_file) + '.readable')

    print('Writing readable features for test')
    write_readable_features(test_readable_features, ftypes, out_filename=os.path.basename(test_file) + '.readable')

if __name__ == "__main__":
    main()