# -*- coding: utf-8 -*-
"""IMDb-Movie-Review-Sentiment-Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EzN0XLqFBumNSO4RHFnTBVDlUIQE8LXv
"""

# Import Required Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Set style for plots
sns.set_style('whitegrid')
plt.style.use('fivethirtyeight')

"""# **Load and Explore the Dataset**"""

# Load the dataset
df = pd.read_csv('Imdb - data_imdb.csv')

# Check the first few rows
print(df.head())

# Check dataset info
print(df.info())

# Check class distribution
print(df['sentiment'].value_counts())

# Visualize class distribution
plt.figure(figsize=(8, 6))
sns.countplot(x='sentiment', data=df)
plt.title('Distribution of Positive and Negative Reviews')
plt.show()

"""# **Text Preprocessing**"""

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)

    # Tokenize text
    tokens = word_tokenize(text)

    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    # Join tokens back into string
    clean_text = ' '.join(tokens)

    return clean_text

nltk.download('punkt_tab')

# Apply cleaning to reviews
df['cleaned_review'] = df['review'].apply(clean_text)

# Add some text statistics
df['word_count'] = df['cleaned_review'].apply(lambda x: len(x.split()))
df['char_count'] = df['cleaned_review'].apply(len)
df['avg_word_length'] = df['cleaned_review'].apply(lambda x: np.mean([len(word) for word in x.split()]))

# Show cleaned data
print(df[['review', 'cleaned_review', 'word_count', 'char_count', 'avg_word_length']].head())

"""# **Exploratory Data Analysis**"""

# Plot distribution of word counts
plt.figure(figsize=(12, 6))
sns.histplot(data=df, x='word_count', hue='sentiment', bins=50, kde=True)
plt.title('Distribution of Word Counts by Sentiment')
plt.xlabel('Word Count')
plt.ylabel('Frequency')
plt.show()

# Plot average word length
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='sentiment', y='avg_word_length')
plt.title('Average Word Length by Sentiment')
plt.show()

# Check most common words
from collections import Counter

def get_top_words(corpus, n=None):
    words = ' '.join(corpus).split()
    return Counter(words).most_common(n)

# Top words in positive reviews
pos_words = get_top_words(df[df['sentiment'] == 'positive']['cleaned_review'], 20)
print("Top words in positive reviews:", pos_words)

# Top words in negative reviews
neg_words = get_top_words(df[df['sentiment'] == 'negative']['cleaned_review'], 20)
print("Top words in negative reviews:", neg_words)

# Plot top words
def plot_top_words(word_list, title):
    words, counts = zip(*word_list)
    plt.figure(figsize=(12, 6))
    sns.barplot(x=list(counts), y=list(words))
    plt.title(title)
    plt.show()

plot_top_words(pos_words, 'Top 20 Words in Positive Reviews')
plot_top_words(neg_words, 'Top 20 Words in Negative Reviews')

# Convert sentiment to numerical values (1 for positive, 0 for negative)
df['sentiment_num'] = df['sentiment'].apply(lambda x: 1 if x == 'positive' else 0)

# Split data into train and test sets
X = df['cleaned_review']
y = df['sentiment_num']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize TF-IDF Vectorizer
tfidf = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))

# Fit and transform train data
X_train_tfidf = tfidf.fit_transform(X_train)

# Transform test data
X_test_tfidf = tfidf.transform(X_test)

print(f"TF-IDF shape for training data: {X_train_tfidf.shape}")
print(f"TF-IDF shape for test data: {X_test_tfidf.shape}")

"""# **Model Building and Evaluation**"""

# Dictionary to store model performance
model_results = {}

