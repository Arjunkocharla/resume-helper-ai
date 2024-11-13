import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_text as extract_pdf_text
from docx import Document
from flask_cors import CORS 
import json
import anthropic
import re
from b2sdk.v2 import InMemoryAccountInfo, B2Api
import io
import tempfile
import time
from dotenv import load_dotenv
import boto3
from botocore.client import Config
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
import openai  # Import OpenAI for GPT
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

gpt_client = openai.OpenAI(
    api_key = os.getenv("GPT_API_KEY"),
)


# Configure upload folder and allowed extensions
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Backblaze B2 configuration
B2_KEY_ID = os.getenv('B2_KEY_ID')
B2_APPLICATION_KEY = os.getenv('B2_APPLICATION_KEY')
B2_BUCKET_NAME = os.getenv('B2_BUCKET_NAME')
B2_ENDPOINT = os.getenv('B2_ENDPOINT')

# Initialize B2 API
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)
bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)

# S3 client for generating pre-signed URLs
s3_client = boto3.client(
    's3',
    endpoint_url=B2_ENDPOINT,
    aws_access_key_id=B2_KEY_ID,
    aws_secret_access_key=B2_APPLICATION_KEY,
    config=Config(signature_version='s3v4')
)

# Initialize OpenAI API
openai.api_key = os.getenv('GPT_API_KEY')

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
    prompt = f"""As an expert HR specialist with deep knowledge of the {job_category} industry, analyze this resume for a {job_category} position, specifically for a Lead ML Engineer role.

1. Identify the top 8-9 most relevant keywords or phrases for this specific {job_category} role, considering current industry trends and job market demands.
2. For each keyword:
   a. Provide a brief explanation of its importance in the {job_category} field (1-2 sentences).
   b. Generate 1-2 impactful, ready-to-use bullet points that the candidate could directly add to their resume. These points should:
      - Integrate the identified keyword naturally
      - Be tailored specifically to the {job_category} position and the candidate's experience level (e.g., if the candidate is an entry-level or junior engineer, focus on foundational skills, relevant coursework, internships, or projects rather than managerial or advanced technical skills)
      - Highlight quantifiable achievements where possible, even if they are from academic projects or internships
      - Use strong action verbs
      - Demonstrate the candidate's potential impact and value in previous roles or projects

Resume text:
{resume_text}

Provide the output in this JSON format:
{{
  "keywords": [
    {{
      "keyword": "string",
      "importance": "string",
      "bullet_points": [
        "string",
        "string"
      ]
    }},
    ...
  ]
}}
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        temperature=0.2,
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
    retry = request.form.get('retry', 'false').lower() == 'true'

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file. Only PDF and DOCX are allowed.'}), 400

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    resume_text = extract_text(file_path)

    retry_prefix = """IMPORTANT: Previous response had JSON parsing errors. Please provide ONLY the JSON response in the exact format specified below. No additional text, explanations or casual conversation - just the parseable JSON response.

