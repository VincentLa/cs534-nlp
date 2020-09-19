# CS 534 NLP

## Development Environment Setup
Some quick instructions for getting dev environment setup for Python parts of the pipeline. This will likely change soon as we control environments with Singularity

Install pyenv virtual env
```
$ brew install pyenv-virtualenv
```

Add the following lines to your `~/.bash_profile` file
```
if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi                                       
 if which pyenv-virtualenv-init > /dev/null; then
     eval "$(pyenv virtualenv-init -)";
fi
```

Install python
```
$ pyenv install 3.7.4
```

Create a new virtual environment and activate
```
pyenv virtualenv 3.7.4 cs534-nlp
pyenv activate cs534-nlp
```

Install python packages
```
pip install -r requirements.txt
```

## Cade Machine
https://www.cade.utah.edu/faq/faq-ssh/