def train_and_evaluate(model, model_name):
    # Train the model
    model.fit(X_train_tfidf, y_train)

    # Predict on test data
    y_pred = model.predict(X_test_tfidf)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['negative', 'positive'])
    cm = confusion_matrix(y_test, y_pred)

    # Store results
    model_results[model_name] = {
        'accuracy': accuracy,
        'report': report,
        'confusion_matrix': cm
    }

    # Print results
    print(f"\n{model_name} Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(report)

    # Plot confusion matrix
    plt.figure(figsize=(6, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['negative', 'positive'],
                yticklabels=['negative', 'positive'])
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()

# Initialize models
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Naive Bayes': MultinomialNB(),
    'Support Vector Machine': SVC(kernel='linear', random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
}

# Train and evaluate each model
for name, model in models.items():
    train_and_evaluate(model, name)

"""# **Hyperparameter Tuning**"""

# Example for Logistic Regression
param_grid = {
    'C': [0.1, 1, 10],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear']
}

lr = LogisticRegression(max_iter=1000, random_state=42)
grid_search = GridSearchCV(lr, param_grid, cv=3, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train_tfidf, y_train)

print("Best parameters:", grid_search.best_params_)
print("Best accuracy:", grid_search.best_score_)

# Evaluate best model
best_lr = grid_search.best_estimator_
train_and_evaluate(best_lr, 'Tuned Logistic Regression')

"""# **Final Model Selection and Evaluation**"""

# Compare all models
results_df = pd.DataFrame.from_dict(model_results, orient='index')
results_df['accuracy'] = results_df['accuracy'].apply(lambda x: f"{x:.4f}")
print(results_df[['accuracy']])

# Select best model based on accuracy
best_model_name = max(model_results, key=lambda x: model_results[x]['accuracy'])
best_model = models[best_model_name]
print(f"\nBest Model: {best_model_name}")

# You can save the best model for future use
import joblib
joblib.dump(best_model, 'best_sentiment_model.pkl')
joblib.dump(tfidf, 'tfidf_vectorizer.pkl')

"""# **Create a Prediction Function**"""

def predict_sentiment(text):
    # Load the saved model and vectorizer
    model = joblib.load('best_sentiment_model.pkl')
    vectorizer = joblib.load('tfidf_vectorizer.pkl')

    # Clean the input text
    cleaned_text = clean_text(text)

    # Transform the text using the vectorizer
    text_tfidf = vectorizer.transform([cleaned_text])

    # Make prediction
    prediction = model.predict(text_tfidf)
    probability = model.predict_proba(text_tfidf)

    # Return result
    sentiment = 'positive' if prediction[0] == 1 else 'negative'
    confidence = probability[0][prediction[0]]

    return {
        'sentiment': sentiment,
        'confidence': float(confidence),
        'probability_positive': float(probability[0][1]),
        'probability_negative': float(probability[0][0])
    }

# Test the function
sample_review = "This movie was fantastic! The acting was superb and the plot was engaging."
print(predict_sentiment(sample_review))

sample_review2 = "I hated this movie. The acting was terrible and the story made no sense."
print(predict_sentiment(sample_review2))

"""# **Create a Summary Report**"""

# Generate a markdown report
report = f"""
# IMDb Movie Review Sentiment Analysis Report

## Dataset Overview
- Total reviews: {len(df)}
- Positive reviews: {len(df[df['sentiment'] == 'positive'])}
- Negative reviews: {len(df[df['sentiment'] == 'negative'])}

## Preprocessing Steps
1. Text cleaning (lowercase, remove special characters)
2. Tokenization
3. Stopword removal
4. Lemmatization
5. Added text statistics (word count, character count, average word length)

## Feature Extraction
- Used TF-IDF vectorization with max_features=10000 and ngram_range=(1, 2)

## Model Performance Comparison
{results_df[['accuracy']].to_markdown()}

## Best Model
- Model: {best_model_name}
- Accuracy: {model_results[best_model_name]['accuracy']:.4f}

## Key Findings
- The dataset was balanced between positive and negative reviews
- Reviews typically contained between 50-150 words
- The {best_model_name} performed best among the tested models
- Common positive words included 'film', 'movie', 'great', 'good'
- Common negative words included 'movie', 'film', 'bad', 'worst'
"""

print(report)

# Save report to file
with open('sentiment_analysis_report.md', 'w') as f:
    f.write(report)