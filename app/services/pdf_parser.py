from pypdf import PdfReader
from typing import List, Dict
import os 

def parse_pdf(path : str) -> List[Dict]:
    reader = PdfReader(path)
    parsedPages = []
    
    filename = os.path.basename(path)
    
    for i , page in enumerate(reader.pages):
        text = page.extract_text()
        
        if text and text.strip():
            parsedPages.append({
                "page" : i+1,
                "text" : text.strip(),
                "source": filename
            })
            
    return parsedPages

    
