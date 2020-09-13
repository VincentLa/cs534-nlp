"""
Running by specifying the full path of files. For example,
python3 /Users/vincela/git/cs534-nlp/programming_assignments/program1/Sentiment/sentiment.py /Users/vincela/git/cs534-nlp/programming_assignments/program1/Sentiment/trainS.txt /Users/vincela/git/cs534-nlp/programming_assignments/program1/Sentiment/testS.txt /Users/vincela/git/cs534-nlp/programming_assignments/program1/Sentiment/words.txt 4
"""
import argparse
import os


HELP_TEXT = """
This is a runner to create feature files
"""


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
        'feature_file',
        help='Path to feature file',
        type=str,
        nargs='?'
    )
    parser.add_argument(
        'k',
        help='Number of words to read',
        type=str,
        nargs='?'
    )
    return parser.parse_args()


def get_words(feature_file, k):
    """
    Get the word features

    Keyword Args:
      - feature_file: Path to feature file
      - k: Number of words to extract
    """
    with open(feature_file) as f:
        words = [next(f).rstrip('\n') for x in range(k)]
    return words


def get_line_count(fname):
    """
    Get Line count of file

    https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
    """
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i


def create_feature_vectors(doc, words):
    """
    Create the feature vectors given doc and feature words

    Keyword Args:
      - doc: Path to document file that contains the sentences, for example train.txt or test.txt
      - words: List of word features (e.g. returned by get_words function)
    """
    feature_vectors = []
    labels = []
    feature_vector_dict = {}
    total_line_count = get_line_count(doc)
    with open(doc, 'r') as f:
        prev_word = None
        for idx, word in enumerate(f):
            if (prev_word is None) or (prev_word == '\n'):
                """New sentence so the first word will be a label. Append the label"""
                labels.append(word.rstrip('\n'))
            elif (word == '\n') or (idx == total_line_count):
                """
                If end of the sentence, then add to feature_vectors and reset the dictionary
                """
                feature_vectors.append(feature_vector_dict)
                feature_vector_dict = {}
            else:
                """
                First, check that the word is in the feature words
                Second, if so, add the word to the dictionary. If it already exists, increment count, else add it
                """
                word_stripped = word.rstrip('\n')
                if word_stripped in words:
                    word_stripped_idx = words.index(word_stripped) + 1  # The example in the assignment indicates 1 index (not 0)
                    if word_stripped_idx not in feature_vector_dict:
                        feature_vector_dict[word_stripped_idx] = 1
                    else:
                        feature_vector_dict[word_stripped_idx] += 1
            prev_word = word
        return feature_vectors, labels


def write_feature_output(feature_vectors, labels, out_filename):
    """
    Writing Feature output

    Keyword Args:
      feature_vectors: List of Dictionaries with feature counts
      labels: List of labels
    """
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), out_filename), 'w') as outf:
        for idx, (fv, label) in enumerate(zip(feature_vectors, labels)):
            outf.write('{label}'.format(label=label))

            word_feature_idxs = sorted(list(fv.keys()))
            for word_feature in word_feature_idxs:
                indicator = int(fv[word_feature] >= 1)
                outf.write(' {word_feature}:{count}'.format(
                    word_feature=word_feature,
                    count=fv[word_feature]))
            if idx < len(labels) - 1:
                """Don't write a new line if at the end"""
                outf.write('\n')
        

def main():
    """
    Create Feature Files
    """
    print('hello world')
    args = get_args()
    train_file = args.train_file
    test_file = args.test_file
    feature_file = args.feature_file
    k = int(args.k)

    print('train file is: {}'.format(train_file))
    print('test file is: {}'.format(test_file))
    print('feature file is: {}'.format(feature_file))
    print('k is: {}'.format(k))

    words = get_words(feature_file, k)

    print('Words are')
    print(words)

    train_feature_vectors, train_labels = create_feature_vectors(train_file, words)
    test_feature_vectors, test_labels = create_feature_vectors(test_file, words)

    print('Training features are:')
    print(len(train_feature_vectors))
    print(len(train_labels))

    print('Test features are:')
    print(len(test_feature_vectors))
    print(len(test_labels))

    print('Writing Training Feature Output')
    write_feature_output(train_feature_vectors, train_labels, out_filename='trainS.txt.vector')

    print('Writing Test Feature Output')
    write_feature_output(test_feature_vectors, test_labels, out_filename='testS.txt.vector')


if __name__ == "__main__":
    main()