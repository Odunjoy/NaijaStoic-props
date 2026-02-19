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
       - **RECURRING FAMILY**: If the story features a Father, Mother, or Triplets, use the names "Odogwu (Dad)", "Amaka (Mom)", and "Triplets (Ngozi, Chioma, Princess)".
       - **OTHERS**: For any other roles, use unique Nigerian names.
    2. **ONE IMAGE PER LOCATION**: The story MUST be written so that every scene within a location can take place using the SAME background image (The Location Setup Image). Scenes should focus on dialogue and motion within that frame.
    3. **DIALOGUE FORMAT**: Format all dialogue as: "[Character Name] says: [Dialogue]". 
       - Dialogue MUST be short (max 12-15 words) to fit under 6 seconds per scene.
    4. **NIGERIANIZATION**: Set in Nigeria with local slang and context. Improve drama for viral impact.
    5. **SFX**: Include a relevant Sound Effect (SFX) for EVERY scene.
    6. **DUAL OUTPUT**: Generate assets for BOTH a "Long Video" (4 locations) and a "Short Video" (3-5 scenes).
    7. **LANGUAGE**: Use {lang_desc}.
    8. **MINIMAL MOVEMENT**: Characters MUST stay on one spot at all times while talking. Avoid "walking", "pacing", or "running" unless absolutely critical for the story. Focus only on facial expressions and hand gestures.
    
    OUTPUT FORMAT (JSON ONLY):
    {{
      "long_video": {{
        "title": "Viral Clickbait Title",
        "description": "Engaging description",
        "tags": ["tag1", "tag2", "tag3"],
        "pov": "POV instruction",
        "locations": [
          {{
            "location_id": 1,
            "location_description": "Detailed setting description (Used to generate the ONLY image for this location)",
            "scenes": [
              {{
                "scene_id": 1,
                "character": "name",
                "action_description": "Specific action for motion prompt",
                "dialogue": "[Name] says: [Dialogue]",
                "sfx": "Short SFX description (e.g., Dramatic boom, car door slam, marketplace noise)"
              }}
            ]
          }}
        ]
      }},
      "short_video": {{
        "title": "Short Title",
        "description": "Short description",
        "tags": ["shorts", "naija"],
        "pov": "POV instruction",
        "scenes": [
          {{
            "scene_id": 1,
            "character": "name",
            "action_description": "Quick action",
            "dialogue": "[Name] says: [Dialogue]",
            "sfx": "Relevant SFX"
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