""" if retry else ""

    prompt = f"""{retry_prefix}As a senior resume analyst and ATS expert with extensive experience in multiple industries, conduct a comprehensive analysis of the following resume. Focus on ATS compatibility, keyword optimization, and industry-specific best practices.
    Respond ONLY with valid JSON in the exact format shown below and is parseable with json loads, with no additional text or explanations.
    1. "ATS_Compatibility_Score": An integer from 1-100 assessing how well the resume would perform in ATS scans. Consider factors such as formatting, use of standard section headings, and keyword relevance.

    2. "Keywords_Analysis": {{
        "Present_Keywords": An array of all relevant keywords found in the resume, sorted by importance.
        "Missing_Keywords": An array of important industry-standard keywords not present in the resume, based on the inferred job category.
        "Keyword_Density": A string representing the overall keyword density (e.g., "15.3%").
        "Keyword_Distribution": An object showing the distribution of keywords across different resume sections.
    }}

    3. "ATS_Friendly_Structure": {{
        "Format_Score": An integer from 1-10 assessing how ATS-friendly the resume format is.
        "Section_Order": An array of strings representing the current order of resume sections.
        "Recommended_Section_Order": An array of strings suggesting the ideal ATS-friendly section order.
        "Formatting_Issues": An array of specific formatting issues that could hinder ATS parsing.
    }}

    4. "Content_Analysis": {{
        "Total_Word_Count": An integer.
        "Bullet_Points_Count": An integer.
        "Action_Verbs_Count": An integer.
        "Quantifiable_Achievements_Count": An integer.
        "Average_Bullet_Length": A float representing the average number of words per bullet point.
        "Skills_Section_Analysis": An object analyzing the effectiveness of the skills section.
    }}

    5. "ATS_Optimization_Tips": An array of strings with specific, actionable recommendations to improve ATS compatibility and keyword usage. Prioritize the top 5 most impactful changes.

    6. "Strengths": An array of strings highlighting the resume's strong points, focusing on elements that would appeal to both ATS systems and human recruiters.

    7. "Industry_Specific_Suggestions": {{
        "Inferred_Industry": A string indicating the primary industry or job category this resume targets.
        "Industry_Keywords": An array of 20-30 highly relevant industry-specific keywords to consider incorporating, ranked by importance.
        "Industry_Specific_Tips": An array of strings with industry-specific advice for ATS optimization and standing out in the inferred field.
        "Emerging_Trends": An array of 3-5 emerging trends or skills in the inferred industry that could enhance the resume.
    }}

    8. "Overall_Assessment": A string (3-4 sentences) evaluating the resume's effectiveness for ATS and human review, highlighting major strengths and areas for improvement. Provide a clear, actionable next step for the candidate.

    9. "Industry_Standards": {{
        "Word_Count_Range": A string representing the typical word count range for resumes in this industry (e.g., "400-600").
        "Keyword_Density_Range": A string representing the ideal keyword density range (e.g., "2%-3.5%").
        "Bullet_Points_Range": A string representing the ideal number of bullet points (e.g., "15-25").
        "Sections_Importance": An object with section names as keys and importance scores (1-10) as values, tailored to the inferred industry.
        "Key_Action_Verbs": An array of 10-15 powerful action verbs commonly used in top resumes for this industry.
        "Ideal_Quantifiable_Achievements": An integer representing the ideal number of quantifiable achievements.
        "File_Format_Preference": A string indicating the preferred file format(s) for ATS (e.g., "PDF, DOCX").
        "Optimal_Length_Pages": A string representing the ideal resume length in pages (e.g., "1-2").
    }}

    10. "Tailored_Improvement_Plan": An array of 3-5 specific, prioritized steps the candidate should take to improve their resume's effectiveness, based on the analysis.

    Resume Text:
    {resume_text}

    Ensure all output is ATS-friendly, industry-specific, and focused on maximizing the resume's performance in both automated screening systems and human review. The JSON should be valid and parseable without errors. Do not include any text outside of the JSON structure.
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

        # Find the JSON part of the response
        json_start = response_content.find('{')
        json_end = response_content.rfind('}') + 1
        
        if json_start == -1 or json_end == 0:
            # If no JSON found, return a fallback response
            return jsonify({
                'ATS_Compatibility_Score': 50,
                'Keywords_Analysis': {
                    'Present_Keywords': [],
                    'Missing_Keywords': [],
                    'Keyword_Density': '0%',
                    'Keyword_Distribution': {}
                },
                'ATS_Friendly_Structure': {
                    'Format_Score': 5,
                    'Section_Order': [],
                    'Recommended_Section_Order': ['Contact Information', 'Summary', 'Experience', 'Education', 'Skills'],
                    'Formatting_Issues': ['Unable to analyze resume format']
                },
                'Content_Analysis': {
                    'Total_Word_Count': len(resume_text.split()),
                    'Bullet_Points_Count': 0,
                    'Action_Verbs_Count': 0,
                    'Quantifiable_Achievements_Count': 0,
                    'Average_Bullet_Length': 0.0,
                    'Skills_Section_Analysis': {}
                },
                'ATS_Optimization_Tips': ['Unable to generate specific recommendations'],
                'Strengths': ['Unable to identify specific strengths'],
                'Industry_Specific_Suggestions': {
                    'Inferred_Industry': 'Unknown',
                    'Industry_Keywords': [],
                    'Industry_Specific_Tips': [],
                    'Emerging_Trends': []
                },
                'Overall_Assessment': 'Unable to perform detailed analysis. Please ensure the resume is in a readable format.',
                'Industry_Standards': {
                    'Word_Count_Range': '400-600',
                    'Keyword_Density_Range': '2%-3.5%',
                    'Bullet_Points_Range': '15-25',
                    'Sections_Importance': {},
                    'Key_Action_Verbs': [],
                    'Ideal_Quantifiable_Achievements': 5,
                    'File_Format_Preference': 'PDF, DOCX',
                    'Optimal_Length_Pages': '1-2'
                },
                'Tailored_Improvement_Plan': ['Review resume format', 'Ensure content is readable', 'Try submitting again']
            }), 200

        # Extract and try to parse the JSON part
        json_str = response_content[json_start:json_end]
        try:
            analysis = json.loads(json_str)
            return jsonify(analysis), 200
        except json.JSONDecodeError:
            # If JSON is invalid, try to clean it up
            cleaned_json = json_str.replace('\n', ' ').replace('\r', '')
            try:
                analysis = json.loads(cleaned_json)
                return jsonify(analysis), 200
            except json.JSONDecodeError:
                # If still invalid, return the fallback response
                return jsonify({
                    'error': 'Failed to parse analysis results',
                    'message': 'The resume analysis service is temporarily unavailable. Please try again.'
                }), 500

    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An unexpected error occurred during analysis.'
        }), 500

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
    if 'resume' not in request.files or 'job_category' not in request.form:
        return jsonify({'error': 'Resume file and job category are required.'}), 400

    file = request.files['resume']
    job_category = request.form['job_category']

    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from resume
        resume_text = extract_text(file_path)
        word_count = len(resume_text.split())

        # Crafting the prompt
        prompt = f"""As an expert career advisor specializing in the {job_category} industry, analyze the following resume text and determine if the length is optimal for making a strong impression in this specific field. Consider current industry standards and expectations for the {job_category} sector.

        1. Provide a detailed analysis of the resume length, including:
           - The current word count
           - The ideal word count range for {job_category} resumes
           - Whether the resume is too short, too long, or just right
           - The impact of the current length on ATS scans and human readability

        2. If adjustments are needed, suggest specific ways to improve the resume length, such as:
           - Sections to expand or condense
           - Types of information to add or remove
           - Strategies for concise yet impactful writing in the {job_category} field

        3. Explain how the optimal length contributes to the overall effectiveness of the resume for {job_category} positions.

        4. Provide 2-3 industry-specific tips for balancing comprehensiveness with conciseness in {job_category} resumes.

        Resume Text:
        {resume_text}

        Format your response as a JSON object with the following structure:
        {{
          "current_word_count": integer,
          "ideal_word_count_range": "string",
          "length_assessment": "string",
          "ats_impact": "string",
          "human_readability_impact": "string",
          "improvement_suggestions": [
            "string",
            ...
          ],
          "length_importance_explanation": "string",
          "industry_specific_tips": [
            "string",
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
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the JSON part from the response
            response_content = response.content[0].text
            json_start = response_content.find('{')
            json_end = response_content.rfind('}') + 1
            analysis = json.loads(response_content[json_start:json_end])

            return jsonify(analysis), 200

        except json.JSONDecodeError as e:
            return jsonify({'error': f'Failed to parse JSON: {str(e)}'}), 500
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
    retry = request.form.get('retry', 'false').lower() == 'true'

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file. Only PDF and DOCX are allowed.'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    resume_text = extract_text(file_path)

    retry_prefix = """IMPORTANT: Previous response had JSON parsing errors. Please provide ONLY the JSON response in the exact format specified below. No additional text, explanations or casual conversation - just the parseable JSON response.

