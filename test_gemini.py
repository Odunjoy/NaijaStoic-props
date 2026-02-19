"""
Quick test of the Google Gemini transformation
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.script_engine import transform_script

# Test script
test_script = """
Woman: I deserve a man who earns at least $100,000 because I am a prize.
Man: What do you bring to the table besides being a prize?
Woman: My presence is the value. I shouldn't have to explain myself.
Man: So let me get this straight. You want a six-figure earner, but your only contribution is existing. That's not a relationship, that's a subscription service.
"""

print("=" * 60)
print("🧠 Testing NaijaStoic with Google Gemini")
print("=" * 60)
print("\n📝 Original Script:")
print(test_script)
print("\n🔄 Transforming with Gemini 2.0 Flash...\n")

# Transform
result = transform_script(test_script)

if result["success"]:
    print("✅ Transformation Successful!\n")
    print("🇳🇬 Nigerian Pidgin Output:")
    print("=" * 60)
    
    for scene in result["scenes"]:
        print(f"\nScene {scene['scene_id']}:")
        print("-" * 40)
        print(scene['dialogue'])
        print()
    
    print("=" * 60)
    print("✨ Cost: ~$0.001 (Gemini is 30-100x cheaper than OpenAI!)")
else:
    print(f"❌ Error: {result['error']}")

print("\n✅ Ready to run full app: streamlit run app.py")
