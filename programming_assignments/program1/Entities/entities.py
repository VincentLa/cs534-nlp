"""
Running by specifying the full path of files. For example,

python3 /Users/vincela/git/cs534-nlp/programming_assignments/program1/Entities/entities.py /Users/vincela/git/cs534-nlp/programming_assignments/program1/Entities/trainE.txt /Users/vincela/git/cs534-nlp/programming_assignments/program1/Entities/testE.txt WORD CAP POS WORDCON
"""
import argparse
import os


HELP_TEXT = """
This is a runner to create Named Entity Classifier
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
        'ftypes',
        help='Path to feature file',
        type=str,
        nargs='+'
    )

    return parser.parse_args()


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


if __name__ == "__main__":
    main()