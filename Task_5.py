import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from io import BytesIO
import base64
from wordcloud import WordCloud
from nltk.corpus import stopwords
from tabulate import tabulate
import pandas as pd


# Function for Data Analysis and Visualization
def analyze_and_visualize(df):
    # Distribution of Competence Levels
    competence_plot = plt.figure(figsize=(10, 6))
    sns.countplot(x='experience_level', data=df, order=df['experience_level'].value_counts().index)
    plt.title('Distribution of Competence Levels')
    plt.xlabel('Experience Level')
    plt.ylabel('Count')

    # Most Valued Skills Word Cloud
    all_job_titles = ' '.join(df['job_title'].str.lower())
    words = all_job_titles.split()
    filtered_skills = [word for word in words if word not in stopwords.words('english')]
    unique_skills = set(filtered_skills)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(unique_skills))
    skills_plot = plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud for Most Valued Skills')

    # Competence Levels by Job Family Heatmap
    heatmap_data = df.groupby(['job_family', 'experience_level']).size().unstack(fill_value=0)
    heatmap_plot = plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt='d')
    plt.title('Competence Levels by Job Family')
    plt.xlabel('Experience Level')
    plt.ylabel('Job Family')

    # Save plots to BytesIO objects
    competence_plot_img = save_plot_to_bytes(competence_plot)
    skills_plot_img = save_plot_to_bytes(skills_plot)
    heatmap_plot_img = save_plot_to_bytes(heatmap_plot)

    # Close plots
    plt.close(competence_plot)
    plt.close(skills_plot)
    plt.close(heatmap_plot)

    # Calculate skill frequencies
    all_job_titles = ' '.join(df['job_title'].str.lower())
    words = all_job_titles.split()
    filtered_skills = [word for word in words if word not in stopwords.words('english')]
    unique_skills = set(filtered_skills)
    skill_frequencies = {skill: filtered_skills.count(skill) for skill in unique_skills}

    # Rank the skills based on frequency
    ranked_skills = sorted(skill_frequencies, key=skill_frequencies.get, reverse=True)
    numbered_skills = [{'Skill': skill, 'Rank': i + 1} for i, skill in enumerate(ranked_skills)]

    # Display the list of skills with ranks in a table
    skills_table = tabulate(numbered_skills, headers="keys", tablefmt="html")

    # Calculate job family frequencies
    job_families = df['job_title'].str.lower()
    job_family_frequencies = job_families.value_counts().to_dict()

    # Rank the job families based on frequency
    ranked_job_families = sorted(job_family_frequencies, key=job_family_frequencies.get, reverse=True)
    numbered_job_families = [{'Job Family': job_family, 'Rank': i + 1} for i, job_family in enumerate(ranked_job_families)]

    # Display the list of job families with ranks in a table
    job_families_table = tabulate(numbered_job_families, headers="keys", tablefmt="html")

    return competence_plot_img, skills_plot_img, heatmap_plot_img, skills_table, job_families_table





def save_plot_to_bytes(plot):
    img = BytesIO()
    plot.savefig(img, format='png')
    img.seek(0)
    encoded_img = base64.b64encode(img.getvalue()).decode('utf-8')
    return encoded_img

# Function for Skills Analysis
def analyze_skills(df):
    # Job Families Overview Plot
    job_families_overview_plot = px.pie(df, names='job_title', title='Job Families Overview', width=800, height=500)

    # Assuming you have extracted skills and stored them in the 'extracted_skills' column
    df['extracted_skills'] = df['job_title'].str.lower().str.split()

    # Flatten the list of lists into a single list of skills
    all_skills = [skill for skills_list in df['extracted_skills'] for skill in skills_list]

    # Create a DataFrame with skills and their frequencies
    skill_frequencies_df = pd.DataFrame(all_skills, columns=['skill']).value_counts().reset_index(name='frequency')

    # Skill Clusters and Rankings Plot
    skill_clusters_rankings_plot = px.bar(skill_frequencies_df, x='skill', y='frequency', title='Skill Clusters and Rankings', width=800, height=500)

    # Convert Plotly figures to HTML
    job_families_overview_plot_html = job_families_overview_plot.to_html(full_html=False)
    skill_clusters_rankings_plot_html = skill_clusters_rankings_plot.to_html(full_html=False)

    return job_families_overview_plot_html, skill_clusters_rankings_plot_html
