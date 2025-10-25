import re
import unicodedata
import os
import google.generativeai as genai


# Configure Google Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Use Gemini 1.5 Flash for fast and efficient processing
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    gemini_model = None
    print("WARNING: GEMINI_API_KEY not set. Using fallback anonymization method.")


def anonymize_resume(text: str) -> str:
    """
    Anonymize resume text by removing personally identifiable information.
    Uses Google Gemini LLM when API key is available, otherwise falls back to basic regex.
    
    Removes:
    1. Names (people, not projects/frameworks)
    2. Emails
    3. Phone numbers
    4. School names (categorized as target/non-target)
    
    Returns fully anonymized text with normalized Unicode and lowercase.
    """
    # normalize unicode
    text = unicodedata.normalize('NFC', text)
    
    # lowercase all text
    text = text.lower()
    
    if gemini_model and GEMINI_API_KEY:
        # Use Gemini LLM for intelligent anonymization
        try:
            prompt = f"""You are a resume anonymization system designed to remove personally identifiable information while preserving technical skills, project names, and framework names.

CRITICAL INSTRUCTIONS:
1. Remove ALL person names (first names, last names) - replace with [REDACTED_NAME]
2. Remove ALL email addresses - replace with [REDACTED_EMAIL]
3. Remove ALL phone numbers in any format - replace with [REDACTED_PHONE]
4. Replace Ivy League and top-tier schools (MIT, Stanford, Harvard, Princeton, Yale, Columbia, UPenn, Dartmouth, Brown, Cornell, Caltech, UC Berkeley, UCLA, Carnegie Mellon, Georgia Tech, etc.) with [TARGET_SCHOOL]
5. Replace all other universities and colleges with [NON_TARGET_SCHOOL]
6. PRESERVE technical terms, programming languages (Python, JavaScript, Java, etc.), frameworks (React, TensorFlow, FastAPI, etc.), and project names
7. PRESERVE non-words that are technology names (e.g., "JGrasp" is a programming tool, keep it as-is)
8. DO NOT remove or replace words that are technical skills or technologies
9. Return ONLY the anonymized text, no explanations or additional formatting
10. Maintain the original structure and line breaks

Resume text to anonymize:
{text}

Return the anonymized resume text:"""

            response = gemini_model.generate_content(prompt)
            anonymized_text = response.text.strip()
            
            # Ensure it's still lowercase and normalized
            anonymized_text = anonymized_text.lower()
            anonymized_text = re.sub(r'\s+', ' ', anonymized_text)
            anonymized_text = anonymized_text.strip()
            
            return anonymized_text
            
        except Exception as e:
            print(f"Warning: Gemini API failed ({e}), falling back to regex-based anonymization")
            # Fall through to regex-based method
    
    # Fallback: Basic regex-based anonymization when LLM unavailable
    # remove emails
    text = re.sub(r'\b[a-za-z0-9._%+-]+@[a-za-z0-9.-]+\.[a-z]{2,}\b', '[REDACTED_EMAIL]', text)
    
    # remove phone numbers (various formats)
    text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[REDACTED_PHONE]', text)
    text = re.sub(r'\b\(\d{3}\)\s*\d{3}-\d{4}\b', '[REDACTED_PHONE]', text)
    text = re.sub(r'\b\d{3}\.\d{3}\.\d{4}\b', '[REDACTED_PHONE]', text)
    text = re.sub(r'\b\d{10}\b', '[REDACTED_PHONE]', text)
    
    # replace target schools (ivy league and top tech schools)
    target_schools = [
        'mit', 'stanford', 'harvard', 'princeton', 'yale', 'columbia', 'upenn',
        'dartmouth', 'brown', 'cornell', 'caltech', 'uchicago', 'northwestern',
        'duke', 'johns hopkins', 'vanderbilt', 'rice', 'notre dame', 'georgetown',
        'carnegie mellon', 'emory', 'berkeley', 'ucla', 'usc', 'nyu', 'tufts',
        'boston university', 'northeastern', 'georgia tech', 'university of michigan',
        'massachusetts institute of technology', 'california institute of technology'
    ]
    
    for school in target_schools:
        text = re.sub(r'\b' + re.escape(school) + r'\b', '[TARGET_SCHOOL]', text)
    
    # replace generic universities
    university_patterns = [
        r'\b\w+ university\b',
        r'\b\w+ college\b',
        r'\b\w+ institute\b',
        r'\buniversity of \w+\b',
        r'\bcollege of \w+\b'
    ]
    
    for pattern in university_patterns:
        text = re.sub(pattern, '[NON_TARGET_SCHOOL]', text)
    
    # Simple name detection using common patterns (fallback only)
    # This is basic and won't catch all names, but prevents nothing from being redacted
    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[REDACTED_NAME]', text)
    
    # collapse whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text


def extract_top_terms(text: str, n: int = 5) -> list:
    """
    Extract top n frequent meaningful terms from text for explanation
    """
    # simple tokenization and frequency counting
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    
    # filter out common stop words
    stop_words = {
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
        'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
        'how', 'man', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did',
        'its', 'let', 'put', 'say', 'she', 'too', 'use', 'with', 'have', 'this',
        'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good', 'much',
        'some', 'time', 'very', 'when', 'come', 'here', 'just', 'like', 'long',
        'make', 'many', 'over', 'such', 'take', 'than', 'them', 'well', 'were'
    }
    
    meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # count frequencies
    word_freq = {}
    for word in meaningful_words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # return top n terms
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:n]]
