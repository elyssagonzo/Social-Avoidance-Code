# Import libraries for survey data manipulation and statistical analysis.
import pandas as pd 
import scipy as sp
from statsmodels.stats.multitest import multipletests

# Load the survey responses for the social-avoidance analysis.
unfiltered_df = pd.read_csv("socialavoidancedata.csv")
if len(unfiltered_df.columns) != 22:
    raise ValueError(
        f"Expected 22 survey columns, found {len(unfiltered_df.columns)}."
    )

# Assign concise names to the survey columns for easier reference. 
unfiltered_df.columns = ['time', 'score', 'year', 'college', 'screentime', 'introvert/extrovert', 'social anxiety', 'convenience value', 'free time', 'buying clothes', 'eating', 'ordering food', 'attention check', 'talking', 'checkout', 'professor', 'tiredness', 'in line', 'avoid', 'explain avoid', 'seek', 'explain seek']

# Remove metadata, demographic fields outside the current analysis,
# and direct yes/no social-avoidance questions not included in the planned correlation tests. 
variable_df = unfiltered_df.drop(['time', 'score', 'year', 'college', 'avoid', 'explain avoid', 'seek', 'explain seek'], axis = 1)

# Exclude respondents who failed the attention check, then remove attention-check variable. 
clean_df = variable_df[variable_df['attention check'] == 5]
clean_df = clean_df.drop(['attention check'], axis = 1)

# Map ordered categorical responses to numeric scores so they can be included 
# in rank-based correlation analysis. 
# note: these values represent researcher-assigned scores or approximate hours
screentime_dict = {'Less than 1 Hour': 0.5, '1-2 Hours': 1.5, '3-5 Hours': 4, '5-7 Hours': 6, '7-9 Hours': 8, 'More than 9 Hours': 10}
intro_extro_dict = {'Introvert': 1, 'Ambivert (mix of both)': 5, 'Extrovert': 10}
free_time_dict = {'Less than half an hour': 0, '1 hour': 1, '2 hours': 2, '3 hours': 3, '4 hours': 4, '5 hours': 5, '6+ hours': 6}

# Apply the mappings to convert screentime, personality, and free-time responses into numeric values.
def convert_screentime(screentime):
    return screentime_dict[screentime]

def convert_in_ex(vert):
    return intro_extro_dict[vert]

def convert_freetime(time):
    return free_time_dict[time]
 
clean_df['screentime'] = clean_df['screentime'].apply(convert_screentime)
clean_df['introvert/extrovert'] = clean_df['introvert/extrovert'].apply(convert_in_ex)
clean_df['free time'] = clean_df['free time'].apply(convert_freetime)

# Specify the explanatory variables and behavioral outcomes.
indep_vars = ['screentime', 'introvert/extrovert', 'social anxiety', 'free time', 'convenience value']
dep_vars = ['buying clothes', 'eating', 'ordering food', 'talking', 'checkout', 'professor', 'tiredness', 'in line']

# Calculate Spearman rank correlations for every explanatory-outcome variable pair. 
values_dict = {
    'variables': [], 
    'n': [],
    'statistic (+/-)': [], 
    'p-value (0.05)': []
}

for invar in indep_vars:
    for devar in dep_vars:
        paired_data = clean_df[[invar,devar]].dropna()

        statistic = sp.stats.spearmanr(
            a=paired_data[invar],
            b=paired_data[devar]
        )

        values_dict['variables'].append(f'{invar} x {devar}')
        values_dict['n'].append(len(paired_data))
        values_dict['statistic (+/-)'].append(statistic.statistic)
        values_dict['p-value (0.05)'].append(statistic.pvalue)

# Organize the correlation results into a dataframe for review, comparison, and export.
significance_correlations = pd.DataFrame(values_dict)

# Identify results with unadjusted p-values below 0.05.
# These are nominally significant and have not been corrected for multiple comparisons.
significant_correlations = significance_correlations[significance_correlations['p-value (0.05)'] < 0.05] 

# Apply the Benjamini-Hochberg correction to all correlation tests
# to control the false discovery rate at 0.05.
valid_p = significance_correlations['p-value (0.05)'].notna()

# Calculate adjusted p-values and identify significant results.
reject, p_adjusted, _, _ = multipletests(
    significance_correlations.loc[valid_p, 'p-value (0.05)'],
    alpha=0.05,
    method='fdr_bh'
)

# Store adjusted p-values and significance decisions.
significance_correlations['p_adjusted'] = float('nan')
significance_correlations['significant_after_BH'] = False

significance_correlations.loc[valid_p, 'p_adjusted'] = p_adjusted
significance_correlations.loc[valid_p, 'significant_after_BH'] = reject

# Display results that remain significant after correction. 
adjusted_sig_correlations = significance_correlations[
    significance_correlations['significant_after_BH']
]

# Summarize the correlation analysis results.
print(f"Respondents retained after attention check: {len(clean_df)}")
print(f"Total correlation tests: {len(significance_correlations)}")
print(f"Unadjusted p-values below 0.05: {len(significant_correlations)}")
print(f"Significant after BH correction: {len(adjusted_sig_correlations)}")

# Display results that remain significant after correction.
print("\nCorrelations significant after BH correction:")
print(adjusted_sig_correlations.to_string(index=False))