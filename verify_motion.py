import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.scene_parser import parse_scenes
from modules.motion_generator import generate_motion_prompt

def test_motion_logic():
    print("[TEST] Verifying Motion Prompt Flow...")
    
    # Mock scene with explicit action
    scene_with_action = {
        "scene_id": 9,
        "shot_type": "Medium Shot",
        "character": "antagonist",
        "action_description": "Throws her hands up in exasperation, face contorted in disbelief.",
        "dialogue": "Haba! You too dey see hook."
    }
    
    # Generate motion prompt
    motion_prompt = generate_motion_prompt(scene_with_action)
    print(f"\nGeneratred Motion Prompt: {motion_prompt}")
    
    if "Throws her hands up" in motion_prompt:
        print("[PASS] Motion prompt includes specific action.")
    else:
        print("[FAIL] Motion prompt ignored specific action.")

    # Mock scene WITHOUT action (fallback check)
    scene_no_action = {
        "scene_id": 1,
        "shot_type": "Close-up",
        "character": "protagonist"
    }
    
    fallback_prompt = generate_motion_prompt(scene_no_action)
    print(f"\nFallback Motion Prompt: {fallback_prompt}")
    
    if "Subtle blinking" in fallback_prompt or "listening calmly" in fallback_prompt:
        print("[PASS] Fallback logic works.")
    else:
        print("[FAIL] Fallback logic might be broken.")

if __name__ == "__main__":
    test_motion_logic()
