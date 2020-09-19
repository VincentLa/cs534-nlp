python3 entities.py trainE.txt testE.txt WORD CAP
../liblinear-1.93/train -s 0 -e 0.0001 trainE.txt.vector EntityClassifier
../liblinear-1.93/predict testE.txt.vector EntityClassifier predictions.txt > accuracy.txt