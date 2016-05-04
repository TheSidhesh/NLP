       	   BLEU Score Evaluator
	-------------------------------------

What is it ?
------------

These is a program that evaluates the [BLEU](https://en.wikipedia.org/wiki/BLEU) Score for a candidate file given a(set of) reference file(s).

Input -
-------

Input to the program:
	1) A candidate file for which the score is to be evaluated
	2) Single or multiple reference files. Multiple reference files must be stored in a folder separately.


Output - 
---------

calculatebleu.py will create bleu_output.txt which contains the evaluated BLEU score for the candidate file.


Usage
----------------

Invoke calculatebleu.py

-->python calculatebleu.py /path/to/candidate /path/to/reference


----------------

Language Used - Python

	
