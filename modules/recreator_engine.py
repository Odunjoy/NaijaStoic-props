"""
Module: YouTube Story Recreator Engine
Transforms YouTube transcripts into Nigerianized dramatic stories with Long and Short assets.
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def recreate_story(transcript: str, language_style: str = "pidgin", google_api_key: str = None) -> dict:
    """
    Transform a YouTube transcript into a Nigerianized story with Long and Short version assets.
    """
    api_key = google_api_key or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Language switch
    if language_style == "mixed":
        lang_desc = "Urban Lagos Mix (English + Spice)"
    elif language_style == "english":
        lang_desc = "Standard Nigerian English (Formal & Sophisticated)"
    else:
        lang_desc = "Nigerian Pidgin (Raw Street Vibe)"

    prompt = f"""
    You are a Viral Content Creator specializing in Nigerian Dramas (NaijaStoic style).
    
    TASK:
    Recreate the following story transcript into a viral Nigerian dramatic story.
    
    INPUT TRANSCRIPT:
    {transcript}
    
    MANDATORY REQUIREMENTS:
    1. **CHARACTER NAMES**: Change all names to common Nigerian names. 
       - **RECURRING FAMILY**: If the story features a Father, Mother, or Triplets, use the names "Odogwu (Dad)", "Amaka (Mom)", and "Triplets (Ngozi, Chioma, Princess)". This ensures visual consistency.
       - **OTHERS**: For any other roles (friends, teachers, coworkers, etc.), use unique, varied Nigerian names (e.g., Segun, Funke, Chinedu, Onyeka) to make every story feel like a new production.
    2. **NIGERIANIZATION**: Set the story in Nigeria (Lagos, Abuja, Port Harcourt, etc.). Use local slang, culture, and context.
    3. **STORY ENHANCEMENT**: Make the story more "dramatic" and "interesting" for a social media audience. Add Nigerian logic traps or "mic drop" moments.
    4. **DUAL OUTPUT**: Generate assets for BOTH a "Long Video" (for YouTube main) and a "Short Video" (for Shorts/TikTok).
    5. **LANGUAGE**: Use {lang_desc}.
    
    OUTPUT FORMAT (JSON ONLY):
    {{
      "long_video": {{
        "title": "Viral Clickbait Title for Long Video",
        "description": "Engaging description with emojis",
        "tags": ["tag1", "tag2", "tag3", "nigeria", "drama"],
        "pov": "POV: You are watching a messy Lagos drama unfold. Edit with fast cuts and dramatic sound effects.",
        "locations": [
          {{
            "location_id": 1,
            "location_description": "Detailed setting description",
            "scenes": [
              {{
                "scene_id": 1,
                "character": "name",
                "action_description": "Specific action",
                "dialogue": "Nigerianized dialogue (15 words max)"
              }}
            ]
          }}
        ]
      }},
      "short_video": {{
        "title": "Viral Title for Short",
        "description": "Short description with hashtags",
        "tags": ["shorts", "naija", "drama"],
        "pov": "POV: The moment she realized... High energy edit.",
        "scenes": [
          {{
            "scene_id": 1,
            "action_description": "Quick action",
            "dialogue": "Punchy line (10 words max)"
          }}
        ]
      }}
    }}
    
    RULES:
    - Long Video: Generate EXACTLY 4 locations with 3-4 scenes each (12-16 scenes total).
    - Short Video: Generate EXACTLY 3-5 scenes total.
    - No markdown formatting in the output, just raw JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Simple JSON extraction
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
            
        return {
            "success": True,
            "data": json.loads(text),
            "raw": text
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
