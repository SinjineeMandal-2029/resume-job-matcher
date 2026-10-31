import re
import pdfplumber
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# ---------- skills list: name -> ways it can be written ----------
SKILLS = {
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++"],
    "sql": ["sql"],
    "mysql": ["mysql"],
    "javascript": ["javascript"],
    "html": ["html"],
    "css": ["css"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning"],
    "nlp": ["nlp", "natural language processing"],
    "scikit-learn": ["scikit-learn", "sklearn", "scikit learn"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "matplotlib": ["matplotlib"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "streamlit": ["streamlit"],
    "api": ["api", "apis"],
    "git": ["git"],
    "github": ["github"],
    "docker": ["docker"],
    "aws": ["aws"],
    "data structures": ["data structures", "dsa"],
    "feature engineering": ["feature engineering"],
    "random forest": ["random forest"],
    "logistic regression": ["logistic regression"],
}


def read_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += (page.extract_text(x_tolerance=1.5) or "") + "\n"
    return text


def extract_skills(text):
    text = text.lower()
    found = set()
    for skill, aliases in SKILLS.items():
        for alias in aliases:
            pattern = r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])"
            if re.search(pattern, text):
                found.add(skill)
                break
    return found


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    tokens = [t.strip(".") for t in text.split()]
    tokens = [lemmatizer.lemmatize(t) for t in tokens if t and t not in stop_words]
    return " ".join(tokens)


def tfidf_score(resume, job_description):
    docs = [clean_text(resume), clean_text(job_description)]
    vectorizer = TfidfVectorizer(token_pattern=r"\S+")
    matrix = vectorizer.fit_transform(docs)
    return round(cosine_similarity(matrix[0], matrix[1])[0][0] * 100, 1)


job_description = """
We are looking for a Machine Learning Intern with experience in Python,
Scikit-learn, and TensorFlow. You will build and evaluate machine learning
models, work with large datasets, and deploy APIs using Flask or FastAPI.
Knowledge of SQL and deep learning is a plus.
"""

resume_text = read_pdf("Sinjinee_3rd_Year_Resume (1).pdf")

resume_skills = extract_skills(resume_text)
jd_skills = extract_skills(job_description)

matched = sorted(resume_skills & jd_skills)
missing = sorted(jd_skills - resume_skills)
coverage = round(len(matched) / len(jd_skills) * 100, 1) if jd_skills else 0

print("Resume skills found :", sorted(resume_skills))
print("Job skills required :", sorted(jd_skills))
print("Matched skills      :", matched)
print("Missing skills      :", missing)
print("Skill coverage      :", coverage, "%")
print("TF-IDF text score   :", tfidf_score(resume_text, job_description), "%")