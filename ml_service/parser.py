import re
import unicodedata


def anonymize_resume(text: str) -> str:
    """
    1. Normalize Unicode (NFC)
    2. Lowercase all text
    3. Remove names, emails, phone numbers via regex
    4. Replace target school names with [TARGET_SCHOOL]
    5. Replace generic universities with [NON_TARGET_SCHOOL]
    6. Collapse whitespace to single spaces
    7. Return fully anonymized text
    """
    # normalize unicode
    text = unicodedata.normalize('NFC', text)
    
    # lowercase all text
    text = text.lower()
    
    # remove emails
    text = re.sub(r'\b[a-za-z0-9._%+-]+@[a-za-z0-9.-]+\.[a-z]{2,}\b', '[REDACTED_EMAIL]', text)
    
    # remove phone numbers (various formats)
    text = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '[REDACTED_PHONE]', text)
    text = re.sub(r'\b\(\d{3}\)\s*\d{3}-\d{4}\b', '[REDACTED_PHONE]', text)
    text = re.sub(r'\b\d{3}\.\d{3}\.\d{4}\b', '[REDACTED_PHONE]', text)
    text = re.sub(r'\b\d{10}\b', '[REDACTED_PHONE]', text)
    
    # remove common names (simple approach - replace common first names)
    common_names = [
        'john', 'jane', 'michael', 'sarah', 'david', 'jessica', 'james', 'emily',
        'robert', 'ashley', 'william', 'amanda', 'christopher', 'melissa', 'daniel',
        'jennifer', 'matthew', 'stephanie', 'andrew', 'nicole', 'joshua', 'elizabeth',
        'andre', 'athari', 'smith', 'johnson', 'williams', 'brown', 'jones', 'garcia'
    ]
    
    for name in common_names:
        text = re.sub(r'\b' + re.escape(name) + r'\b', '[REDACTED_NAME]', text)
    
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
