# 🚀 Quick Start Guide - NaijaStoic

## Step-by-Step Setup

### 1. Install Dependencies

Since there was a network issue during install, run this when you have internet:

```bash
cd C:\Users\Bodunde\Desktop\Antigravity\NaijaStoic
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web app framework
- `openai` - AI transformation engine
- `pandas` - CSV database handling
- `python-dotenv` - Environment management

### 2. Add Your OpenAI API Key

Edit the `.env` file and add your API key:

```
OPENAI_API_KEY=sk-your-actual-key-here
```

Get your key from: https://platform.openai.com/api-keys

**Cost Estimate**: Each script transformation costs **$0.03 - $0.10**

### 3. Test the Modules

Run the test script to verify everything works:

```bash
python test_modules.py
```

You should see all 6 modules pass their tests ✅

### 4. Run the App

Start the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 How to Use the App

1. **Open the App**: Click the local URL or it should open automatically
2. **Enter API Key**: Paste your OpenAI key in the sidebar (if not in .env)
3. **Paste Script**: Input your Stoic Cole script in the left panel
4. **Configure**:
   - Choose "Auto-match" or select a specific SEO template (1-58)
   - Pick your visual style (Luxury, Casual, etc.)
5. **Click "Nigerianize"**: Transform the script
6. **Review Output**:
   - See the Nigerian Pidgin dialogue
   - View image prompts for each scene
   - Check motion prompts for video
   - Review SFX suggestions
7. **Export**: Download the complete JSON package

## 📋 What You'll Get

The output JSON contains everything you need for production:

```json
{
  "seo_data": {
    "title": "Viral Nigerian Title 🚩",
    "tags": ["Stoicism", "Nigeria", "Relationships"],
    "hashtags": ["#nogreeforanybody", "#fearwomen"]
  },
  "scenes": [
    {
      "scene_id": 1,
      "shot_type": "Close-up (Antagonist)",
      "dialogue": "Nigerian Pidgin dialogue here...",
      "image_prompt": "Full DALL-E/Midjourney prompt...",
      "i2v_motion_prompt": "Runway/Luma motion prompt...",
      "sfx": ["Sound effect 1", "Sound effect 2"]
    }
  ]
}
```

## 🎨 Using the Output

### For Images (DALL-E 3 / Midjourney)
Copy the `image_prompt` for each scene into your image AI tool.

### For Videos (Runway Gen-3 / Luma)
1. Generate the image first
2. Use the `i2v_motion_prompt` to animate it

### For Sound
Use the SFX list to find:
- Background music (Afrobeats, lofi)
- Sound effects (record scratch, bass thud)
- Timing markers for editing

## 💡 Tips for Best Results

1. **Write Clear Scripts**: The AI works best with dialogue-heavy scripts
2. **Use the Sample**: Click "Load sample script" to see the format
3. **Match SEO Manually**: For specific topics, manually select the SEO template
4. **Iterate**: If the output isn't perfect, try again with tweaked input

## 🐛 Troubleshooting

**"OpenAI API key not found"**
- Make sure .env file exists with your key
- Or enter it directly in the sidebar

**"SEO database not found"**
- Verify `data/seo_content.csv` exists
- It should have been created automatically

**"Poor quality transformations"**
- Try the sample script first to verify it works
- Ensure your script has clear dialogue
- Check that your API key has credits

## 📊 The 58 SEO Templates

The app includes 58 pre-loaded Nigerian content themes:

1. Odogwu vs Breakfast Distributor
2. Who Dey Pay The Bills?
3. Wetin Be Emotional Labor?
4. The Format Don Leak
... (55 more)

Each has:
- ✅ Viral Nigerian title
- ✅ Relevant tags
- ✅ Trending hashtags

## 🎬 Production Workflow

**Recommended workflow:**

1. **Script** → Use NaijaStoic app
2. **Images** → Generate 3 scenes with DALL-E/Midjourney
3. **Video** → Animate images with Runway/Luma
4. **Audio** → Add voiceover + SFX
5. **Edit** → Assemble in CapCut/DaVinci Resolve
6. **Upload** → TikTok, Instagram Reels, YouTube Shorts

## 💰 Cost Breakdown

- Script transformation: **$0.03 - $0.10**
- Image generation (DALL-E 3): **$0.04 × 3 = $0.12**
- Video animation (Runway): **~$0.40** (depends on plan)
- **Total per video**: ~$0.55 - $0.62

## 🚨 Important Notes

- ✅ The app generates **prompts only** by default (cost-effective)
- ✅ You can manually call image/video APIs if you prefer
- ✅ All cultural references are authentic Nigerian slang
- ✅ The "Logic Trap" structure is preserved automatically

---

**Need Help?** Check the main `README.md` for full documentation.

**Ready to create viral Nigerian Stoic content?** 🧠🇳🇬

Let's get started! 🚀
