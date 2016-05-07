# masterthesis
Scripts I used for my master's thesis in computer linguistics.

----

This repository includes two files:

- A simple chunker I wrote because there was not one for Russian
- A script to add features I used for training a coreference classifier.

chunker.py
-----------

The purpose of this script is to extract noun phrases and anaphoric pronouns from preprocessed Russian texts. 

**Input**: The script takes a TreeTagger-processed text on input, which means it must be a .txt file, consisting of tab-separated lines of "word  tags  lemma" format.

**Dependencies**: No external dependencies are required.

**Options**: You can pass a `--launch %foldername%` flag to the script to direct it to a folder where the files to analyze are kept. Otherwise it willsearch for *.txt files in the folder where it is located.

**Output**: The script produces a .txt file that contains a list of tab-separated lines with one extracted noun phrase per line. At the beginning of the line its ordinal number is appended, and the head of the phrase is marked as such. Anaphoric pronouns are extracted as separate noun phrases.

featurer.py
-----------

The purpose of this script is to make a corpus of noun phrase pairs from the provided list of files, and mark it up, according to the list of features. A more detailed description is provided in my master's thesis.

**Input**: The script takes a list of noun phrases, created by chunker.py on input.

**Dependencies**: No external dependencies are required.

**Options**: You can pass a `--launch %foldername%` flag to the script to direct it to a folder where the files to analyze are kept. Otherwise it willsearch for *.txt files in the folder where it is located.

**Output**: The script produces a .csv file that contains a comma-separated list of pairs of noun phrases and feature values for each of the pairs.

