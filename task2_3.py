import nltk
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def process_skills(df):
    # Combine all job titles into a single string
    all_job_titles = ' '.join(df['job_title'].str.lower())

    # Split the string into words
    words = all_job_titles.split()

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_skills = [word for word in words if word not in stop_words]

    # Extract unique words as potential skills
    unique_skills = set(filtered_skills)

    # Convert the list of skills to a DataFrame
    skills_df = pd.DataFrame({'Big Data Skills': list(unique_skills)})

    # Use TF-IDF vectorization to convert skills into numerical features
    vectorizer = TfidfVectorizer()
    skills_tfidf = vectorizer.fit_transform(skills_df['Big Data Skills'])

    # Apply KMeans clustering
    num_clusters = 3  # You can adjust the number of clusters based on your preference
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    skills_df['Cluster'] = kmeans.fit_predict(skills_tfidf)

    # Return the processed skills DataFrame
    return skills_df

