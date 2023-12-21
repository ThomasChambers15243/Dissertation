# What is this?

This project is the artefact for my 3rd Year Computer Science Dissertation at Falmouth University. The repo contains all code files, data collection and analysis.

**Research Question:** Can large language models generate code for small-scale problems that compete with model, human-written answers.

**Hypothesis H1:** Large language models can generate
code for small-scale coding problems that produce higher scoring in
a range of given metrics when compared to model, human answers.


# Navigation 

**/Paper** Contains documentation of research 
- Initial proposal PDF
- Overleaf main.tex and .bib

**/Code** The majority of the code base
- Data - Where the raw .csv results are stored alongside all R code used in analysis
- Analyzer - Contains all methods to calculate code metrics
- Lexer - Contains methods to extract tokens counts for metric calculations
- Generation - Contains methods to send and receive generations using OpenAI's API
- Generated solutions used in testing

**/Solution**  Folder where all human and generated solutions are stored