"""
Module G: Metadata Manager
Generates comprehensive metadata including POV fields for all script-generated assets.
"""

from datetime import datetime
from typing import Optional, Dict, List


def generate_scene_metadata(
    scene: dict,
    seo_data: dict,
    animation_style: str = "3d_cgi",
    visual_context: Optional[dict] = None
) -> dict:
    """
    Generate comprehensive metadata for a single scene including POV.
    
    Args:
        scene: Scene dictionary with dialogue, character, phase info
        seo_data: SEO data for context
        animation_style: Animation style being used
        visual_context: Optional visual context from extracted frames
    
    Returns:
        Dictionary with comprehensive metadata including POV
    """
    
    scene_id = scene.get("scene_id", 1)
    character = scene.get("character", "protagonist")
    phase = scene.get("phase", "Unknown")
    camera_angle = scene.get("camera_angle", "Medium Shot")
    
    # Generate POV components
    pov = {
        "camera_perspective": generate_camera_pov(character, camera_angle, scene_id),
        "narrative_focus": generate_narrative_pov(character, phase, scene_id),
        "editing_notes": generate_editing_notes(phase, character, scene_id)
    }
    
    # Additional metadata
    metadata = {
        "focal_character": get_character_name(character),
        "emotional_tone": get_emotional_tone(phase, character),
        "scene_purpose": f"{phase} - {get_phase_purpose(phase)}",
        "timestamp_seconds": (scene_id - 1) * 7,  # 7 seconds per scene
        "duration_seconds": 7
    }
    
    return {
        "pov": pov,
        "metadata": metadata
    }


def generate_camera_pov(character: str, camera_angle: str, scene_id: int) -> str:
    """
    Generate camera POV description.
    
    Args:
        character: Character speaking (protagonist/antagonist/both)
        camera_angle: Camera angle from scene
        scene_id: Scene number
    
    Returns:
        Camera perspective description
    """
    
    if character == "protagonist":
        focal = "Odogwu"
        level = "steady, eye level from Chioma's position"
    elif character == "antagonist":
        focal = "Chioma"
        level = "steady, eye level from Odogwu's position"
    else:  # both
        focal = "Both characters"
        level = "neutral observer, slightly elevated"
    
    return f"{camera_angle} - {focal}'s perspective, {level}"


def generate_narrative_pov(character: str, phase: str, scene_id: int) -> str:
    """
    Generate narrative POV description.
    
    Args:
        character: Character speaking
        phase: Story phase (Hook, Build, Pivot, Dunk)
        scene_id: Scene number
    
    Returns:
        Narrative focus description
    """
    
    narrative_map = {
        "Hook": {
            "protagonist": "Observing antagonist's demands calmly",
            "antagonist": "Making entitled demands/establishing conflict",
            "both": "Initial confrontation - setting up the argument"
        },
        "Build": {
            "protagonist": "Listening and processing the argument",
            "antagonist": "Defending position with passion",
            "both": "Argument intensifying - both sides presenting"
        },
        "Pivot": {
            "protagonist": "Asking the critical question - shift begins",
            "antagonist": "Reacting to unexpected question",
            "both": "Turning point - logic meets emotion"
        },
        "Dunk": {
            "protagonist": "Delivering logical breakdown/final point",
            "antagonist": "Realizing the logical trap",
            "both": "Resolution - protagonist's logic wins"
        }
    }
    
    default = f"{get_character_name(character)} in {phase} phase"
    return narrative_map.get(phase, {}).get(character, default)


