import re

def preprocess(text:str) -> str:
    if not text or len(text.strip()) < 5:
        raise ValueError("Input text too short.")
    
    text = text.strip()
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)

    return text