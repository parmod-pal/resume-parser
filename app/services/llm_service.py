import os
import json
from groq import Groq
from app.models import ResumeData
from app.utils.logger import logger
from dotenv import load_dotenv


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in environment variables. Please add it to your .env file.")


client = Groq(api_key=GROQ_API_KEY)


GROQ_MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """You are an expert HR data extraction system. Your task is to extract structured information from a resume.
You MUST respond ONLY with valid JSON. Do not include any explanations, preambles, or markdown formatting.
If a field is not present in the text, use null for strings or [] for arrays. Do NOT hallucinate information."""

def extract_resume_data(text: str, regex_data: dict) -> ResumeData:
    """
    Sends raw resume text to Groq API and extracts structured data using Llama 3.
    """
    
    # We pass the regex_data in so the LLM doesn't have to guess the contact info
    extraction_prompt = f"""
    Parse the following resume text into JSON.
    I have already extracted the following contact info using deterministic rules: {json.dumps(regex_data)}. 
    Include these exact values in your final contact_information JSON output.
    
    Expected JSON Structure:
    {{
        "contact_information": {{"name": "", "email": "", "phone": "", "location": "", "urls": []}},
        "summary": "",
        "work_experience": [{{"company": "", "role": "", "duration": "", "responsibilities": []}}],
        "education": [{{"degree": "", "institution": "", "year": ""}}],
        "skills": [],
        "certifications": ["certification 1", "certification 2"]
    }}

    Resume Text:
    {text}
    """

    try:
        logger.info(f"Sending extraction prompt to Groq API using model: {GROQ_MODEL}...")
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": extraction_prompt}
            ],
            temperature=0.0, 
            response_format={"type": "json_object"} 
        )
        
        raw_response = response.choices[0].message.content
        logger.info("Successfully received response from Groq.")
        
        
        parsed_json = json.loads(raw_response)
        
        
        validated_data = ResumeData(**parsed_json)
        return validated_data
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from Groq: {e}\nRaw Output: {raw_response}")
        raise ValueError("Extraction failed: Model output was not valid JSON.")
    except Exception as e:
        logger.error(f"Groq API Error: {str(e)}")
        raise RuntimeError(f"Failed to communicate with LLM API: {str(e)}")