def generate_editing_notes(phase: str, character: str, scene_id: int) -> str:
    """
    Generate editing notes for video production.
    
    Args:
        phase: Story phase
        character: Character speaking
        scene_id: Scene number
    
    Returns:
        Editing guidance notes
    """
    
    if phase == "Hook":
        if character == "antagonist":
            return "Emphasize entitled expression, wild gestures. Build initial conflict. Consider light VFX on key words."
        else:
            return "Show calm composure contrast. Subtle reactions only. Establish protagonist's stoic nature."
    
    elif phase == "Build":
        if character == "antagonist":
            return "Increase intensity. Passionate gestures. Show defensive body language building."
        else:
            return "Maintain calm demeanor. Slight eyebrow raises or head tilts. Contrast against antagonist's energy."
    
    elif phase == "Pivot":
        if character == "protagonist":
            return "KEY MOMENT: Emphasize the question. Slight pause before delivery. This is the trap being set."
        elif character == "antagonist":
            return "Show confusion/surprise. Defensive posture shift. The trap is sprung."
        else:
            return "Tension peak. Both characters engaged. Show the shift in power dynamic."
    
    elif phase == "Dunk":
        if character == "protagonist":
            if scene_id >= 12:
                return "PAYOFF: Strong confident delivery. Knowing smile. Final mic drop moment. Consider SFX emphasis."
            else:
                return "Logical explanation. Clear, measured points. Show intelligence and confidence building."
        else:
            return "Show defeat. Deflated posture. Speechless reaction. Argument crumbling."
    
    return f"Standard {phase} phase execution"


def get_character_name(character: str) -> str:
    """Get proper character name."""
    map_names = {
        "protagonist": "Odogwu",
        "antagonist": "Chioma",
        "both": "Both Characters"
    }
    return map_names.get(character, character)


def get_emotional_tone(phase: str, character: str) -> str:
    """Get emotional tone for scene."""
    
    tone_map = {
        "Hook": {
            "protagonist": "Calm, observant",
            "antagonist": "Entitled, demanding",
            "both": "Tense confrontation"
        },
        "Build": {
            "protagonist": "Composed, analytical",
            "antagonist": "Passionate, defensive",
            "both": "Rising conflict"
        },
        "Pivot": {
            "protagonist": "Strategic, questioning",
            "antagonist": "Confused, caught off-guard",
            "both": "Shifting dynamics"
        },
        "Dunk": {
            "protagonist": "Confident, logical",
            "antagonist": "Deflated, speechless",
            "both": "Resolution, victory"
        }
    }
    
    return tone_map.get(phase, {}).get(character, "Neutral")


def get_phase_purpose(phase: str) -> str:
    """Get the purpose of each phase."""
    purposes = {
        "Hook": "Establish conflict and grab attention",
        "Build": "Develop argument and raise tension",
        "Pivot": "Turn the tables with logic",
        "Dunk": "Deliver the logical knockout"
    }
    return purposes.get(phase, "Story progression")


def generate_onscreen_hooks(seo_data: dict, scenes: List[dict]) -> List[str]:
    """
    Generate catchy on-screen POV hooks for video overlays.
    (e.g., "POV: Toxic Council", "POV: The Entitled One")
    """
    
    title = seo_data.get("title", "").lower()
    script_text = " ".join([s.get("dialogue", "") for s in scenes]).lower()
    
    hooks = []
    
    # Analyze theme
    is_toxic = any(word in script_text for word in ["pay", "bills", "deserve", "entitled", "prize"])
    is_relationship = any(word in script_text for word in ["man", "woman", "date", "marriage", "breakfast"])
    is_logic = any(word in script_text for word in ["logic", "sense", "why", "how"])
    
    # Base hooks
    raw_title = seo_data.get("title", "Naija Stoic Logic")
    hooks.append(f"POV: {raw_title}")
    
    if is_toxic:
        hooks.append("POV: The Toxic Council")
        hooks.append("POV: Entitlement Mentality")
        hooks.append("POV: Slay Queen Logic")
    
    if is_relationship:
        hooks.append("POV: Modern Relationships")
        hooks.append("POV: High Value Standards")
        hooks.append("POV: Breakfast Served Hot")
    
    if is_logic:
        hooks.append("POV: Logic Applied")
        hooks.append("POV: The Logic Trap")
        hooks.append("POV: No Gree For Anybody")

    # Filter/Clean
    unique_hooks = []
    for h in hooks:
        if h not in unique_hooks:
            unique_hooks.append(h)
            
    return unique_hooks[:5] # Return top 5


def generate_final_lesson(seo_data: dict, scenes: List[dict]) -> str:
    """
    Generate a punchy, entertaining, and educational lesson based on the script.
    """
    script_text = " ".join([s.get("dialogue", "") for s in scenes]).lower()
    
    # Analyze theme for specific lessons
    if any(word in script_text for word in ["pay", "bills", "deserve", "entitled"]):
        return "Your value comes from your character, not your entitlement. No gree for sapa mentality."
    elif any(word in script_text for word in ["prize", "worth", "standards"]):
        return "A true prize doesn't need to announce its price. Character over packaging."
    elif any(word in script_text for word in ["marriage", "man", "woman", "date"]):
        return "Relationships na partnership, no be entitlement workshop. Stay logical."
    elif any(word in script_text for word in ["why", "how", "logic"]):
        return "Question everything with logic. When emotions rise, wisdom must lead."
    
    return "Protect your peace and use your logic. No gree for anybody."


