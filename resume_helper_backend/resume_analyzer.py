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

    prompt = f"""As an expert resume analyst and ATS specialist, analyze the following resume with a focus on ATS compatibility and keyword optimization. Provide a structured response in JSON format. The JSON should include:

    1. "ATS_Compatibility_Score": An integer from 1-100 assessing how well the resume would perform in ATS scans.

    2. "Keywords_Analysis": {{
        "Present_Keywords": An array of all relevant keywords found in the resume.
        "Missing_Keywords": An array of important industry-standard keywords not present in the resume.
        "Keyword_Density": A string representing the overall keyword density (e.g., "15.3%").
    }}

    3. "ATS_Friendly_Structure": {{
        "Format_Score": An integer from 1-10 assessing how ATS-friendly the resume format is.
        "Section_Order": An array of strings representing the current order of resume sections.
        "Recommended_Section_Order": An array of strings suggesting the ideal ATS-friendly section order.
    }}

    4. "Content_Analysis": {{
        "Total_Word_Count": An integer.
        "Bullet_Points_Count": An integer.
        "Action_Verbs_Count": An integer.
        "Quantifiable_Achievements_Count": An integer.
    }}

    5. "ATS_Optimization_Tips": An array of strings with specific, actionable recommendations to improve ATS compatibility and keyword usage.

    6. "Strengths": An array of strings highlighting the resume's strong points.

    7. "Industry_Specific_Suggestions": {{
        "Inferred_Industry": A string indicating the primary industry or job category this resume targets.
        "Industry_Keywords": An array of 20-30 highly relevant industry-specific keywords to consider incorporating.
        "Industry_Specific_Tips": An array of strings with industry-specific advice for ATS optimization.
    }}

    8. "Overall_Assessment": A string (3-4 sentences) evaluating the resume's effectiveness for ATS, highlighting major strengths and areas for improvement.

    9. "Industry_Standards": {{
        "Word_Count_Range": A string representing the typical word count range for resumes in this industry (e.g., "400-600").
        "Keyword_Density_Range": A string representing the ideal keyword density range (e.g., "2%-3.5%").
        "Bullet_Points_Range": A string representing the ideal number of bullet points (e.g., "15-25").
        "Sections_Importance": An object with section names as keys and importance scores (1-10) as values.
        "Key_Action_Verbs": An array of 10-15 powerful action verbs commonly used in top resumes for this industry.
        "Ideal_Quantifiable_Achievements": An integer representing the ideal number of quantifiable achievements.
        "File_Format_Preference": A string indicating the preferred file format(s) for ATS (e.g., "PDF, DOCX").
        "Optimal_Length_Pages": A string representing the ideal resume length in pages (e.g., "1-2").
    }}

    Resume Text:
    {resume_text}

    Ensure all output is ATS-friendly and focused on maximizing the resume's performance in automated screening systems. The JSON should be valid and parseable without errors. Do not include any text outside of the JSON structure.
    """

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=3000,
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