"""
Module A: The "Naija Vibe" Script Engine
Transforms Stoic Cole scripts into Nigerian Pidgin while preserving logic trap structure.
Uses Google Gemini API for AI transformation.
"""

import os
import json
import google.generativeai as genai
import re
from dotenv import load_dotenv

load_dotenv()

# Slang mapping dictionary
SLANG_MAP = {
    "high value man": "Odogwu",
    "high-value man": "Odogwu",
    "top man": "Top Man",
    "breakup": "breakfast",
    "break up": "breakfast",
    "broke up": "give breakfast",
    "financial struggle": "Sapa",
    "struggling financially": "dey for Sapa",
    "being scammed": "Maga",
    "scammed": "Maga",
    "used": "Spare Tire",
    "social media clout": "Wash",
    "clout": "Packaging",
    "controversial plan": "Format",
    "scheme": "Update",
    "don't back down": "No Gree For Anybody",
    "stand your ground": "No Gree For Anybody",
    "stay wise": "Stay Woke",
    "be smart": "Eye Don Open",
    "dollars": "Naira",
    "$": "N",
    "relationship": "situationship",
    "modern woman": "Slay Queen",
    "independent woman": "Boss Lady",
    "sigma male": "Original Man",
    "alpha male": "Odogwu",
}


def load_system_prompt():
    """Load the AI system prompt from file."""
    prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "system_prompt.txt")
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def apply_slang_mapping(text):
    """Apply Nigerian slang replacements to text."""
    result = text
    for english, naija in SLANG_MAP.items():
        # Case-insensitive replacement
        result = result.replace(english, naija)
        result = result.replace(english.capitalize(), naija)
        result = result.replace(english.upper(), naija.upper())
    return result


def transform_script(original_script: str, language_style: str = "pidgin", google_api_key: str = None, story_mode: str = "single") -> dict:
    """
    Transform a Stoic Cole script into Nigerian Pidgin format using Google Gemini.
    Returns a dict with 'scenes' list and 'setting_description'.
    
    Args:
        original_script: The original script text
        language_style: 'pidgin', 'mixed', or 'english'
        google_api_key: Optional Google API key (uses env var if not provided)
        story_mode: 'single' (13 scenes, 1 loc) or 'multi' (4 locs, 3-4 scenes each)
    
    Returns:
        dict with 'scenes' list and 'setting_description' (or 'locations' if multi)
    """
    # Get API key
    api_key = google_api_key or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found. Set GOOGLE_API_KEY environment variable.")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    
    # Use Gemini 2.5 Flash
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Load system prompt
    system_prompt = load_system_prompt()
    
    # DETERMINE LANGUAGE STYLE INSTRUCTIONS
    if language_style == "mixed":
        lang_instruction = "1. Rewrite into **Urban Lagos Mix (English + Spice)**. Characters should sound like educated Lagos professionals who switch codes naturally. Use professional English spiced with catchy Pidgin phrases and slang. Corporate but street-smart."
        end_phrase = "No gree for anybody"
    elif language_style == "english":
        lang_instruction = "1. Rewrite into **Standard Nigerian English**. Clear, grammatically correct, and sophisticated English as spoken by educated Nigerians. Use a distinct Nigerian tone and assertiveness, but ABSOLUTELY NO PIDGIN, NO STREET SLANG (no Sapa, no breakfast, no gree, etc.). Use formal Nigerian sentence structures (e.g., 'So, how can you explain this?' instead of 'How you wan explain this?'). Target an elite, corporate Nigerian professional audience."
        end_phrase = "Do not back down from your principles"
    else: # Default pidgin
        lang_instruction = "1. Rewrite into **Nigerian Pidgin (Vibe)** (Authentic Nigerian Pidgin English). Raw, expressive, and full of local street flavor (Warri/Lagos style)."
        end_phrase = "No gree for anybody"

    # DETERMINE STYLE NAME
    style_name = "Nigerian Vibe" if language_style == "pidgin" else ("Urban Lagos Mix" if language_style == "mixed" else "Standard Nigerian English")
    
    # STORY MODE SPECIFIC INSTRUCTIONS
    if story_mode == "multi":
        mode_instruction = """
        2. MANDATORY: Expand the story to span across **EXACTLY 4 DIFFERENT LOCATIONS** in Nigeria.
        3. Under EVERY location, generate **3 to 4 scenes** (total of 12-16 scenes for the entire video).
        4. Provide a distinct and detailed 'location_description' for each of the 4 locations.
        5. Ensure the narrative flows logically as characters move between these 4 settings.
        """
        output_format = """
        {
            "viral_title": "...",
            "locations": [
                {
                    "location_id": 1,
                    "location_description": "Detailed description of location 1...",
                    "scenes": [
                        {
                            "scene_id": 1,
                            "character": "...",
                            "camera_angle": "...",
                            "action_description": "...",
                            "dialogue": "..."
                        },
                        ...
                    ]
                },
                ...
            ]
        }
        """
    else:
        mode_instruction = """
        2. Expand to 13 scenes (90 seconds total, 7 seconds per scene)
        3. Keep protagonist calm and logical
        4. Make antagonist emotional/entitled (scenes 1-6)
        """
        output_format = """
        {
            "viral_title": "...",
            "setting_description": "...",
            "scenes": [
                {
                    "scene_id": 1,
                    "phase": "Hook",
                    "character": "antagonist", 
                    "camera_angle": "Medium Shot",
                    "action_description": "...",
                    "dialogue": "..."
                },
                ...
            ]
        }
        """

    # Create user prompt
    user_prompt = f"""Transform this Stoic Cole script into the {style_name} format.
    
    Target Style: {language_style.upper()}
    Story Mode: {story_mode.upper()}

Original Script:
{original_script}

Requirements:
{lang_instruction}
{mode_instruction}
5. Use Nigerian cultural references (Lagos, Lekki, etc.)
6. Convert currency to Naira
7. CRITICAL: Each scene = 10-15 words MAX (7-second dialogue)
8. **Analyze the script's visual context** to create detailed setting description(s).
9. **Describe specific character actions** for every scene.
10. **MAINTAIN VISUAL CONTINUITY** within each location.

Output Format: JSON ONLY.
{output_format}

End the final scene with "{end_phrase}"
"""
    
    # Combine system and user prompts
    combined_prompt = f"{system_prompt}\n\n{user_prompt}"
    
    # Call Gemini API
    try:
        response = model.generate_content(combined_prompt)
        transformed_text = response.text.strip()
        
        # Parse the response (JSON)
        result_data = parse_transformed_script(transformed_text)
        
        return {
            "success": True,
            "scenes": result_data.get("scenes", []),
            "setting_description": result_data.get("setting_description", ""),
            "locations": result_data.get("locations", []),
            "viral_title": result_data.get("viral_title", ""),
            "raw_output": transformed_text
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "scenes": [],
            "setting_description": "",
            "locations": []
        }