def generate_video_metadata(
    title: str,
    scenes: List[dict],
    seo_data: dict,
    animation_style: str = "3d_cgi",
    language_style: str = "pidgin"
) -> dict:
    """
    Generate comprehensive metadata for the entire video.
    
    Args:
        title: Video title
        scenes: List of all scenes
        seo_data: SEO data
        animation_style: Animation style used
        language_style: Language style used
    
    Returns:
        Complete video metadata
    """
    
    return {
        "title": title,
        "created_at": datetime.now().isoformat(),
        "total_scenes": len(scenes),
        "duration_seconds": len(scenes) * 7,
        "style": get_style_name(animation_style),
        "language": get_language_name(language_style),
        "onscreen_hooks": generate_onscreen_hooks(seo_data, scenes),
        "final_lesson": generate_final_lesson(seo_data, scenes), # NEW: Catchy Lesson
        "format": "vertical 9:16",
        "target_platform": "TikTok, Instagram Reels, YouTube Shorts",
        "content_type": "Nigerian Stoic Logic - Relationship Commentary"
    }


def get_style_name(animation_style: str) -> str:
    """Get readable style name."""
    styles = {
        "2d_lofi": "2D Lofi Anime",
        "3d_cgi": "3D CGI Pixar Style"
    }
    return styles.get(animation_style, animation_style)


def get_language_name(language_style: str) -> str:
    """Get readable language name."""
    languages = {
        "pidgin": "Nigerian Pidgin English",
        "mixed": "Urban Lagos Mix (English + Pidgin)",
        "english": "Standard Nigerian English"
    }
    return languages.get(language_style, language_style)


def add_pov_context_to_seo(seo_data: dict, scenes: List[dict]) -> dict:
    """
    Add POV context to SEO data based on scenes.
    
    Args:
        seo_data: Existing SEO data
        scenes: List of scenes
    
    Returns:
        Enhanced SEO data with POV context
    """
    
    # Count protagonist vs antagonist scenes
    protag_count = sum(1 for s in scenes if s.get("character") == "protagonist")
    antag_count = sum(1 for s in scenes if s.get("character") == "antagonist")
    
    # Determine overall POV context
    if protag_count > antag_count:
        pov_context = "Male protagonist defending against entitled demands with stoic logic"
    elif antag_count > protag_count:
        pov_context = "Female antagonist making demands, protagonist responds with logic"
    else:
        pov_context = "Balanced dialogue showing logic vs emotion conflict"
    
    # Add to SEO data
    enhanced_seo = seo_data.copy()
    enhanced_seo["pov_context"] = pov_context
    enhanced_seo["primary_character"] = "Odogwu (Protagonist)" if protag_count >= antag_count else "Chioma (Antagonist)"
    enhanced_seo["narrative_style"] = "Stoic Logic - No Gree For Anybody"
    
    return enhanced_seo


if __name__ == "__main__":
    # Test metadata generation
    test_scene = {
        "scene_id": 7,
        "phase": "Pivot",
        "character": "protagonist",
        "camera_angle": "Close-up",
        "dialogue": "So wetin you dey bring to the table?"
    }
    
    test_seo = {
        "title": "Test Video",
        "tags": ["stoicism", "relationships"],
        "hashtags": ["#nogreeforanybody"]
    }
    
    metadata = generate_scene_metadata(test_scene, test_seo)
    
    print("✅ Metadata Manager Test\n")
    print(f"POV - Camera: {metadata['pov']['camera_perspective']}")
    print(f"POV - Narrative: {metadata['pov']['narrative_focus']}")
    print(f"POV - Editing: {metadata['pov']['editing_notes']}\n")
    print(f"Focal Character: {metadata['metadata']['focal_character']}")
    print(f"Emotional Tone: {metadata['metadata']['emotional_tone']}")
