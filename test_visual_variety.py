import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.visual_generator import generate_scene_setup_prompt, generate_image_prompt, OUTFIT_POOLS, HAIRSTYLES, MAKEUP, ACCESSORIES, LOCATION_POOL, POSTURE_POOL

def test_visual_variety():
    print("="*60)
    print("🧪 Testing Visual Variety Features")
    print("="*60)
    
    # Test 1: Random Scene Setup Variety
    print("\n--- Test 1: Scene Setup Variety ---")
    for i in range(3):
        prompt = generate_scene_setup_prompt()
        print(f"\n[Run {i+1}] Setup Prompt:")
        print(f"  {prompt[:200]}...")
        
        # Check for new keywords
        has_posture = any(p in prompt for p in POSTURE_POOL)
        has_location = any(l.split(',')[0] in prompt for l in LOCATION_POOL)
        has_hair = any(h in prompt for h in HAIRSTYLES)
        has_makeup = any(m in prompt for m in MAKEUP)
        has_acc = any(a in prompt for a in ACCESSORIES)
        
        print(f"  Posture detected: {has_posture}")
        print(f"  Location detected: {has_location}")
        print(f"  Hair/Makeup/Acc detected: {has_hair or has_makeup or has_acc}")

    # Test 2: Specific Image Prompt Variety
    print("\n--- Test 2: Image Prompt Variety (Specific Scene) ---")
    mock_scene = {
        "scene_id": 1, 
        "character": "antagonist", 
        "phase": "Hook", 
        "camera_angle": "Wide Shot"
    }
    
    for i in range(3):
        prompt = generate_image_prompt(mock_scene)
        print(f"\n[Run {i+1}] Image Prompt:")
        print(f"  {prompt[:200]}...")
        
        # Check for specific requested items
        requested_items = ["polo", "shirt", "jeans", "trousers", "jacket", "skirt", "glasses", "beads", "posture"]
        found_items = [item for item in requested_items if item.lower() in prompt.lower()]
        
        if found_items:
            print(f"  Found Variety Items: {', '.join(found_items)}")
        else:
            print("  No variety items found (Random luck, check next run)")

    print("\n" + "="*60)
    print("🎉 Visual Variety Testing Complete!")
    print("="*60)


def test_prop_generation():
    print("\n" + "="*60)
    print("🧪 Testing Prop Generation Features")
    print("="*60)
    
    from modules.visual_generator import generate_props
    
    # Test 1: Prop Generation Contents
    print("\n--- Test 1: Prop Generation Contents ---")
    props = generate_props(animation_style="3d_cgi")
    
    required_keys = ["hero", "antagonist", "setting"]
    for key in required_keys:
        exists = key in props
        length = len(props[key]) if exists else 0
        print(f"Prop '{key}' exists: {exists} (Length: {length})")
        if exists:
            print(f"  Content: {props[key][:100]}...")
            
    # Test 2: Animation Style Influence
    print("\n--- Test 2: Animation Style Influence ---")
    props_2d = generate_props(animation_style="2d_lofi")
    props_3d = generate_props(animation_style="3d_cgi")
    
    is_different = props_2d["hero"] != props_3d["hero"]
    print(f"2D and 3D props are different: {is_different}")
    print(f"  2D snippet: ...{props_2d['hero'][props_2d['hero'].find('Style:'):props_2d['hero'].find('Style:')+50]}...")
    print(f"  3D snippet: ...{props_3d['hero'][props_3d['hero'].find('Style:'):props_3d['hero'].find('Style:')+50]}...")

    print("\n" + "="*60)
    print("🎉 Prop Generation Testing Complete!")
    print("="*60)


if __name__ == "__main__":
    test_visual_variety()
    test_prop_generation()