def parse_transformed_script(text: str) -> dict:
    """
    Parse the AI input which should be JSON, but handle fallback if it's not.
    """
    cleaned_text = text
    # Clean up markdown code blocks if present
    if "```json" in text:
        cleaned_text = text.replace("```json", "").replace("```", "")
    elif "```" in text:
        cleaned_text = text.replace("```", "")
    
    cleaned_text = cleaned_text.strip()
        
    try:
        # Try finding the first open brace and last close brace
        start_idx = cleaned_text.find('{')
        end_idx = cleaned_text.rfind('}')
        if start_idx != -1 and end_idx != -1:
            json_str = cleaned_text[start_idx:end_idx+1]
            data = json.loads(json_str)
            return data
            
    except json.JSONDecodeError:
        print("JSON Decode failed, attempting regex/legacy parse")
        pass
    
    # FALLBACK: Legacy parsing
    scenes = []
    current_scene = None
    current_dialogue = []
    
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        
        if line.upper().startswith("SCENE "):
            if current_scene:
                scenes.append({
                    "scene_id": current_scene,
                    "phase": "Unknown",
                    "character": "Unknown",
                    "camera_angle": "Unknown",
                    "action_description": "Standing naturally", # Default for fallback
                    "dialogue": '\n'.join(current_dialogue).strip()
                })
                current_dialogue = []
            
            try:
                # Extract number
                parts = line.upper().replace("SCENE ", "").split()
                num_part = re.sub(r'[^0-9]', '', parts[0])
                current_scene = int(num_part)
            except (ValueError, IndexError):
                current_scene = len(scenes) + 1
        
        elif line and current_scene:
            if not line.startswith('[') and not line.startswith('(') and not line.startswith('{'):
                current_dialogue.append(line)
    
    if current_scene and current_dialogue:
        scenes.append({
            "scene_id": current_scene,
            "dialogue": '\n'.join(current_dialogue).strip()
        })
        
    return {
        "scenes": scenes,
        "setting_description": "Lagos rooftop lounge with modern lighting" 
    }


if __name__ == "__main__":
    # Test the script engine
    test_script = """
    Woman: I deserve a man who earns at least $100,000 because I am a prize.
    Man: What do you bring to the table besides being a prize?
    """
    
    # Mocking environment for test if not set
    if not os.getenv("GOOGLE_API_KEY"):
        print("Please set GOOGLE_API_KEY to run test.")
    else:
        result = transform_script(test_script)
        
        if result["success"]:
            print("✅ Transformation successful!")
            print(f"Setting: {result.get('setting_description')}")
            for scene in result["scenes"]:
                print(f"Scene {scene.get('scene_id')}: {scene.get('action_description', 'N/A')} | {scene.get('dialogue')}")
        else:
            print(f"❌ Error: {result['error']}")
