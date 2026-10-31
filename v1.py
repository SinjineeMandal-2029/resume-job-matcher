import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    tokens = [t.strip(".") for t in text.split()]
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t and t not in stop_words]
    return " ".join(tokens)


def match_score(resume, job_description, ngram=(1, 2)):
    docs = [clean_text(resume), clean_text(job_description)]
    vectorizer = TfidfVectorizer(token_pattern=r"\S+", ngram_range=ngram)
    tfidf_matrix = vectorizer.fit_transform(docs)
    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return round(score * 100, 1)


resume = """
Third-year AI & ML student. Built machine learning models in Python using
Scikit-learn and Pandas. Trained Random Forest and Logistic Regression models,
did feature engineering and hyperparameter tuning. Built a Flask web app.
Skilled in SQL, C++ and data structures.
"""

job_description = """
We are looking for a Machine Learning Intern with experience in Python,
Scikit-learn, and TensorFlow. You will build and evaluate machine learning
models, work with large datasets, and deploy APIs using Flask or FastAPI.
Knowledge of SQL and deep learning is a plus.
"""

marketing_job = """
We need a Marketing Executive to manage social media campaigns, create
brand content, run Instagram ads, and work with the sales team to
increase customer engagement and brand awareness.
"""

print("Cleaned resume:", clean_text(resume))
print()

print("--- With word pairs (1, 2) ---")
print("ML job score:       ", match_score(resume, job_description, (1, 2)), "%")
print("Marketing job score:", match_score(resume, marketing_job, (1, 2)), "%")
print("Same text score:    ", match_score(resume, resume, (1, 2)), "%")
print()

print("--- Single words only (1, 1) ---")
print("ML job score:       ", match_score(resume, job_description, (1, 1)), "%")
print("Marketing job score:", match_score(resume, marketing_job, (1, 1)), "%")
print("Same text score:    ", match_score(resume, resume, (1, 1)), "%")