import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
from flask_cors import CORS 
import json
import anthropic
import re

app = Flask(__name__)
CORS(app)



client = anthropic.Anthropic()

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_pdf_text(file_path)
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    else:
        raise ValueError('Unsupported file format')

def analyze_keywords_with_claude(resume_text, job_category):
    prompt = f"""As an HR specialist, analyze this resume for a {job_category} position.
    1. Identify the top 10 most relevant keywords or phrases for this job category.
    2. Based on these keywords and the resume content, generate 5 impactful, ready-to-use bullet points 
    that the candidate could directly add to their resume. These points should integrate the keywords 
    and be tailored to the {job_category} position.

    Resume text:
    {resume_text}

    Provide the output in this JSON format:
    {{
      "keywords": ["keyword1", "keyword2", ...],
      "bullet_points": ["Ready-to-use point 1", "Ready-to-use point 2", ...]
    }}
    """

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1000,
        temperature=0.3,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract the JSON part from the response
    response_content = response.content[0].text
    json_start = response_content.find('{')
    json_end = response_content.rfind('}') + 1
    json_str = response_content[json_start:json_end]

    return json_str

@app.route('/analyze_resume_structure', methods=['POST'])
def analyze_resume_structure():
    if 'resume' not in request.files:
        return jsonify({'error': 'Resume file is required.'}), 400

    file = request.files['resume']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file. Only PDF and DOCX are allowed.'}), 400

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    resume_text = extract_text(file_path)

    prompt = f"""As an expert resume analyst and career advisor, analyze the following resume. Your task is to provide a structured response in JSON format. Ensure that the JSON is perfectly formatted, with all keys and string values enclosed in double quotes, and no extraneous text outside the JSON structure. The JSON should include the following sections:

    1. "Inferred Industry": A string indicating the industry or job category this resume is targeting.

    2. "Metrics": An object containing:
       - "Total Word Count": An integer.
       - "Number of Bullet Points": An integer.
       - "Percentage of Empty Lines": A string formatted as a percentage (e.g., "10.5%").
       - "Number of Action Verbs Used": An integer.
       - "Number of Quantifiable Achievements": An integer.

    3. "Structure": An object containing:
       - "Presence and Order of Standard Sections": An array of strings.
       - "Overall Layout Effectiveness": An integer (scale of 1-10).

    4. "Content": An object containing:
       - "Balance Between Technical Skills and Soft Skills": A string formatted as a percentage (e.g., "70% technical, 30% soft").
       - "Top 5 Relevant Keywords": An array of strings.

    5. "Strengths": An array of strings listing key strengths of the resume.

    6. "Areas for Improvement": An array of strings listing specific suggestions for enhancement.

    7. "Overall Assessment": A string providing a brief evaluation summary (2-3 sentences).

    8. "Industry Comparison": An object containing:
       - "Typical Word Count Range": A string.
       - "Typical Number of Bullet Points Range": A string.
       - "Typical Percentage of Empty Lines Range": A string formatted as a percentage range (e.g., "5-15%").
       - "Typical Number of Action Verbs Used Range": A string.
       - "Typical Number of Quantifiable Achievements Range": A string.

    9. "Recommendations": An array of strings listing actionable recommendations to improve the resume's appeal.

    Resume Text:
    {resume_text}

    Ensure the JSON is valid and can be parsed without errors. Do not include any text outside of the JSON structure.
    """

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract the content from the response
        response_content = response.content[0].text

        # Log the response content for debugging
        print("Response Content:", response_content)

        # Attempt to parse the JSON directly
        try:
            analysis = json.loads(response_content)
            return jsonify(analysis), 200
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return the raw content for debugging
            return jsonify({
                'error': f'Failed to parse JSON: {str(e)}',
                'raw_content': response_content
            }), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_keywords', methods=['POST'])
def analyze_keywords():
    if 'resume' not in request.files or 'job_category' not in request.form:
        return jsonify({'error': 'Resume file and job category are required.'}), 400

    file = request.files['resume']
    job_category = request.form['job_category']

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file. Only PDF and DOCX are allowed.'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    resume_text = extract_text(file_path)

    try:
        analysis_json = analyze_keywords_with_claude(resume_text, job_category)
        analysis = json.loads(analysis_json)  # Parse the JSON string here
        return jsonify({
            'job_category': job_category,
            'analysis': analysis
        }), 200

    except json.JSONDecodeError as e:
        return jsonify({'error': f'Failed to parse JSON: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_resume_length', methods=['POST'])
def analyze_resume_length():
    if 'resume' not in request.files:
        return jsonify({'error': 'Resume file is required.'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from resume
        resume_text = extract_text(file_path)
        word_count = len(resume_text.split())

        # Define ideal word count ranges based on industry standards
        # This can be more dynamic based on job category if needed
        ideal_min = 500
        ideal_max = 1000

        difference = word_count - ideal_max if word_count > ideal_max else ideal_min - word_count

        # Crafting the prompt
        prompt = (
            f"You are an experienced career advisor. Analyze the following resume text and determine if the length "
            f"is optimal for making a strong impression for a professional job application. "
            f"Provide the word count and advise whether it is too short, too long, or just right. If adjustments are needed, "
            f"suggest how to improve it.\n\n{resume_text}"
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an experienced career advisor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.3
            )

            analysis_text = response.choices[0].message.content.strip()

            return jsonify({
                'word_count': word_count,
                'analysis': analysis_text
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'Invalid file type. Only PDF and DOCX are allowed.'}), 400

@app.route('/suggest_keywords', methods=['POST'])
def suggest_keywords():
    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({'error': 'Resume file and job description are required.'}), 400

    file = request.files['resume']
    job_description = request.form['job_description']

    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from resume
        resume_text = extract_text(file_path)

        # Crafting a detailed prompt
        prompt = f"""You are a career counselor assisting with optimizing resumes. Given the following resume text and job description, 
        suggest 5 keywords that would enhance the resume's relevance and effectiveness for the job role. 
        For each keyword:
        1. Provide a brief explanation of why it's important (1-2 sentences)
        2. Suggest a bullet point or sentence incorporating the keyword that the user could add to their resume.

        Resume Text:
        {resume_text}

        Job Description:
        {job_description}

        Format your response as a JSON object with the following structure:
        {{
          "keywords": [
            {{
              "keyword": "Example Keyword",
              "explanation": "Brief explanation of importance",
              "suggestion": "Example bullet point or sentence"
            }},
            ...
          ]
        }}
        """

        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0.3,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the JSON part from the response
            response_content = response.content[0].text
            json_start = response_content.find('{')
            json_end = response_content.rfind('}') + 1
            suggestions = json.loads(response_content[json_start:json_end])

            return jsonify({
                'job_description': job_description,
                'keyword_suggestions': suggestions['keywords']
            }), 200

        except json.JSONDecodeError as e:
            return jsonify({'error': f'Failed to parse JSON: {str(e)}'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    else:
        return jsonify({'error': 'Invalid file type. Only PDF and DOCX are allowed.'}), 400

if __name__ == '__main__':
    # Create UPLOAD_FOLDER if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)