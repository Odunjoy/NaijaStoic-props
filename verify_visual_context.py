import os
import sys
from dotenv import load_dotenv

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.visual_generator import generate_scene_setup_prompt, generate_image_prompt

def test_scene_setup_logic():
    print("[TEST] Testing Scene Setup Generation Logic...")
    
    # Case 1: No visual context, no story context (Should use Default)
    print("\n--- Test 1: Default Fallback ---")
    prompt_default = generate_scene_setup_prompt(visual_context=None)
    if "Lekki home" in prompt_default or "wardrobe" in prompt_default:
         print("[PASS] Used default location.")
    else:
         print(f"[FAIL] Did not use default location. Output: {prompt_default[:50]}...")

    # Case 2: Visual Context from YouTube (Should override everything)
    print("\n--- Test 2: YouTube Visual Context Override ---")
    yt_context = {"style": "Neon", "location": "Cyberpunk Market"}
    prompt_yt = generate_scene_setup_prompt(visual_context=yt_context)
    if "Cyberpunk Market" in prompt_yt:
        print("[PASS] YouTube location override successful.")
    else:
        print(f"[FAIL] YouTube location not used. Output: {prompt_yt[:50]}...")

    # Case 3: Script Analysis Context (Should be used if no YouTube context)
    # Note: In app.py, we pass the script analysis result AS 'visual_context' if no YT context exists.
    # So we simulate that here.
    print("\n--- Test 3: Script Analysis Setting Override ---")
    script_derived_context = {"location": "A muddy mechanic workshop in Yaba"} 
    # visual_generator.py expects a dict with 'location' key
    prompt_script = generate_scene_setup_prompt(visual_context=script_derived_context)
    
    if "muddy mechanic workshop" in prompt_script:
        print("[PASS] Script-derived location used successfully.")
    else:
        print(f"[FAIL] Script-derived location not used. Output: {prompt_script[:50]}...")

    # Case 4: Image Prompt with Script Context
    print("\n--- Test 4: Image Prompt with Script Context ---")
    mock_scene = {"scene_id": 1, "character": "protagonist", "phase": "Hook", "camera_angle": "Wide"}
    img_prompt = generate_image_prompt(mock_scene, visual_context=script_derived_context)
    
    if "muddy mechanic workshop" in img_prompt:
         print("[PASS] Image prompt uses script location.")
    else:
         print("[FAIL] Image prompt missing script location.")

if __name__ == "__main__":
    load_dotenv()
    test_scene_setup_logic()
