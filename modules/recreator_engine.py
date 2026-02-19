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
    2. **ONE IMAGE PER LOCATION**: Each location MUST be extracted from the actual transcript/story context. The `location_description` MUST be a rich, detailed, visually specific description of the actual setting (e.g. "a luxurious restaurant in Victoria Island Lagos, with white table cloths, dim candlelight, and floor-to-ceiling glass windows overlooking the harbor at night"). This description will be used directly to generate the background image. DO NOT use vague labels like 'kitchen' or 'office'. Every scene within a location reuses the SAME background image — focus on dialogue and character expressions.
    3. **DIALOGUE FORMAT**: Format all dialogue as: "[Character Name] says: [Dialogue]". 
       - Dialogue MUST be short (max 12-15 words) to fit under 6 seconds per scene.
    4. **NIGERIANIZATION**: Set in Nigeria with authentic Nigerian context and drama. Improve drama for viral impact.
    5. **SFX**: Include a relevant Sound Effect (SFX) for EVERY scene.
    6. **DUAL OUTPUT**: Generate assets for BOTH a "Long Video" (4 locations) and a "Short Video" (3-5 scenes).
    7. **LANGUAGE - STRICT RULE**: ALL dialogue MUST be written STRICTLY in {lang_desc}. This is NON-NEGOTIABLE. Do NOT mix languages. Do NOT switch to Pidgin if English is selected.
    8. **ZERO CHARACTER MOVEMENT + POSTURE AWARENESS**: Characters MUST stay completely stationary at all times. They MUST NOT walk, pace, run, or move between scenes. Location changes happen via SCENE CUTS only.
       - If the location is a SEATED setting (auditorium, restaurant, cafe, car, classroom, office desk, boardroom, courtroom): Characters are SEATED. `action_description` MUST describe seated actions only — e.g. "leans forward in seat", "grips armrest", "turns in chair", NOT "walks" or "stands up".
       - If the location is a STANDING setting (hallway, rooftop, market, street, living room): Characters STAND still. `action_description` describes standing posture only.
    
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
                "action_description": "POSTURE-AWARE action: If location is a seated setting (auditorium, restaurant, car, etc.) → describe only seated actions (e.g. 'shifts in seat', 'leans toward other character'). If standing location → describe only standing gestures. NEVER include walking or movement between positions.",
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
