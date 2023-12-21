# What is this?

This project is the artefact for my 3rd Year Computer Science Dissertation at Falmouth University. The repo contains all code files, data collection and analysis.

**Research Question:** Can large language models generate code for small-scale problems that compete with model, human-written answers.

**Hypothesis H1:** Large language models can generate
code for small-scale coding problems that produce higher scoring in
a range of given metrics when compared to model, human answers.


# Navigation 

**main.py** Main file to run 

**/Code** The majority of the code base
- _Data.py_ - Where the raw .csv results are stored alongside all R code used in analysis
- _Analyzer.py_ - Contains all methods to calculate code metrics
- _Lexer.py_ - Contains methods to extract tokens counts for metric calculations
- _Generation.py_ - Contains methods to send and receive generations using OpenAI's API
- _Generated.py_ solutions used in testing
- _pilotProblems.json_ - Contains problem used in the pilot study, in human-readable text

**/Tests** Tests for the project and problem solutions
- _LexerTests.py_ - Tests the lexer meets its functional requirements 
- _ProblemTests.py_ - Tests that the human and generated solutions successfully pass the task
- _/LexerTestSamples_ - Python code samples used by LexerTests.py

**/Solution**  Folder where all human and generated solutions are stored

**/Paper** Contains documentation of research 
- Initial proposal PDF
- Overleaf main.tex and .bib