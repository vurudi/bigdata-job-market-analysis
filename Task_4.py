import pandas as pd

def group_by_job_title(df):
    # Group by job title and collect unique competence levels
    competence_levels = df.groupby('job_title')['experience_level'].unique()

    # Create a DataFrame to store the results
    result_df = pd.DataFrame({'Job Title': competence_levels.index, 'Competence Levels': competence_levels.values})

    return result_df
