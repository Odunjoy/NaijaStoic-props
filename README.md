# 🧠 NaijaStoic Script Transformer

Transform "Stoic Cole" video scripts into viral Nigerian content packages with AI-powered cultural adaptation.

## 🎯 What It Does

NaijaStoic is an automated system that takes Western "Stoic/High-Value Man" scripts and outputs complete Nigerian production packages including:

- **Naija Script**: Nigerian Pidgin dialogue with authentic street-wise language
- **Image Prompts**: "Naija Lofi" 2D aesthetic prompts for DALL-E/Midjourney
- **Video Motion Prompts**: I2V prompts for Runway/Luma with subtle animations
- **SFX Suggestions**: Scene-specific sound effects with timing
- **SEO Package**: Viral titles, tags, and trending hashtags

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

```bash
# Navigate to the project directory
cd NaijaStoic

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter API Key**: Add your OpenAI API key in the sidebar
2. **Paste Script**: Input your original "Stoic Cole" script
3. **Configure SEO**: Choose auto-match or manually select from 58 templates
4. **Select Style**: Pick your visual aesthetic (Luxury, Casual, etc.)
5. **Click "Nigerianize"**: Transform the script
6. **Export JSON**: Download the complete production package

## 🎨 Features

### The "Naija Vibe" Engine
- Automatic Pidgin/Slang translation
- Cultural context adaptation (Lagos, Lekki, Sapa references)
- Currency conversion ($ → Naira)
- Preserves "logic trap" structure

### Viral Formula Structure
Every script follows the 3-act beat:
1. **Hook (0-10s)**: Antagonist's trigger statement
2. **Pivot (10-30s)**: Stoic's trap question
3. **Dunk (30-60s)**: Logic takedown with Nigerian context

### Visual Generation
- 2D Lofi animation aesthetic
- Purple/Teal/Gold color grading
- Lagos skyline backgrounds
- Character presets (Stoic Man, Expressive Woman)

### SEO Database
58 pre-loaded content templates with:
- Viral Nigerian titles
- Localized tags
- Trending hashtags (#nogreeforanybody, #fearwomen, etc.)

## 📁 Project Structure

```
NaijaStoic/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── README.md                       # This file
├── data/
│   └── seo_content.csv            # 58-row SEO database
├── modules/
│   ├── script_engine.py           # AI transformation engine
│   ├── scene_parser.py            # 3-scene breakdown
│   ├── visual_generator.py        # Image prompts
│   ├── motion_generator.py        # I2V prompts
│   ├── sfx_generator.py           # Sound effects
│   └── seo_mapper.py              # SEO matching
└── prompts/
    └── system_prompt.txt          # AI system instruction
```

## 💡 Example Output

```json
{
  "seo_data": {
    "title": "Odogwu vs Breakfast Distributor 🚩",
    "tags": ["Stoicism", "Nigeria", "Relationships"],
    "hashtags": ["#nogreeforanybody", "#fearwomen", "#naija"]
  },
  "scenes": [
    {
      "scene_id": 1,
      "shot_type": "Close-up (Antagonist)",
      "dialogue": "If you no get 50 Million for account, no talk to me...",
      "image_prompt": "Nigerian woman looking frustrated, talking, interior lofi apartment...",
      "i2v_motion_prompt": "Subtle head movement, talking, hair swaying...",
      "sfx": ["Low-tempo slowed + reverb Afrobeats", "Muffled city noise"]
    }
  ]
}
```

## 💰 Cost Estimate

- **Per transformation**: $0.03 - $0.10 (OpenAI API)
- **Image generation** (if using DALL-E): $0.04 per image × 3 scenes = $0.12
- **Total per video**: ~$0.15 - $0.25

## 🎯 Branding Guardrails

The system automatically enforces:
- ✅ Night/sunset lighting (Purple/Blue/Gold)
- ✅ Calm protagonist (never angry)
- ✅ Lagos/Lekki cultural references
- ✅ Naira currency
- ✅ Nigerian slang authenticity

## 🔧 Customization

### Add New SEO Templates

Edit `data/seo_content.csv` and add new rows:
```csv
id,original_title,naija_title,tags,hashtags
59,New Topic,Naija Title,"tag1,tag2","#hash1,#hash2"
```

### Modify Slang Dictionary

Edit `modules/script_engine.py` → `SLANG_MAP` dict

### Change Visual Presets

Edit `modules/visual_generator.py` → `CHARACTERS` and `SETTINGS` dicts

## 🐛 Troubleshooting

**Error: "OpenAI API key not found"**
- Make sure `.env` file exists with `OPENAI_API_KEY=your_key`

**Error: "SEO database not found"**
- Verify `data/seo_content.csv` exists
- Check file permissions

**Poor quality transformations**
- Try adjusting the system prompt in `prompts/system_prompt.txt`
- Increase the temperature parameter in `script_engine.py`

## 📚 Resources

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [DALL-E 3 Guide](https://platform.openai.com/docs/guides/images)
- [Runway ML](https://runwayml.com)
- [Luma AI](https://lumalabs.ai)

## 🤝 Contributing

This is a specialized tool for Nigerian content creators. Contributions welcome!

## 📄 License

MIT License - Free to use for personal and commercial projects

---

**Built with ❤️ for Nigerian content creators**

*No Gree For Anybody* 🧠🇳🇬
