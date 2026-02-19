"""
Test Script for NaijaStoic Modules
Run this to verify all modules work correctly before using the full app.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("🧪 NaijaStoic Module Test Suite")
print("=" * 60)

# Test 1: Scene Parser
print("\n1️⃣ Testing Scene Parser...")
try:
    from modules.scene_parser import parse_scenes, validate_scene_structure
    
    test_scenes = [
        {"scene_id": 1, "dialogue": "Test dialogue 1"},
        {"scene_id": 2, "dialogue": "Test dialogue 2"},
        {"scene_id": 3, "dialogue": "Test dialogue 3"}
    ]
    
    parsed = parse_scenes(test_scenes)
    validation = validate_scene_structure(parsed)
    
    if validation["valid"]:
        print("   ✅ Scene Parser working correctly")
    else:
        print(f"   ❌ Scene Parser validation failed: {validation['issues']}")
except Exception as e:
    print(f"   ❌ Scene Parser error: {e}")

# Test 2: Visual Generator
print("\n2️⃣ Testing Visual Generator...")
try:
    from modules.visual_generator import generate_image_prompt
    
    test_scene = {
        "scene_id": 1,
        "shot_type": "Close-up (Antagonist)",
        "character": "antagonist"
    }
    
    prompt = generate_image_prompt(test_scene)
    
    if "2D animation" in prompt and "Lofi" in prompt:
        print("   ✅ Visual Generator working correctly")
        print(f"   Sample: {prompt[:80]}...")
    else:
        print("   ❌ Visual Generator output missing required elements")
except Exception as e:
    print(f"   ❌ Visual Generator error: {e}")

# Test 3: Motion Generator
print("\n3️⃣ Testing Motion Generator...")
try:
    from modules.motion_generator import generate_motion_prompt
    
    test_scene = {
        "scene_id": 2,
        "shot_type": "Wide Shot",
        "character": "protagonist"
    }
    
    motion = generate_motion_prompt(test_scene)
    
    if "Subtle" in motion and "2D" in motion:
        print("   ✅ Motion Generator working correctly")
        print(f"   Sample: {motion[:80]}...")
    else:
        print("   ❌ Motion Generator output missing required elements")
except Exception as e:
    print(f"   ❌ Motion Generator error: {e}")

# Test 4: SFX Generator
print("\n4️⃣ Testing SFX Generator...")
try:
    from modules.sfx_generator import suggest_sfx, generate_sfx_manifest
    
    test_scenes = [
        {"scene_id": 1, "character": "antagonist"},
        {"scene_id": 2, "character": "protagonist"},
        {"scene_id": 3, "character": "protagonist"}
    ]
    
    manifest = generate_sfx_manifest(test_scenes)
    
    if "music_tracks" in manifest and "scene_sfx" in manifest:
        print("   ✅ SFX Generator working correctly")
        print(f"   Music tracks: {len(manifest['music_tracks'])} sections")
        print(f"   Scene SFX: {len(manifest['scene_sfx'])} scenes")
    else:
        print("   ❌ SFX Generator output incomplete")
except Exception as e:
    print(f"   ❌ SFX Generator error: {e}")

# Test 5: SEO Mapper
print("\n5️⃣ Testing SEO Mapper...")
try:
    from modules.seo_mapper import load_seo_database, match_content, get_trending_hashtags
    
    db = load_seo_database()
    test_script = "She want me to pay bills"
    seo = match_content(test_script, db)
    trending = get_trending_hashtags()
    
    if seo and "title" in seo and len(trending) > 0:
        print("   ✅ SEO Mapper working correctly")
        print(f"   Database entries: {len(db)}")
        print(f"   Matched title: {seo['title']}")
        print(f"   Trending tags: {len(trending)} hashtags")
    else:
        print("   ❌ SEO Mapper output incomplete")
except Exception as e:
    print(f"   ❌ SEO Mapper error: {e}")

# Test 6: Script Engine (requires API key)
print("\n6️⃣ Testing Script Engine...")
try:
    from modules.script_engine import load_system_prompt, apply_slang_mapping
    
    # Test slang mapping (doesn't need API)
    test_text = "High value man facing breakup"
    mapped = apply_slang_mapping(test_text)
    
    # Test system prompt loading
    prompt = load_system_prompt()
    
    if "Odogwu" in mapped and len(prompt) > 100:
        print("   ✅ Script Engine (slang mapping) working correctly")
        print(f"   Mapped: '{test_text}' → '{mapped}'")
        print("   ⚠️  Full transformation requires OpenAI API key")
    else:
        print("   ❌ Script Engine incomplete")
except Exception as e:
    print(f"   ❌ Script Engine error: {e}")

print("\n" + "=" * 60)
print("🎉 Module Testing Complete!")
print("=" * 60)
print("\nNext Steps:")
print("1. Add your OpenAI API key to .env file")
print("2. Run: pip install -r requirements.txt")
print("3. Run: streamlit run app.py")
print("\n" + "=" * 60)
