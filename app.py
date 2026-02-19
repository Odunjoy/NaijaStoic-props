"""
NaijaStoic Script Transformer
Main Streamlit Application
"""

import streamlit as st
import json
import os
import glob
import random
from dotenv import load_dotenv

# Import our modules
from modules.script_engine import transform_script
from modules.scene_parser import parse_scenes, validate_scene_structure
from modules.visual_generator import generate_image_prompt, get_style_variations, generate_scene_setup_prompt, analyze_visual_style, OUTFIT_POOLS, generate_image_prompt_condensed, generate_props
from modules.motion_generator import generate_motion_prompt
from modules.sfx_generator import suggest_sfx, generate_sfx_manifest
from modules.seo_mapper import load_seo_database, match_content, get_seo_by_id, list_all_titles
from modules.youtube_utils import download_video, extract_frames, get_video_info, get_transcript
from modules.recreator_engine import recreate_story
from modules.metadata_manager import generate_scene_metadata, generate_video_metadata, add_pov_context_to_seo
from constants import FEMALE_VOICE_SPEC, MALE_VOICE_SPEC # Import voice specs from constants

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="NaijaStoic Script Transformer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #8B5CF6 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        text-align: center;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .scene-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: white;
    }
    .success-box {
        background: #10b981;
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🧠 NaijaStoic Script Transformer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Transform Stoic Cole scripts into viral Nigerian content</p>', unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.header("🧭 Navigation")
        app_mode = st.radio(
            "Choose Tool",
            ["Script Transformer", "YouTube Scene Extractor"],
            index=0
        )
        st.markdown("---")
    
    if app_mode == "Script Transformer":
        render_script_transformer()
    elif app_mode == "YouTube Scene Extractor":
        render_youtube_extractor()


def render_youtube_extractor():
    """Render the YouTube Scene Extractor UI."""
    st.header("📺 YouTube Scene Extractor")
    st.info("Extract major scene screenshots from YouTube videos to help visualize and recreate context.")
    
    # URL Input - keep key stable to persist input
    url = st.text_input("YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...", key="yt_url_input")
    
    if url:
        # Get video info first (only if new URL or not implicitly stored? Streamlit handles caching if just re-running)
        # Using session state to avoid re-fetching on every run if URL hasn't changed
        if 'last_url' not in st.session_state or st.session_state['last_url'] != url:
            with st.spinner("Fetching video info..."):
                info = get_video_info(url)
                if info:
                    st.session_state['video_info'] = info
                    st.session_state['last_url'] = url
                else:
                    st.error("Could not fetch video info. Please check the URL.")
                    
        # Display Info if available
        if 'video_info' in st.session_state:
            info = st.session_state['video_info']
            st.success(f"Found: **{info['title']}** ({info['duration']}s)")
            if info['thumbnail']:
                st.image(info['thumbnail'], width=320)
                
            # Settings
            col1, col2 = st.columns(2)
            with col1:
                num_frames = st.slider("Number of screenshots to extract", 3, 12, 6)
            
            # Process button
            if st.button("📸 Extract Scenes", type="primary"):
                process_youtube_video(url, num_frames)
                st.rerun() # Rerun to update the view immediately with new frames

    # PERSISTENT DISPLAY - Check session state for frames regardless of button press
    if 'extracted_frames' in st.session_state and st.session_state['extracted_frames']:
        frames = st.session_state['extracted_frames']
        st.markdown("---")
        st.subheader(f"📸 Extracted Scenes ({len(frames)})")
        
        # Display in grid
        cols = st.columns(3)
        for i, frame_path in enumerate(frames):
            with cols[i % 3]:
                st.image(frame_path, caption=f"Scene {i+1}", use_column_width=True)

        # Video Context Analysis Section (Persistent)
        st.markdown("---")
        st.subheader("🎨 Visual Style Analysis")
        
        # Check if we already have analysis results
        if 'visual_context' in st.session_state and st.session_state['visual_context']:
            analysis_result = st.session_state['visual_context']
            st.success("✅ Style Analyzed! Switch to 'Script Transformer' to use it.")
            
            if isinstance(analysis_result, dict):
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Detected Style:** {analysis_result.get('style')}")
                with col2:
                    st.success(f"**Detected Location:** {analysis_result.get('location')}")
            else:
                st.info(f"**Detected Style:** {analysis_result}")
            
            if st.button("🔄 Re-Analyze Visual Style"):
                # Clear and re-run analysis logic
                perform_visual_analysis()
        else:
            if st.button("✨ Analyze Visual Style for Script Transformer"):
                perform_visual_analysis()


def perform_visual_analysis():
    """Helper to run the analysis logic."""
    if 'extracted_frames' not in st.session_state:
        return

    api_key = os.getenv("GOOGLE_API_KEY") or st.text_input("Enter Google API Key for Analysis", type="password")
    if api_key:
        with st.spinner("Analyzing visual style of extracted frames..."):
            analysis_result = analyze_visual_style(st.session_state['extracted_frames'], api_key)
        
        if analysis_result:
            st.session_state['visual_context'] = analysis_result
            st.rerun() # Refresh to show results
        else:
            st.error("Could not analyze images. Check API key and quotas.")
    else:
        st.warning("API Key needed for analysis.")


def process_youtube_video(url, num_frames):
    """Handle the download and extraction process."""
    status_text = st.empty()
    progress_bar = st.progress(0)
    
    # Step 1: Download
    status_text.text("⬇️ Downloading video... (this may take a moment)")
    progress_bar.progress(10)
    
    video_path = download_video(url, "temp_downloads")
    
    if not video_path:
        status_text.text("❌ Download failed.")
        st.error("Failed to download video. Please check your internet connection or the URL.")
        return
        
    progress_bar.progress(50)
    status_text.text("🎞️ Extracting frames...")
    
    # Step 2: Extract Frames
    frames = extract_frames(video_path, "temp_frames", num_frames)
    
    progress_bar.progress(90)
    status_text.text("✅ Processing complete!")
    
    # Store frames in session state
    if frames:
        st.session_state['extracted_frames'] = frames
    else:
        st.warning("No frames could be extracted.")
    
    progress_bar.progress(100)


def render_script_transformer():
    """Render the main Script Transformer UI."""
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            value=os.getenv("GOOGLE_API_KEY", ""),
            help="Your Google Gemini API key for script transformation"
        )
        
        # SEO Selection
        st.subheader("📊 SEO Settings")
        
        # Load SEO database
        try:
            seo_db = load_seo_database()
            titles = list_all_titles()
            
            seo_mode = st.radio(
                "SEO Mapping Mode",
                ["Auto-match from script", "Manual selection"]
            )
            
            selected_row_id = None
            if seo_mode == "Manual selection":
                # Create selectbox with titles
                title_options = [f"{id}. {title}" for id, title in titles]
                selected = st.selectbox("Select SEO Template", title_options)
                selected_row_id = int(selected.split(".")[0])
            
        except Exception as e:
            st.error(f"Error loading SEO database: {e}")
            selected_row_id = None
        
        # Visual Style Selection
        st.subheader("🎨 Visual Style")
        
        # Language Style Selection (NEW!)
        st.subheader("🗣️ Language Style")
        language_choice = st.radio(
            "Select Script Language",
            ["Nigerian Pidgin (Vibe)", "Urban Lagos Mix (English + Spice)", "Standard Nigerian English"],
            help="Choose the dialect/tone for the script conversion."
        )
        
        # Map choice to backend key
        lang_map = {
            "Nigerian Pidgin (Vibe)": "pidgin",
            "Urban Lagos Mix (English + Spice)": "mixed",
            "Standard Nigerian English": "english"
        }
        selected_language = lang_map[language_choice]
        
        # NEW: Visual Context Checkbox
        use_visual_context = False
        if 'visual_context' in st.session_state and st.session_state['visual_context']:
            st.info("✨ Extracted Style Available")
            
            # Handle help text for dict or string
            ctx = st.session_state['visual_context']
            if isinstance(ctx, dict):
                help_text = f"Style: {ctx.get('style', 'N/A')}\nLocation: {ctx.get('location', 'High-end Bedroom')}"
            else:
                help_text = str(ctx)
                
            use_visual_context = st.checkbox("Project Visual Style from YouTube", value=True, help=help_text)
        
        style_options = get_style_variations()
        selected_style = st.selectbox(
            "Color Grading",
            options=list(style_options.keys()),
            format_func=lambda x: style_options[x]
        )
        
        # Animation Style Selection (NEW!)
        from modules.visual_generator import get_animation_styles
        animation_options = get_animation_styles()
        selected_animation = st.selectbox(
            "Animation Style",
            options=list(animation_options.keys()),
            format_func=lambda x: animation_options[x],
            help="Choose between 2D Lofi or 3D CGI Pixar-style animation"
        )
        
        # Store selections in session state
        st.session_state['style'] = selected_style
        st.session_state['animation_style'] = selected_animation
        st.session_state['language_style'] = selected_language
        
        # Story Mode Selection (NEW!)
        st.subheader("📖 Story Mode")
        story_mode_choice = st.radio(
            "Select Story Mode",
            ["Single Location (13 scenes)", "Multi-Location (4 locations, 12-16 scenes)"],
            help="Single Location is the standard 90s format. Multi-Location spans across multiple settings."
        )
        selected_story_mode = "multi" if "Multi" in story_mode_choice else "single"
        st.session_state['story_mode'] = selected_story_mode
        
        # Motion Aesthetic Selection (NEW!)
        st.subheader("🎞️ Motion Settings")
        aesthetic_options = ["Maintain 2D aesthetic", "Maintain 3D aesthetic"]
        selected_aesthetic = st.radio(
            "Motion Aesthetic",
            options=aesthetic_options,
            index=0 if "2d" in selected_animation.lower() else 1,
            help="Determine if the motion prompts should preserve 2D or 3D visual logic."
        )
        st.session_state['aesthetic_choice'] = "2D" if "2D" in selected_aesthetic else "3D"
        
        # Cost estimate
        st.subheader("💰 Cost Estimate")
        st.success("**Google Gemini 2.5 Flash**  \nEstimated cost: **~$0.001 per transformation** 🎉  \n*Much cheaper than OpenAI!*")
    
    # Main content area
    tab1, tab2 = st.tabs(["🚀 Standard Transformer", "📺 YouTube Recreator"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input Script")
        st.markdown("Paste your original **Stoic Cole** script below:")
        
        # Sample script for testing
        sample_script = """Woman: I deserve a man who earns at least $100,000 because I am a prize.
Man: What do you bring to the table besides being a prize?
Woman: My presence is the value. I shouldn't have to explain myself.
Man: So let me get this straight. You want a six-figure earner, but your only contribution is existing. That's not a relationship, that's a subscription service."""
        
        original_script = st.text_area(
            "Original Script",
            height=300,
            placeholder="Paste Stoic Cole script here...",
            value=sample_script if st.checkbox("Load sample script") else ""
        )
        
        # Transform button
        transform_button = st.button("🚀 Nigerianize Script", type="primary", use_container_width=True)
    
    with col2:
        st.header("🎬 Output Preview")
        
        if transform_button:
            if not api_key:
                st.error("❌ Please provide a Google Gemini API key in the sidebar")
            elif not original_script.strip():
                st.error("❌ Please enter a script to transform")
            else:
                # Transform the script
                with st.spinner(f"🔄 Transforming script into {language_choice} ({selected_story_mode} mode)..."):
                    result = transform_script(original_script, language_style=selected_language, google_api_key=api_key, story_mode=selected_story_mode)
                
                if result["success"]:
                    st.success("✅ Transformation complete!")
                    
                    # Extract scenes and locations
                    if selected_story_mode == "multi":
                         locations = result.get("locations", [])
                         # Flatten scenes for processing but keep location context
                         scenes = []
                         for loc in locations:
                             for scene in loc.get("scenes", []):
                                 scene["location_description"] = loc.get("location_description")
                                 scenes.append(scene)
                    else:
                         scenes = result["scenes"]
                         locations = []
                    
                    # Extract setting description
                    setting_description = result.get("setting_description", "")
                    
                    # Validate structure
                    validation = validate_scene_structure(scenes) if selected_story_mode == "single" else {"valid": True, "issues": []}
                    if not validation["valid"]:
                        st.warning(f"⚠️ Structure issues: {', '.join(validation['issues'])}")
                    
                    # Get SEO data
                    if seo_mode == "Auto-match from script":
                        seo_data = match_content(original_script, seo_db)
                    else:
                        seo_data = get_seo_by_id(selected_row_id)
                    
                    # Override Title with Viral Hook if available
                    viral_title = result.get("viral_title")
                    if viral_title:
                        seo_data["title"] = viral_title
                        st.caption(f"🔥 Viral Title Generated: **{viral_title}**")
                    
                    # Pass visual context if enabled
                    if use_visual_context:
                        # Pass the full dict or string
                        visual_ctx = st.session_state.get('visual_context', {})
                        # If visual context has explicit location, it overrides script setting
                    else:
                        # If no external visual context, create one from the extracted setting!
                        if setting_description:
                             visual_ctx = {"style": "Cinematic 3D CGI Animation", "location": setting_description}
                        else:
                             visual_ctx = {}
                    
                    # Build complete output with selected styles
                    output = build_complete_output(
                        scenes, 
                        seo_data, 
                        st.session_state.get('style', 'default'),
                        st.session_state.get('animation_style', '2d_lofi'),
                        original_script,  # Pass original script for context extraction
                        visual_context=visual_ctx,
                        aesthetic_type=st.session_state.get('aesthetic_choice', '2D'),
                        story_mode=selected_story_mode,
                        locations=locations
                    )
                    
                    # Store in session state
                    st.session_state['output'] = output
                    st.session_state['scenes'] = scenes
                    
                else:
                    st.error(f"❌ Transformation failed: {result.get('error', 'Unknown error')}")
    
    # Display output if available
    if 'output' in st.session_state and 'scenes' in st.session_state:
        st.markdown("---")
        display_output(st.session_state['output'], st.session_state['scenes'])

    with tab2:
        st.header("📺 YouTube Story Recreator")
        st.markdown("Recreate stories from channels like **@MSA.official** with a Nigerian vibe.")
        
        yt_url = st.text_input("Enter YouTube URL (optional)", placeholder="https://www.youtube.com/watch?v=...", key="recreator_url")
        
        fetch_clicked = st.button("🔍 Fetch Auto-Transcript", use_container_width=True)
        
        # Handle fetching transcript separately
        if fetch_clicked:
            if not yt_url.strip():
                st.error("❌ Please enter a YouTube URL to fetch from")
            else:
                with st.spinner("🔍 Fetching transcript..."):
                    fetched_text = get_transcript(yt_url)
                    if fetched_text:
                        st.session_state['manual_transcript'] = fetched_text
                        st.success("✅ Transcript fetched! See below.")
                    else:
                        st.error("❌ Could not fetch transcript. Please paste it manually below.")
        
        # Manual Transcript Area
        transcript_input = st.text_area(
            "📝 Transcript to Recreate (Fetched or Pasted)", 
            value=st.session_state.get('manual_transcript', ''),
            placeholder="Paste your story transcript here...",
            height=300,
            key="transcript_area"
        )
        
        # Sync the text area back to session state for persistence
        st.session_state['manual_transcript'] = transcript_input
        
        recreate_button = st.button("🔥 Recreate Nigerian Story", type="primary", use_container_width=True, key="recreate_btn")
        
        if recreate_button:
            if not api_key:
                st.error("❌ Please provide a Google Gemini API key in the sidebar")
            elif not transcript_input.strip():
                st.error("❌ Please provide a transcript (fetch or paste)")
            else:
                with st.spinner("🔥 Reimagining story..."):
                    result = recreate_story(transcript_input, language_style=selected_language, google_api_key=api_key)
                    if result["success"]:
                        st.session_state['recreator_output'] = result["data"]
                        st.success("✅ Story Recreated Successfully!")
                    else:
                        st.error(f"❌ Recreation failed: {result.get('error')}")

        if 'recreator_output' in st.session_state:
            st.markdown("---")
            display_recreator_output(st.session_state['recreator_output'])


def build_complete_output(scenes: list, seo_data: dict, style_variation: str, animation_style: str = "2d_lofi", original_script: str = "", visual_context: str | dict = "", aesthetic_type: str = "2D", story_mode: str = "single", locations: list = None) -> dict:
    """
    Build the complete JSON output package with comprehensive metadata and POV.
    """
    
    # Extract story context from original script (look for key objects/topics)
    story_context = extract_story_context(original_script)
    
    # Extract outfit overrides for use in individual scenes
    outfit_overrides = story_context.get("outfit_changes", {})
    
    # Add POV context to SEO data
    enhanced_seo = add_pov_context_to_seo(seo_data, scenes)
    
    # Generate video-level metadata
    video_meta = generate_video_metadata(
        title=seo_data.get("title", ""),
        scenes=scenes,
        seo_data=enhanced_seo,
        animation_style=animation_style,
        language_style=st.session_state.get('language_style', 'pidgin')
    )
    
    output = {
        "video_metadata": video_meta,
        "seo_data": enhanced_seo,
        "scene_setup": generate_scene_setup_prompt(animation_style, story_context, visual_context),
        "props": generate_props(animation_style, story_context, visual_context, locations=locations),
        "scenes": []
    }
    
    # Process each scene
    parsed_scenes = parse_scenes(scenes, story_mode=story_mode)
    
    for scene in parsed_scenes:
        # Extract visual style string specifically for motion prompt if needed
        motion_ctx_str = ""
        if isinstance(visual_context, dict):
            motion_ctx_str = visual_context.get("style", "")
        elif isinstance(visual_context, str):
            motion_ctx_str = visual_context
        
        # Generate comprehensive metadata for this scene
        scene_metadata = generate_scene_metadata(
            scene=scene,
            seo_data=enhanced_seo,
            animation_style=animation_style,
            visual_context=visual_context
        )
            
        scene_output = {
            "scene_id": scene.get("scene_id"),
            "shot_type": scene.get("camera_angle", "Medium Shot"),
            "dialogue": scene.get("dialogue"),
            "pov": scene_metadata["pov"],  # NEW: POV field
            "metadata": scene_metadata["metadata"],  # NEW: Additional metadata
            "image_prompt": generate_image_prompt(scene, style_variation, animation_style, visual_context=visual_context, outfit_override=outfit_overrides),
            "condensed_prompt": generate_image_prompt_condensed(scene, style_variation, animation_style, visual_context=visual_context),
            "i2v_motion_prompt": generate_motion_prompt(scene, visual_context=motion_ctx_str, aesthetic_type=aesthetic_type),
            "sfx": suggest_sfx(scene)
        }
        output["scenes"].append(scene_output)
    
    return output


def extract_story_context(script: str) -> dict:
    """
    Extract the main focus/topic from the original script and determine
    how it affects character outfits.
    """
    if not script:
        return {"prop_description": "", "outfit_changes": {}}
    
    script_lower = script.lower()
    
    # Initialize with random outfits from the pools
    odogwu_outfit = random.choice(OUTFIT_POOLS["odogwu"])
    chioma_outfit = random.choice(OUTFIT_POOLS["antagonist"])
    
    context = {
        "prop_description": "",
        "outfit_changes": {
            "odogwu": odogwu_outfit,
            "chioma": chioma_outfit
        }
    }
    
    # Keyword overrides (Force specific outfits if the story demands it)
    if "jacket" in script_lower or "leather" in script_lower:
        context["outfit_changes"]["odogwu"] = "wearing a black leather jacket over a white t-shirt and dark jeans"
    
    elif "car" in script_lower or "vehicle" in script_lower or "drive" in script_lower:
        context["prop_description"] = "a luxury car visible in the driveway through the window"
    
    elif "shoes" in script_lower or "heels" in script_lower:
        context["prop_description"] = "designer shoes displayed prominently on a shelf"
    
    elif "watch" in script_lower:
        context["outfit_changes"]["odogwu"] = "wearing a smart-casual blazer with an expensive luxury watch prominently visible on his wrist"
    
    elif "bag" in script_lower or "purse" in script_lower or "handbag" in script_lower:
        context["prop_description"] = "a designer handbag prominently placed on a nearby table"
    
    # Dress story
    elif "dress" in script_lower and "wear" in script_lower:
        context["prop_description"] = "elegant dresses hanging in the wardrobe"
    
    # Jewelry story
    elif "jewelry" in script_lower or "diamond" in script_lower:
        context["prop_description"] = "expensive jewelry on display"
    
    return context


def display_output(output: dict, scenes: list):
    """
    Display the transformed output in the UI with comprehensive metadata.
    """
    
    st.header("📦 Complete Production Package")
    
    # Video Metadata Section (NEW!)
    if "video_metadata" in output:
        st.subheader("🎬 Video Metadata")
        vm = output["video_metadata"]
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Duration", f"{vm.get('duration_seconds')}s")
        with col2:
            st.metric("Scenes", vm.get('total_scenes'))
        with col3:
            st.metric("Style", vm.get('style', 'N/A'))
        with col4:
            st.metric("Language", vm.get('language', 'N/A'))
        
        # NEW: On-Screen POV Hook Suggestions
        if "onscreen_hooks" in vm:
            st.markdown("---")
            st.subheader("🎨 On-Screen POV Suggestions")
            st.info("💡 Copy these catchy titles to use as text overlays in your video editor:")
            
            hooks = vm["onscreen_hooks"]
            hook_cols = st.columns(len(hooks) if hooks else 1)
            for i, hook in enumerate(hooks):
                with hook_cols[i]:
                    st.code(hook, language="text")
        
        # NEW: Stoic Lesson Learned
        if "stoic_lesson" in vm:
            st.markdown("---")
            st.subheader("✨ Stoic Lesson Learned")
            st.success(f"**Takeaway:** {vm['stoic_lesson']}")
        
        with st.expander("📋 Full Video Metadata", expanded=False):
            st.json(vm)
    
    # SEO Section
    st.markdown("---")
    st.subheader("📊 SEO & Metadata")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Title", output["seo_data"]["title"])
    with col2:
        st.write("**Tags:**")
        st.write(", ".join(output["seo_data"]["tags"]))
    with col3:
        st.write("**Hashtags:**")
        st.write(" ".join(output["seo_data"]["hashtags"]))
    
    # NEW: POV Context display
    if "pov_context" in output["seo_data"]:
        st.info(f"**POV Context:** {output['seo_data']['pov_context']}")
    
    if "primary_character" in output["seo_data"]:
        st.success(f"**Primary Character:** {output['seo_data']['primary_character']}")
    
    # Scene Setup Section
    st.markdown("---")
    st.subheader("🎬 Scene Setup (Opening Shot)")
    with st.expander("📸 Establishing Shot - Scene Setup", expanded=True):
        st.markdown("**Scene Setup Prompt:**")
        st.text_area(
            "Scene setup establishing shot",
            output["scene_setup"],
            height=150,
            key="scene_setup_prompt"
        )
    
    # Props & References Section (NEW!)
    if "props" in output:
        st.markdown("---")
        st.subheader("🖼️ Character & Setting Props (References)")
        st.info("💡 Copy these prompts to your AI image generator to create consistent reference images for your characters and setting.")
        
        prop_cols = st.columns(3)
        props = output["props"]
        
        with prop_cols[0]:
            st.markdown("**👤 Hero (Odogwu)**")
            st.text_area("Hero Prop", props.get("hero", ""), height=150, key="hero_prop")
            
        with prop_cols[1]:
            st.markdown("**👤 Antagonist (Chioma)**")
            st.text_area("Antagonist Prop", props.get("antagonist", ""), height=150, key="antagonist_prop")
            
        with prop_cols[2]:
            st.markdown("**🏙️ Settings/Environments**")
            # If multi-mode, show all settings in a scrollable area or multiple boxes
            setting_props = {k: v for k, v in props.items() if k.startswith("setting")}
            if len(setting_props) > 1:
                for k, v in setting_props.items():
                    st.text_area(f"Setting {k.replace('setting_loc_', '')}", v, height=100, key=f"prop_{k}")
            else:
                st.text_area("Setting Prop", props.get("setting", ""), height=150, key="setting_prop")
    
    # Scenes Section
    st.markdown("---")
    st.subheader(f"🎬 Dialogue Scenes (1-{len(output['scenes'])})")
    
    # Check if we have locations to group by
    scenes_by_loc = {}
    if "location_context" in output["scenes"][0] and any(s.get("location_context") for s in output["scenes"]):
        for scene in output["scenes"]:
            loc = scene.get("location_context", "Default Location")
            if loc not in scenes_by_loc:
                scenes_by_loc[loc] = []
            scenes_by_loc[loc].append(scene)
    else:
        scenes_by_loc = {"The Story": output["scenes"]}

    for location_name, loc_scenes in scenes_by_loc.items():
        if len(scenes_by_loc) > 1:
            st.markdown(f"### 📍 Location: {location_name}")
            
        for scene in loc_scenes:
            with st.expander(f"Scene {scene.get('scene_id')} - {scene.get('shot_type')} ({scene.get('character')})"):
                st.markdown(f"**💬 Dialogue:** {scene.get('dialogue')}")
                
                if "pov" in scene:
                    st.markdown("**🎯 Point of View (POV) - For Editing:**")
                    st.caption(f"📷 **Camera:** {scene['pov'].get('camera_perspective', 'N/A')}")
                    st.caption(f"📖 **Focus:** {scene['pov'].get('narrative_focus', 'N/A')}")
                    st.caption(f"✂️ **Edit:** {scene['pov'].get('editing_notes', 'N/A')}")
                
                if "metadata" in scene:
                    st.markdown("**🔍 Metadata:**")
                    st.caption(f"👤 **Focal:** {scene['metadata'].get('focal_character', 'N/A')} | 🎭 **Tone:** {scene['metadata'].get('emotional_tone', 'N/A')}")
                    st.caption(f"🎯 **Purpose:** {scene['metadata'].get('scene_purpose', 'N/A')}")
                    st.caption(f"⏱️ **Timestamp:** {scene['metadata'].get('timestamp_seconds', '0')}s")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**🖼️ Image Prompt:**")
                    st.text_area(
                        f"Image prompt {scene.get('scene_id')}", 
                        scene.get('image_prompt'), 
                        height=100,
                        key=f"img_{scene.get('scene_id')}"
                    )
                
                with col2:
                    st.markdown("**🎞️ Motion Prompt:**")
                    st.text_area(
                        f"Motion prompt {scene.get('scene_id')}", 
                        scene.get('i2v_motion_prompt'), 
                        height=100,
                        key=f"motion_{scene.get('scene_id')}"
                    )
                
                st.markdown("**🔊 Sound Effects:**")
                for sfx in scene.get('sfx'):
                    st.write(f"- {sfx}")
    
    # Export Section
    st.markdown("---")
    st.subheader("💾 Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Custom JSON encoder for numpy/pandas types
        import numpy as np
        class NpEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return super(NpEncoder, self).default(obj)

        # JSON download
        try:
            json_str = json.dumps(output, indent=2, cls=NpEncoder)
            st.download_button(
                label="📥 Download Complete JSON (with Metadata)",
                data=json_str,
                file_name="naijastoic_output_with_metadata.json",
                mime="application/json"
            )
        except Exception as e:
            st.error(f"Error preparing export: {e}")
            st.code(json.dumps(output, indent=2, default=str), language="json")
    
    with col2:
        # Copy all motion prompts and SFX together
        combined_output = []
        for scene in output["scenes"]:
            # First line: shot_type, dialogue, motion prompt
            first_line = f"{scene.get('shot_type')}, {scene.get('dialogue')}, {scene.get('i2v_motion_prompt')}"
            # Following lines: SFX items
            scene_block = first_line + "\n" + "\n".join(scene.get('sfx'))
            combined_output.append(scene_block)
        
        # Join with blank line separator
        all_combined = "\n\n".join(combined_output)
        
        if st.button("📹🔊 Copy All Motion Prompts & SFX"):
            st.code(all_combined, language="text")
            st.info("👆 Copy the text above (scenes separated by blank lines)")
    
    # View full JSON button
    if st.button("📋 View Full JSON"):
        st.code(json_str, language="json")

    # NEW: Copy POV Editing Reference
    if st.button("📝 Copy POV Editing Reference"):
        pov_reference = []
        pov_reference.append(f"# POV Editing Reference for: {output['seo_data']['title']}\n")
        pov_reference.append(f"POV Context: {output['seo_data'].get('pov_context', 'N/A')}\n")
        
        for scene in output["scenes"]:
            pov_ref= f"\n## Scene {scene.get('scene_id')}: {scene.get('shot_type')}"
            pov_ref += f"\nDialogue: {scene.get('dialogue')}"
            if "pov" in scene:
                pov_ref += f"\n📷 Camera: {scene['pov'].get('camera_perspective')}"
                pov_ref += f"\n📖 Focus: {scene['pov'].get('narrative_focus')}"
                pov_ref += f"\n✂️ Edit: {scene['pov'].get('editing_notes')}"
            if "metadata" in scene:
                pov_ref += f"\n⏱️ Time: {scene['metadata'].get('timestamp_seconds')}s - {scene['metadata'].get('timestamp_seconds', 0) + 7}s"
            pov_reference.append(pov_ref)
        
        full_pov = "\n".join(pov_reference)
        st.code(full_pov, language="markdown")
        st.info("👆 Copy this POV reference for your editing session")

    # Combined Prompts Export Section
    st.markdown("---")
    st.subheader("📝 Bulk Prompt Copy Tools")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Copy All Prompts (Single Spaced)"):
            full_text = generate_bulk_prompts(output, double_spaced=False, condensed=False)
            st.code(full_text, language="text")
            st.info("👆 Copy the single-spaced prompts above")

    with col2:
        if st.button("📝 Copy All Prompts (Double Spaced)"):
            full_text = generate_bulk_prompts(output, double_spaced=True, condensed=False)
            st.code(full_text, language="text")
            st.info("👆 Copy the double-spaced prompts above")

    with col3:
        if st.button("📝 Copy All Prompts (Condensed)"):
            full_text = generate_bulk_prompts(output, double_spaced=False, condensed=True)
            st.code(full_text, language="text")
            st.info("👆 Copy the condensed prompts above")


def generate_bulk_prompts(output: dict, double_spaced: bool = False, condensed: bool = False) -> str:
    """
    Helper to generate bulk prompt string for all scenes.
    """
    scene_prompts = []
    
    for scene in output["scenes"]:
        # Clean up newlines in prompts
        img_prompt = scene.get('image_prompt', '').replace("\n", " ").strip()
        motion = scene.get('i2v_motion_prompt', '').replace("\n", " ").strip()
        sfx = " ".join(scene.get('sfx', []))
        
        # Get Camera POV
        camera_pov = "N/A"
        if "pov" in scene:
            camera_pov = scene['pov'].get('camera_perspective', 'N/A').replace("\n", " ").strip()
        
        # Identify character gender with strict word matching
        char_field = f" {scene.get('character', '').lower()} "
        scene_id = scene.get('scene_id', 1)
        
        # Priority 1: Direct character labels
        if "antagonist" in char_field or "chioma" in char_field:
            is_female = True
            is_male = False
        elif "protagonist" in char_field or "odogwu" in char_field:
            is_female = False
            is_male = True
        else:
            # Priority 2: Keyword scanning with word boundaries
            female_keywords = ["woman", "female", "she", "lady", "girl"]
            male_keywords = ["man", "male", "he", "guy", "boy"]
            
            # Using spaces as simple word boundaries for speed in Streamlit
            is_female = any(f" {k} " in char_field for k in female_keywords)
            # Ensure "he" doesn't catch "she"
            is_male = any(f" {k} " in char_field for k in male_keywords) and not is_female
            
            # Fallback based on scene structure
            if not is_female and not is_male:
                if 1 <= scene_id <= 6:
                    is_female = True
                    is_male = False
                else:
                    is_female = False
                    is_male = True
        
        dialogue = scene.get('dialogue', '').strip()
        voice_spec = ""
        gender_prefix = ""
        
        if dialogue:
            if is_female:
                voice_spec = FEMALE_VOICE_SPEC
                gender_prefix = "She says: "
            elif is_male:
                voice_spec = MALE_VOICE_SPEC
                gender_prefix = "He says: "
        
        if condensed:
            # Use action directly and condensed img prompt
            action = scene.get('action_description', '').replace("\n", " ").strip()
            img_prompt = scene.get('condensed_prompt', '').replace("\n", " ").strip()
            scene_block = f"{voice_spec} [{camera_pov}] {scene.get('shot_type')}, {gender_prefix}{dialogue}, {img_prompt}, Character action: {action}, {motion} {sfx}"
        else:
            # Full logic
            scene_block = f"{voice_spec} [{camera_pov}] {scene.get('shot_type')}, {gender_prefix}{dialogue}, {img_prompt}, {motion} {sfx}"
        
        scene_prompts.append(scene_block)
    
    # Add Final Lesson
    if "video_metadata" in output and "final_lesson" in output["video_metadata"]:
        lesson = output["video_metadata"]["final_lesson"]
        lesson_pov = "[Final close-up - Odogwu's perspective, steady, eye level from Chioma's position] Final close-up"
        lesson_block = f"{MALE_VOICE_SPEC} {lesson_pov}, He says: {lesson}"
        scene_prompts.append(lesson_block)
    
    join_str = "\n\n" if double_spaced else "\n"
    return join_str.join(scene_prompts)


def display_recreator_output(data: dict):
    """Refactored display logic for YouTube Recreator dual outputs."""
    long_data = data.get("long_video", {})
    short_data = data.get("short_video", {})
    
    st.subheader("📦 Generated Video Assets")
    
    long_tab, short_tab = st.tabs(["📽️ Long Video (Full Story)", "📱 Short Video (Highlights)"])
    
    with long_tab:
        st.markdown(f"### 🔥 Long: {long_data.get('title', 'Untitled')}")
        st.info(f"**POV:** {long_data.get('pov', 'N/A')}")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**📝 Description:**")
            st.text_area("Long Description", long_data.get("description", ""), height=150, key="long_desc")
        with col2:
            st.markdown("**🏷️ Tags:**")
            st.text_area("Long Tags", ", ".join(long_data.get("tags", [])), height=150, key="long_tags")
            
        # Display Scenes grouped by location for Long Video
        st.markdown("---")
        st.subheader("🎬 Long Video Scenes")
        
        visual_ctx = {"style": "Cinematic 3D CGI Animation", "location": "Nigeria"}
        global_scene_idx = 0
        
        for loc_idx, loc in enumerate(long_data.get("locations", [])):
            loc_desc = loc.get("location_description", "Unknown Location")
            st.markdown(f"#### 📍 Location {loc_idx + 1}: {loc_desc}")
            
            # NEW: Generate and display Location Setup Prompt
            # Pass loc_desc into setup prompt generation
            setup_prompt = generate_scene_setup_prompt(
                animation_style=st.session_state.get('animation_style', '3d_cgi'),
                visual_context={"location": loc_desc, "style": "Cinematic 3D CGI Animation"}
            )
            with st.expander(f"🖼️ Location {loc_idx + 1} SETUP PROMPT (Copy this first)"):
                st.text_area(f"Setup Prompt {loc_idx + 1}", setup_prompt, height=150, key=f"re_loc_setup_{loc_idx}")
            
            for scene in loc.get("scenes", []):
                # Generate prompts on the fly for Recreator mode
                scene["location_context"] = loc_desc
                img_prompt = generate_image_prompt(scene, animation_style=st.session_state.get('animation_style', '3d_cgi'), visual_context=visual_ctx)
                motion_prompt = generate_motion_prompt(scene, visual_context=st.session_state.get('style', 'default'), aesthetic_type=st.session_state.get('aesthetic_choice', '3D'))
                
                with st.expander(f"Scene {scene.get('scene_id')} - {scene.get('character')}"):
                    st.markdown(f"**💬 Dialogue:** {scene.get('dialogue')}")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.text_area("Image Prompt", img_prompt, height=100, key=f"re_long_img_{global_scene_idx}")
                    with c2:
                        st.text_area("Motion Prompt", motion_prompt, height=100, key=f"re_long_mot_{global_scene_idx}")
                
                global_scene_idx += 1

    with short_tab:
        st.markdown(f"### ⚡ Short: {short_data.get('title', 'Untitled')}")
        st.info(f"**POV:** {short_data.get('pov', 'N/A')}")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**📝 Description:**")
            st.text_area("Short Description", short_data.get("description", ""), height=100, key="short_desc")
        with col2:
            st.markdown("**🏷️ Tags:**")
            st.text_area("Short Tags", ", ".join(short_data.get("tags", [])), height=100, key="short_tags")
            
        st.markdown("---")
        st.subheader("🎬 Shorts Scenes")
        
        for i, scene in enumerate(short_data.get("scenes", [])):
            # Generate prompts on the fly
            img_prompt = generate_image_prompt(scene, animation_style=st.session_state.get('animation_style', '3d_cgi'), visual_context=visual_ctx)
            motion_prompt = generate_motion_prompt(scene, visual_context=st.session_state.get('style', 'default'), aesthetic_type=st.session_state.get('aesthetic_choice', '3D'))
            
            with st.expander(f"Short Scene {scene.get('scene_id')}"):
                st.markdown(f"**💬 Dialogue:** {scene.get('dialogue')}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.text_area("Image Prompt", img_prompt, height=100, key=f"re_short_img_{i}")
                with c2:
                    st.text_area("Motion Prompt", motion_prompt, height=100, key=f"re_short_mot_{i}")


if __name__ == "__main__":
    main()
