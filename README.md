- **Project overview**: This project explores the relationship between individual characteristics, such as introversion/extroversion and social anxiety, and preferences for avoiding or engaging in everyday social situations among college students. Participant-level survey data are not included in this repository to protect respondent privacy. 
- **Files**: 
    - spearmans_analysis.py: Cleans survey data, calculates Spearman rank correlations, and adjusts p-values for multiple comparisons using the Benjamini-Hochberg procedure. 
    - data_visualization.py: Generates bar charts showing mean responses across categories of selected independent variables.
    - requirements.txt: Lists the Python libraries required to run the scripts. 
    - figures/: Contains generated visualizations.
- **How to run**: Python 3 and the libraries listed in requirements.txt.
    1. Clone or download this repository.
    2. Install the required libraries:
        ```bash pip install -r requirements.txt ```
    3. Place the survey CSV file, socialavoidance.csv, in the project directory. The dataset is not included in this repository. 
    4. Run either script from the project directory: 
        ```bash python spearmans_analysis.py ```
        ```bash python data_visualization.py ```
- **Methods and Limitations**: This project uses self-reported survey responses and Spearman rank correlations to examine associations between variables. The results are exploratory and do not establish causation. Multiple-comparison correction is used to account for testing numerous correlations.  