""" if retry else ""

    prompt = f"""{retry_prefix}As an expert ATS optimization specialist and industry recruiter, perform a deep analysis of this resume and job description to provide highly specific, tailored 6-7 keyword suggestions. Focus on actionable, industry-specific improvements that will maximize ATS scoring.
    Respond ONLY with valid JSON in the exact format shown below and is parseable with json loads, with no additional text or explanations.

1. First, analyze the resume to understand:
   - The candidate's current experience level and role
   - Technical skills, tools, and domain expertise
   - Industry-specific achievements and certifications
   - Current role and career trajectory
   - Existing keyword density and placement

2. Then, analyze the job description to identify:
   - Must-have technical skills, tools, and technologies
   - Required certifications and qualifications
   - Desired experience levels and competencies
   - Industry-specific terminology and frameworks
   - Key responsibilities and deliverables
   - Recurring keywords and their variations
   - Technology stack requirements
   - Domain-specific methodologies

3. Based on this analysis, provide:
   - High-impact keywords missing from the resume but crucial for ATS scoring
   - Existing keywords that need stronger emphasis or modern context
   - Industry-specific technical terms that would strengthen the application
   - Role-specific tools and technologies mentioned in the job description
   - Methodologies and frameworks valued in the industry
   - Measurable metrics and achievements using these keywords

