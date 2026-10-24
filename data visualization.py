# Import libraries for survey data manipulation, visualization, text formatting,
# and filename handling. 
import pandas as pd
import matplotlib.pyplot as plt    
import textwrap as tw
import re
from pathlib import Path

# Define a class to load, clean, and summarize the survey data.
class COGS164_Data: 
    def __init__(self, csvfile): 
        # Load in the raw survey responses and standardize column names.
        unfiltered_df=pd.read_csv(csvfile) 
        
        for column in unfiltered_df.columns: # 
            unfiltered_df.rename(columns={column: column.strip()}, inplace=True)  

        # Retain only respondents who passed the attention check.
        self.COGS164_df = unfiltered_df[unfiltered_df['Select "5" if you are paying attention.']==5]

        # Define explanatory variables and behavioral outcome variables
        # for the descriptive comparison.
        self.indep_vars = [
                           'What year in college are you?', 
                           'On average, what is your daily reported phone screen time?', 
                           'Do you consider yourself an extrovert, introvert, or a mix of both?', 
                           'On a scale of 1-10 how socially anxious are you?', 
                           'On average, how many hours of free time/unstructured time do you have during the day?',
                           'On a scale of 1-10, how much value do you place on convenience/ease of access?'] 
        
        self.dep_vars = [   
                        'On a scale of 1-10, do you prefer to order clothes online or shop in person?', 
                        'On a scale of 1-10, do you prefer to eat alone or with friends?', 
                        'On a scale of 1-10, are you more likely to order food from an online delivery service, or dine out in person?', 
                        'On a scale of 1-10, would you prefer talking to a friend over text or call?',
                        'On a scale of 1-10 do you prefer to use self checkout or regular checkout?', 
                        'On a scale of 1-10, if a professor asks you to discuss a question with the person sitting next to you, how likely are you to talk to your peer?', 
                        'On a scale of 1-10,  how tired do you feel after a large social event? ( i.e. a gathering, kickback, party, etc.)', 
                        'On a scale of 1-10, how likely are you to talk with other people while waiting in a line.', 
                        'Do you prefer to avoid social situations?', 
                        'Do you actively seek social situations?'
                       ]  
    
    # Providing helper methods for inspecting column names and analysis variables
    # during development and debugging.
    def print_column_names(self): 
        print("\n".join(["'"+column+"'"for column in list(self.COGS164_df.columns)]))  

    def print_indep_vars(self):  
        print("\n".join(self.indep_vars))
    
    def print_dep_vars(self):
        print("\n".join(self.dep_vars))

    # Calculate response frequencies for each cateogry of a selected variable.        
    def get_frequencies(self,indep_var):  
        df=pd.DataFrame({'x':self.COGS164_df[indep_var]}) 
        df=df.groupby('x').value_counts().reset_index() 
        df.rename(columns={'count': 'y'}, inplace=True) 
        return df
    
    # Calculate the mean outcome score within each category of the
    # selected explanatory variable. 
    def get_mean(self,indep_var,dep_var):  
        df=pd.DataFrame({'x':self.COGS164_df[indep_var], 'y':self.COGS164_df[dep_var]}) 
        return df.groupby('x')['y'].mean().reset_index()
    
    # Replace invalid characters in filenames.
    def sanitize_filename(self, filename):
        return re.sub(r'[<>:"/\\|?*]', '_', filename)
    

theData=COGS164_Data('socialavoidancedata.csv')  
# Generate and save a bar chart for each explanatory-outcome variable pair.
# Exclude binary social avoidance questions from mean-based visualization.
figures_dir = Path('figures')
figures_dir.mkdir(exist_ok=True)
plot_count=0

for indep in theData.indep_vars: 
    for dep in theData.dep_vars: 
        if dep in (
            'Do you prefer to avoid social situations?',
            'Do you actively seek social situations?'
        ):
            continue
        
        # Calculate the mean outcome scores for each explanatory-outcome variable category.
        temp_df=theData.get_mean(indep,dep)

        # Create the figure and plot the group means. 
        plt.figure(figsize=(10, 7))
        plt.bar(temp_df['x'],temp_df['y'])

        # Format the chart title and axis labels for readability.
        title_font = {'family': 'verdana', 'color': 'black', 'weight': 'bold', 'size': 16}

        label_font = {'family': 'verdana', 'color': 'black', 'weight': 'normal', 'size': 12}

        # Add wrapped survey questions as the chart title and axis labels. 
        plt.xlabel(tw.fill(indep),fontdict=label_font)
        plt.ylabel(tw.fill(dep),fontdict=label_font)
        plt.title(tw.fill(indep+'\n'+' vs.'+'\n'+dep),fontdict=title_font)

        # Remove unnecessary plot borders. 
        plt.gca().spines['bottom'].set_visible(False) 
        plt.gca().spines['top'].set_visible(False)   
        plt.gca().spines['right'].set_visible(False)    
           
        # Label each bar with its mean value, rounded to two decimal places. 
        for x, y in zip(temp_df['x'], temp_df['y']): 
            plt.text(x, y, str(round(y,2)), ha='center', va='bottom', color='black')  
    
        # Save each chart and close the figure before generating the next one.
        filename = theData.sanitize_filename(f'{plot_count}_{indep}_vs_{dep}.png')  
        plt.savefig(figures_dir / filename, bbox_inches='tight')
        plot_count+=1
        plt.close()       