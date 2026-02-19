import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.scene_parser import parse_scenes
from modules.visual_generator import generate_image_prompt

def test_action_logic():
    print("[TEST] Verifying Action Description Flow...")
    
    # Mock transformed scene data from Gemini (as if from script_engine)
    mock_input_scenes = [
        {
            "scene_id": 1,
            "dialogue": "You think say you wise?",
            "action_description": "Sitting on the hood of a car, smoking a cigar, looking arrogant."
        }
    ]
    
    # 1. Test Parse Scenes
    print("\n--- Test 1: Parse Scenes Preservation ---")
    parsed_scenes = parse_scenes(mock_input_scenes)
    scene_1 = parsed_scenes[0]
    
    if scene_1.get("action_description") == "Sitting on the hood of a car, smoking a cigar, looking arrogant.":
        print("[PASS] parse_scenes preserved 'action_description'")
    else:
        print(f"[FAIL] parse_scenes dropped 'action_description'. Got: {scene_1}")

    # 2. Test Image Action Generation
    print("\n--- Test 2: Image Prompt Action Usage ---")
    
    # Case A: With action description
    prompt_with_action = generate_image_prompt(scene_1)
    if "smoking a cigar" in prompt_with_action:
        print("[PASS] Image prompt uses explicit action description.")
    else:
        print(f"[FAIL] Image prompt ignored action description. Output: {prompt_with_action}")
        
    # Case B: Without action description (Fallback)
    scene_no_action = {
        "scene_id": 1, 
        "phase": "Hook", 
        "character": "antagonist",
        "action_description": "" # Empty
    }
    prompt_fallback = generate_image_prompt(scene_no_action)
    
    # visual_generator default for Hook/Antagonist is "looking emotional or dramatic..."
    if "looking emotional or dramatic" in prompt_fallback:
        print("[PASS] Image prompt fell back to default logic correctly.")
    else:
        print(f"[FAIL] Image prompt fallback logic broken. Output: {prompt_fallback}")

if __name__ == "__main__":
    test_action_logic()
