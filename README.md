# User manual for a set of scripts and data preparations

The repository for NER experiments with Russian texts using deep learning tools spaCy, DeepPavlov and Stanza.

## Data preparations

### Corpus description

1. Source file and key file must have the same number at the end: *source12.txt - key12.txt*.
2. All key files must have a comma as a separator.
3. One line in key files contains only one named entity with a tag. Tag must be in upper case: *Джеймс Мэй,PER*.
4. Only PER, ORG, LOC and MISC are supported.
5. If you are going to use DeepPavlov split the source files so that one line contains only one sentence.
6. Do not add spaces before of after comma.

You can find examples of corpus files in the demo_corpus directory.

## Scripts description

The script directory layout is crucial for correct script execution.

### Script `run_scripts.py`

This script was created for running all sets of scripts in the correct order.

Arguments of this script:

1. Path to directory that contains source files.
2. Path to directory that ready to accept results of work by neural network.
3. Path to one of three scripts that works with neural network (`pavlov_ru_executant.py`, `stanza_ru_executant.py` or `spacy_ru_executant.py`).
4. Path to directory that ready to accept technical files and corpus final report.
5. Prefix for files with result of work by selected neural network.
6. Path to directory that contains key files.
7. Path to directory that ready to accept results of auto testing.
8. Name of selected library (spaCy, Stanza or DeepPavlov).
9. Permission to handle misc tag (misc - permission, something else - denial).
10. Optional tag: mode for auto testing script. If typed 'experimental' right selected entities with wrong tag will get mark CF instead of FN (FN by default).

Results of execution:

Chain of scripts has been executed, final report for the corpus has been created.

### Script `scripts/stanza_ru_executant.py`

This script was created for processing source files using Stanza library.

Arguments of this script:

1. Source file for processing.
2. Path to file that will be created by script. Will contain a list of named entities founded by a neural network.
3. Path to directory that ready to accept technical files.

Results of execution:

1. File with founded named entities by network.
2. File with number of tokens with O tag in text.

### Script `scripts/spacy_ru_executant.py`

This script was created for processing source files using the SpaCy library.

Arguments of this script:

1. Source file for processing.
2. Path to file that will be created by script. Will contain a list of named entities founded by a neural network.
3. Path to directory that ready to accept technical files (information about tokens with O tag).

Results of execution:

1. File with founded named entities by network.
2. File with number of tokens with O tag in text.

### Script `scripts/pavlov_ru_executant.py`

This script was created for processing source files using the DeepPavlov framework.

Arguments of this script:

1. Source file for processing.
2. Path to file that will be created by script. Will contain a list of named entities founded by a neural network.
3. Path to directory that ready to accept technical files (information about tokens with O tag).

Results of execution:

1. File with founded named entities by network.
2. File with number of tokens with O tag in text.

### Script `scripts/neuro_operator.py`

This script was created for operating multiple launches of `stanza_ru_executant.py`, `pavlov_ru_executant.py` or `spacy_ru_executant.py`.

Arguments of this script:

1. Path to directory with source files.
2. Path to directory that ready to accept results of selected script work.
3. Path to `stanza_ru_executant.py`, `pavlov_ru_executant.py` or `spacy_ru_executant.py`.
4. Path to directory that ready to accept technical files (information about tokens with O tag).
5. Prefix for files that contains result of work by neural network.

Result of execution:

Selected script processing all txt files in selected directory.

### Script `scripts/test_operator.py`

This script was created for the operation of multiple auto test script launches.

Arguments of this script:

1. Path to directory with key files.
2. Path to directory with list of entities founded by neural network.
3. Path to directory that is ready for accept results of auto testing.
4. Path to directory thet ready to accept technical files (information about O tag tokens with FN mark).
5. Path to auto_test.py.
6. Permission to handle misc tag (misc - permission, something else - denial).
7. Optional: mode of work. If write 'experimental' named entities highlighted correctly but having the wrong tag get CF mark instead of FN mark (FN by default).

Result of execution:

All files at argv[2] path will be checked by auto test script.

### Script `scripts/auto_test.py`

This script was created for automatic testing of results created by a neural network.

Arguments of this script:

1. Path to key file.
2. Path to file with neural network answer.
3. Path to directory that ready to accept file with results of testing.
4. Path to directory that contains information about O tags (information about FN O tokens number).
5. Permission to handle misc tag (misc - permission, something else - denial).
6. Optional: mode of work. If write 'experimental' named entities highlighted correctly but having the wrong tag get CF mark instead of FN mark (FN by default).

Result of execution:

File that contains result of automatic testing

### Script `scripts/analytic.py`

This script was created for generating the final report. Uses data created by: `auto_test.py` and `pavlov_ru_executant.py` or `stanza_ru_executant.py` or `spacy_ru_executant.py`.

Arguments of this script:

1. Path to directory that contains technical files (information about FN O tokens number and total number of O tag tokens).
2. Name of selected library (Stanza, Spacy, DeepPavlov).
3. Path to directory that contains results of automatic testing script.

Result of execution:

Script creates final report in directory with technical files.

## Libraries installation

### SpaCy

```
pip install -U pip setuptools wheel
pip install -U spacy
python -m spacy download ru_core_news_lg
```

More information you can find [here](https://spacy.io/usage#installation).

### Stanza

Requires python 3.6|3.7|3.8

```
pip install stanza
```

And download model in Python interactive interpreter:

```python
import stanza
stanza.download('ru')
```

More information you can find [here](https://stanfordnlp.github.io/stanza/).

### DeepPavlov

Requires python 3.6|3.7

Does not support windows at 07.03.22

Create a virtual environment:

```
python -m venv env
```

Activate the environment:

```
source ./env/bin/activate
```

Install the package inside this virtual environment:

```
pip install deeppavlov
```

Model download example:

```
python -m deeppavlov install ner_ontonotes_bert_torch
```

More information you can find [here](http://docs.deeppavlov.ai/en/master/intro/installation.html) or [here](https://habr.com/ru/company/mipt/blog/472890/).
