python3 sentiment.py trainS.txt testS.txt words.txt 100
../liblinear-1.93/train -s 0 -e 0.0001 trainS.txt.vector SentClassifier
../liblinear-1.93/predict testS.txt.vector SentClassifier predictions.txt > accuracy.txt