import io
from flask import Flask, request, jsonify
from flask_cors import CORS
from matcher import read_pdf, analyze

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload limit
CORS(app)


@app.route("/")
def home():
    return jsonify({"status": "Resume matcher API is running"})


@app.route("/analyze", methods=["POST"])
def analyze_route():
    file = request.files.get("resume")
    job_description = request.form.get("job_description", "").strip()

    if file is None or file.filename == "":
        return jsonify({"error": "Please upload your resume as a PDF."}), 400
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported."}), 400
    if len(job_description) < 30:
        return jsonify({"error": "Please paste a longer job description."}), 400

    try:
        resume_text = read_pdf(io.BytesIO(file.read()))
    except Exception:
        return jsonify({"error": "Could not read this PDF. Try another file."}), 400

    if len(resume_text.strip()) < 50:
        return jsonify({"error": "No text found. Scanned PDFs are not supported yet."}), 400

    return jsonify(analyze(resume_text, job_description))


@app.errorhandler(413)
def too_large(e):
    return jsonify({"error": "File too large (max 5 MB)."}), 413


if __name__ == "__main__":
    app.run(debug=True)