For each keyword suggestion:
- Explain why it's specifically important for this role and industry
- Detail how it impacts ATS scoring and ranking
- Provide 2-3 ready-to-use bullet points that:
  * Incorporate the keyword naturally and with proper context
  * Include specific metrics and quantifiable achievements
  * Use strong action verbs aligned with seniority level
  * Are tailored to the candidate's experience level
  * Follow ATS-friendly formatting and keyword placement
  * Are industry-specific and technically accurate
  * Include relevant tools and methodologies
  * Demonstrate impact and results

Resume Text:
{resume_text}

Job Description:
{job_description}

Provide your response in the following JSON format:
{{
  "experience_gap_analysis": "A detailed analysis of the gap between current resume and job requirements",
  "keywords": [
    {{
      "keyword": "Specific technical or professional term",
      "importance": "Detailed explanation of why this keyword is crucial for this specific role and its impact on ATS scoring",
      "bullet_points": [
        {{
          "point": "Complete, ready-to-use bullet point with metrics and context",
          "explanation": "Why this bullet point is effective and how it strengthens the resume for ATS optimization"
        }}
      ],
      "placement": "Specific section where this keyword/bullet point should be added for maximum ATS impact"
    }}
  ],
  "overall_strategy": "Comprehensive strategy for implementing these changes effectively and optimizing ATS scoring"
}}
"""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_content = response.content[0].text
        json_start = response_content.find('{')
        json_end = response_content.rfind('}') + 1
        json_str = response_content[json_start:json_end]

        # Sanitize the JSON string
        json_str = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', json_str)

        # Add error handling for JSON parsing
        try:
            suggestions = json.loads(json_str)
        except json.JSONDecodeError as json_error:
            # If JSON parsing fails, return the error details
            return jsonify({
                'error': f'Failed to parse JSON: {str(json_error)}',
                'json_str': json_str,
                'error_position': json_error.pos,
                'error_lineno': json_error.lineno,
                'error_colno': json_error.colno
            }), 500

        return jsonify({
            'job_description': job_description,
            'keyword_suggestions': suggestions
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'Resume file is required.'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        try:
            # Initialize B2 API
            info = InMemoryAccountInfo()
            b2_api = B2Api(info)
            b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)

            # Get the bucket
            bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)

            # Upload the file
            file_data = file.read()
            file_info = bucket.upload_bytes(
                data_bytes=file_data,
                file_name=filename,
                content_type=file.content_type
            )

            # Verify the upload
            if not file_info or not file_info.id_:
                raise Exception("File upload failed: No file info returned")

            # Get the file URL
            download_url = b2_api.get_download_url_for_fileid(file_info.id_)

            # Verify the download URL
            if not download_url:
                raise Exception("Failed to generate download URL")

            # Use b2_api to get file info instead of bucket
            file_metadata = b2_api.get_file_info(file_info.id_)

            return jsonify({
                'message': 'File uploaded successfully',
                'filename': filename,
                'file_id': file_info.id_,
                'download_url': download_url,
                'file_size': file_metadata.size if file_metadata else None
            }), 200

        except Exception as e:
            app.logger.error(f"Upload error: {str(e)}")
            return jsonify({'error': f'Upload failed: {str(e)}'}), 500

    else:
        return jsonify({'error': 'Invalid file type. Only PDF, DOC, and DOCX are allowed.'}), 400

import os
from flask import send_file, request, jsonify
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from b2sdk.v2.exception import B2Error
import io

@app.route('/download_resume', methods=['GET'])
def download_resume():
    file_id = request.args.get('file_id')
    
    if not file_id:
        return jsonify({'error': 'file_id is required'}), 400

    try:
        # Initialize B2 API
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)

        # Get file info
        file_info = b2_api.get_file_info(file_id)

        if not file_info:
            return jsonify({'error': 'File not found'}), 404

        # Get the bucket
        bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)

        # Download the file to a BytesIO object
        download_buffer = io.BytesIO()
        bucket.download_file_by_id(file_id, download_buffer)
        download_buffer.seek(0)

        # Send the file
        return send_file(
            download_buffer,
            as_attachment=True,
            download_name=file_info.file_name,
            mimetype=file_info.content_type
        )

    except B2Error as e:
        app.logger.error(f"B2 API Error: {str(e)}")
        return jsonify({
            'error': f'B2 API Error: {str(e)}',
            'file_id': file_id
        }), 500
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        return jsonify({
            'error': f'Download failed: {str(e)}',
            'file_id': file_id
        }), 500

@app.route('/get_resume_download_url', methods=['GET'])
def get_resume_download_url():
    file_id = request.args.get('file_id')
    
    if not file_id:
        return jsonify({'error': 'file_id is required'}), 400

    try:
        # Initialize B2 API to get file info
        info = InMemoryAccountInfo()
        b2_api = B2Api(info)
        b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)

        # Get file info
        file_info = b2_api.get_file_info(file_id)

        if not file_info:
            return jsonify({'error': 'File not found'}), 404

        # Use boto3 to generate pre-signed URL
        s3_client = boto3.client(
            's3',
            endpoint_url=B2_ENDPOINT,  # Use the endpoint from environment variables
            aws_access_key_id=B2_KEY_ID,
            aws_secret_access_key=B2_APPLICATION_KEY,
            config=Config(signature_version='s3v4')
        )

        duration_in_seconds = 3600  # 1 hour

        # Generate the pre-signed URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': B2_BUCKET_NAME,
                'Key': file_info.file_name
            },
            ExpiresIn=duration_in_seconds
        )

        return jsonify({
            'download_url': presigned_url,
            'filename': file_info.file_name,
            'content_type': file_info.content_type,
            'size': file_info.size,
            'expires_in': duration_in_seconds
        }), 200

    except Exception as e:
        app.logger.error(f"Error generating pre-signed URL: {str(e)}")
        return jsonify({
            'error': f'Failed to generate pre-signed URL: {str(e)}',
            'file_id': file_id
        }), 500

def update_resume_via_gpt(resume_text, suggestions):
    messages = [
        {"role": "system", "content": "You are a resume editor."},
        {"role": "user", "content": f"Here is a resume and some suggestions for improvement. Please apply the suggestions to the resume.\n\nResume Text:\n{resume_text}\n\nSuggestions:\n{suggestions}\n\nReturn the updated resume text."}
    ]
    response = gpt_client.chat.completions.create(
        model="gpt-4",  # Use the appropriate model
        messages=messages,
        max_tokens=2000,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def create_pdf_with_text(text, output_path):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(10, 750, text)  # Adjust the position as needed
    can.save()

    packet.seek(0)
    with open(output_path, 'wb') as f:
        f.write(packet.getbuffer())

@app.route('/apply_suggestions', methods=['POST'])
def apply_suggestions():
    if 'resume' not in request.files or 'suggestions' not in request.form:
        return jsonify({'error': 'Resume file and suggestions are required.'}), 400

    file = request.files['resume']
    suggestions = json.loads(request.form['suggestions'])

    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file. Only PDF and DOCX are allowed.'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    resume_text = extract_text(file_path)

    # Generate suggestions using Claude
    prompt = f"""As an expert resume editor, analyze the following resume and suggestions. 
    Provide a list of specific changes to be made to the resume, including the exact text to be added, 
    removed, or modified, and the location of each change. Do not rewrite the entire resume.

    Resume Text:
    {resume_text}

    Suggestions:
    {json.dumps(suggestions, indent=2)}

    Please return your response in the following JSON format, that is parsable and json loads can handle:
    {{
        "changes": [
            {{
                "type": "add" | "remove" | "modify",
                "location": "section name or line number",
                "original_text": "text to be changed (for modify and remove)",
                "new_text": "text to be added or modified"
            }}
        ]
    }}
    """
    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            temperature=0.3,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Extract the suggestions from the Claude model response
        suggestions_text = response.content[0].text

        # Pass the resume text and suggestions to GPT for updates
        updated_resume_text = update_resume_via_gpt(resume_text, suggestions_text)

        # Create a new PDF with the updated resume text
        updated_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"updated_{filename}")
        create_pdf_with_text(updated_resume_text, updated_file_path)

        # Upload the updated file to Backblaze B2
        download_url = upload_to_backblaze(updated_file_path)

        return jsonify({'download_url': download_url}), 200

    except Exception as e:
        logging.error(f"Error in apply_suggestions: {e}")
        return jsonify({'error': str(e)}), 500

def upload_to_backblaze(file_path):
    # Initialize B2 API
    info = InMemoryAccountInfo()
    b2_api = B2Api(info)
    b2_api.authorize_account("production", B2_KEY_ID, B2_APPLICATION_KEY)

    # Get the bucket
    bucket = b2_api.get_bucket_by_name(B2_BUCKET_NAME)

    # Upload the file
    with open(file_path, 'rb') as file_data:
        file_info = bucket.upload_bytes(
            data_bytes=file_data.read(),
            file_name=os.path.basename(file_path),
            content_type='application/pdf'  # or 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' for DOCX
        )

    # Get the download URL
    download_url = b2_api.get_download_url_for_fileid(file_info.id_)
    return download_url

def apply_changes_to_file(file_path, changes):
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return apply_changes_to_pdf(file_path, changes)
    elif file_extension == '.docx':
        return apply_changes_to_docx(file_path, changes)
    else:
        raise ValueError("Unsupported file type")

def apply_changes_to_pdf(file_path, changes):
    # Read the existing PDF
    reader = PdfReader(file_path)
    output = PdfWriter()

    # Iterate over each page
    for page_number, page in enumerate(reader.pages):
        # Extract text from the page
        text = page.extract_text()

        # Apply changes
        for change in changes:
            if change['type'] == 'modify':
                text = text.replace(change['original_text'], change['new_text'])
            elif change['type'] == 'add':
                text += f"\n{change['new_text']}"
            elif change['type'] == 'remove':
                text = text.replace(change['original_text'], '')

        # Create a new PDF page with the modified text
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawString(10, 750, text)  # Adjust the position as needed
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfReader(packet)
        output.add_page(new_pdf.pages[0])

    # Save the updated PDF
    updated_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"updated_{os.path.basename(file_path)}")
    with open(updated_file_path, 'wb') as f:
        output.write(f)

    return updated_file_path

def apply_changes_to_docx(file_path, changes):
    doc = Document(file_path)
    
    for change in changes:
        if change['type'] == 'modify':
            for paragraph in doc.paragraphs:
                if change['original_text'] in paragraph.text:
                    paragraph.text = paragraph.text.replace(change['original_text'], change['new_text'])
        elif change['type'] == 'add':
            doc.add_paragraph(change['new_text'])
        elif change['type'] == 'remove':
            for paragraph in doc.paragraphs:
                if change['original_text'] in paragraph.text:
                    paragraph.text = paragraph.text.replace(change['original_text'], '')
    
    updated_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"updated_{os.path.basename(file_path)}")
    doc.save(updated_file_path)
    
    return updated_file_path

if __name__ == '__main__':
    # Create UPLOAD_FOLDER if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

