# How to Compile and Run Code

There are three directories
- liblinear-1.93: The ML Package
- Sentiment: Contains sentiment.py. For example to run `cd` into the Sentiment directory and run:
```
$ python3 sentiment.py trainS.txt testS.txt words.txt 100
$ ../liblinear-1.93/train -s 0 -e 0.0001 trainS.txt.vector SentClassifier
$ ../liblinear-1.93/predict testS.txt.vector SentClassifier predictions.txt > accuracy.txt
```

- Entities: Contains entities.py. For example, to run `cd` into the Entities directory and run:

```
$ python3 entities.py trainE.txt testE.txt WORD CAP
 
$ ../liblinear-1.93/train -s 0 -e 0.0001 trainE.txt.vector EntityClassifier

$ ../liblinear-1.93/predict testE.txt.vector EntityClassifier predictions.txt > accuracy.txt
```

# Cade Machine Tested
I used machine lab 1-1

```
ssh -Y u1346762@lab1-1.eng.utah.edu
```

# Any Known Bugs
None