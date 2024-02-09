from flask import Flask, render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib

from Task_5 import analyze_and_visualize, analyze_skills

matplotlib.use('Agg')  # Use the 'Agg' backend (non-GUI)

from Task_4 import group_by_job_title
from task2_3 import process_skills

app = Flask(__name__)
np.random.seed(42)  # specific seed value

# Load the dataset
df = pd.read_csv('dataset/Data Science Jobs Salaries.csv')
raw_data_head = df.head().to_html()
missing_values = df.isnull().sum().to_frame().to_html()

# Your data preprocessing code
# Task 1: Convert 'work_year' to a consistent format
df['work_year'] = df['work_year'].str.replace('e', '', regex=False).astype(int)

# Task 2: Convert 'salary_currency' to uppercase for consistency
df['salary_currency'] = df['salary_currency'].str.upper()

# Task 3: Convert 'experience_level' to a categorical data type
df['experience_level'] = pd.Categorical(df['experience_level'], categories=['EN', 'MI', 'SE', 'EX'], ordered=True)

# Task 4: Convert 'remote_ratio' to a percentage
df['remote_ratio'] = df['remote_ratio'] / 100.0

# Task 5: Handle missing values (replace with mean or other strategies)
df['salary'].fillna(df['salary'].mean(), inplace=True)

# Task 6: Drop unnecessary columns
df.drop(['salary_in_usd'], axis=1, inplace=True)

# Display the preprocessed dataset
preprocessed_data_head = df.head().to_html()


# Define a route for the homepage
@app.route('/')
def home():
    # Render the homepage HTML template
    return render_template('homepage.html')


# Define a route for the home page
@app.route('/preprocess')
def preprocess():
    # Unique job titles
    unique_job_titles = df['job_title'].unique()

    # Task 1: Identify Big Data Job Families
    # Assume keywords related to Big Data job families (customize this based on your data)
    big_data_keywords = ['Data Scientist', 'Machine Learning', 'Data Analyst', 'Data Engineer', 'Data Science Engineer',
                         'Data Analytics', 'ML Engineer', 'AI Scientist', 'Big Data', 'Data Architect']

    # Create a new column 'job_family' and assign it based on the keywords
    def assign_job_family(title):
        for keyword in big_data_keywords:
            if keyword.lower() in title.lower():
                return keyword
        return 'Other'

    df['job_family'] = df['job_title'].apply(assign_job_family)

    # Updated dataset with job families
    updated_dataset = df[['job_title', 'job_family']].head()
    # Display the preprocessed dataset
    preprocessed_data_head = df.head().to_html()

    # Render the result in an HTML template
    return render_template('result.html', raw_data_head=raw_data_head, missing_values=missing_values,
                           unique_job_titles=unique_job_titles, updated_dataset=updated_dataset,
                           preprocessed_data_head=preprocessed_data_head)


# Define a route for the skills page
@app.route('/skills')
def skills():
    # Call the process_skills function
    skills_df = process_skills(df)

    # Render the result in an HTML template
    return render_template('skills.html', skills_data=skills_df.to_html())


# Define a route for the competence levels page
@app.route('/competence_levels')
def competence_levels():
    # Call the group_by_job_title function
    competence_levels_df = group_by_job_title(df)

    # Create a pie chart
    plt.figure(figsize=(8, 8))
    plt.pie([len(levels) for levels in competence_levels_df['Competence Levels']],
            labels=competence_levels_df['Job Title'], autopct='%1.1f%%', startangle=140)
    plt.title('Competence Levels Distribution')

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 for embedding in HTML
    chart_img = base64.b64encode(img.getvalue()).decode('utf-8')

    # Close the plot
    plt.close()

    # Render the result in an HTML template
    return render_template('competence_levels.html', competence_levels_data=competence_levels_df.to_html(index=False),
                           chart_img=chart_img)


#@@@@@@task 5
# Create the 'job_family' column
unique_job_titles = df['job_title'].unique()
print("Unique Job Titles:")
#print(unique_job_titles)

# Assume keywords related to Big Data job families (customize this based on your data)
big_data_keywords = ['Data Scientist', 'Machine Learning', 'Data Analyst', 'Data Engineer', 'Data Science Engineer', 'Data Analytics', 'ML Engineer', 'AI Scientist', 'Big Data', 'Data Architect']

# Create a new column 'job_family' and assign it based on the keywords
def assign_job_family(title):
    for keyword in big_data_keywords:
        if keyword.lower() in title.lower():
            return keyword
    return 'Other'

df['job_family'] = df['job_title'].apply(assign_job_family)


# Define a route for the data_analysis view
@app.route('/data_analysis')
def data_analysis():
    # Call the analyze_and_visualize function
    competence_plot_img, skills_plot_img, heatmap_plot_img, skills_table, job_families_table = analyze_and_visualize(df)

    # Render the result in an HTML template
    return render_template('data_analysis.html',
                           competence_plot_img=competence_plot_img,
                           skills_plot_img=skills_plot_img,
                           heatmap_plot_img=heatmap_plot_img,
                           skills_table=skills_table,
                           job_families_table=job_families_table)


# Define a route for the recommendations page
@app.route('/recommendations')
def recommendations():
    # Render the recommendations.html template
    return render_template('recommendation.html')


# Define a route for the skills analysis page
@app.route('/skills_analysis')
def skills_analysis():
    # Call the analyze_skills function
    job_families_overview_plot, skill_clusters_rankings_plot = analyze_skills(df)

    # Render the skills_analysis.html template
    return render_template('skills_analysis.html',
                           job_families_overview_plot=job_families_overview_plot,
                           skill_clusters_rankings_plot=skill_clusters_rankings_plot)





if __name__ == '__main__':
    app.run()
