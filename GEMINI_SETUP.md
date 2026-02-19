# 🔧 Google Gemini API Setup Guide

## Issue: API Model Not Found

If you're seeing this error:
```
404 models/gemini-1.5-pro-latest is not found
```

This means your Google API key might be for a different API service. Here's how to fix it:

---

## Option 1: Get Google AI Studio API Key (Recommended)

1. **Go to Google AI Studio**: https://aistudio.google.com/app/apikey
2. **Create API Key** or use existing one
3. **Important**: Make sure it's for "Google AI Studio" (not Google Cloud)
4. **Copy the API key** to `.env` file:
   ```
   GOOGLE_API_KEY=AIzaSy...
   ```

---

## Option 2: Use OpenAI Instead (Simpler)

If Gemini setup is causing issues, I can quickly switch the app back to OpenAI.

**Steps:**
1. Get OpenAI API key from: https://platform.openai.com/api-keys
2. Run in the NaijaStoic folder:
   ```bash
   pip uninstall google-generativeai
   pip install openai
   ```
3. Let me know and I'll revert the code to use OpenAI

**Cost comparison:**
- OpenAI GPT-4: $0.03-$0.10 per transformation
- Google Gemini: $0.001 per transformation (100x cheaper!)

---

## Option 3: Test Available Models

Run this to see what models your API key has access to:

```python
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY_HERE")

print("Available models:")
for model in genai.list_models():
    print(f"  - {model.name}")
```

Then update `.env` with the correct model name:
```
GEMINI_MODEL=models/gemini-pro
```

---

## ✅ Current App Status

**What's Working:**
- ✅ All 6 module tests pass
- ✅ Scene parser, Visual generator, Motion generator working
- ✅ SFX generator, SEO mapper working
- ✅ Streamlit UI built and ready
- ✅ 58-row SEO database loaded

**What Needs Your Help:**
- ⚠️ Gemini API model configuration
- ⚠️ API key verification

---

## 🚀 Next Steps

1. **Choose your preferred option** above
2. **If using Gemini**: Verify API key from Google AI Studio
3. **If using OpenAI**: Let me know and I'll switch the code back
4. **Run the app**: `streamlit run app.py`

---

## 💬 Need Help?

Just let me know which option you prefer and I'll guide you through it!

**No Gree For Anybody!** 🧠🇳🇬
