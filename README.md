# IMDb Movie Review Sentiment Analysis 

## 1. Introduction
### 1.1 Project Overview
Sentiment analysis is a natural language processing task that classifies text as expressing positive or negative sentiment. This project analyzes IMDb movie reviews to predict sentiment, which can help filmmakers, critics, and platforms understand audience opinions.

### 1.2 Problem Statement
Build a machine learning model to classify IMDb movie reviews as positive or negative using text preprocessing, feature extraction, and classification algorithms.

## 2. Dataset Description
- **Source**: IMDb dataset (50,000 reviews)
- **Features**:
  - Review text (free-text)
  - Sentiment label (positive/negative)
- **Class Distribution**: Balanced (25,000 positive, 25,000 negative)

## 3. Methodology
### 3.1 Data Preprocessing
- Text cleaning (lowercase, special character removal)
- Tokenization
- Stopword removal
- Lemmatization
- Added features: word count, character count, average word length

### 3.2 Feature Extraction
- TF-IDF Vectorization (10,000 features, unigrams and bigrams)

### 3.3 Models Implemented
1. Logistic Regression
2. Naive Bayes
3. Support Vector Machine
4. Random Forest

### 3.4 Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrices

## 4. Results
### 4.1 Model Performance Comparison
| Model                | Accuracy |
|----------------------|----------|
| Logistic Regression  | 0.8921   |
| Naive Bayes          | 0.8634   |
| SVM                  | 0.8876   |
| Random Forest        | 0.8452   |

### 4.2 Key Findings
- Logistic Regression performed best (89.21% accuracy)
- Most common positive words: "film", "movie", "great", "good"
- Most common negative words: "movie", "film", "bad", "worst"
- Review length didn't strongly correlate with sentiment

## 5. Conclusion
- Demonstrated effective sentiment classification of movie reviews
- Logistic Regression with TF-IDF features worked best
- Potential applications: automated review analysis, content recommendation

## 6. Future Work
- Experiment with deep learning models (LSTM, BERT)
- Incorporate additional features (sentiment lexicons)
- Deploy as a web application

## Appendix
- Complete code implementation
- Sample predictions
- Confusion matrices
