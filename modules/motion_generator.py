"""
Module D: Image-to-Video (I2V) Motion Prompts
Generates motion prompts for Runway Gen-3, Luma Dream Machine, or similar I2V tools.
"""


def generate_motion_prompt(scene: dict, visual_context: str = "", aesthetic_type: str = "2D") -> str:
    """
    Generate I2V motion prompt for a scene.
    Now supports visual_context to influence camera movement style.
    Example: "Cinematic, slow pan right, focus on Odogwu"
    
    Args:
        scene: Scene object with scene_id, shot_type, character, dialogue
        visual_context: Optional string description of visual style/camera vibes
        aesthetic_type: "2D" or "3D"
    
    Returns:
        Motion prompt string for I2V AI tools
    """
    
    scene_id = scene.get("scene_id", 1)
    shot_type = scene.get("shot_type", "Close-up")
    character = scene.get("character", "protagonist")
    
    # Base motion requirements (dynamic based on aesthetic)
    aesthetic_note = "Maintain 2D aesthetic" if "2D" in aesthetic_type.upper() else "Maintain 3D aesthetic"
    base_motion = f"Stay on one spot at all times. Subtle movements only. {aesthetic_note}."
    
    # === AUTO CAMERA ANGLE ROTATION ===
    # Cycles through 4 distinct camera angles based on scene position
    # This makes the same image feel like 4 different shots
    scene_position = ((scene_id - 1) % 4) + 1
    camera_cycles = {
        1: "Very slow subtle push-in toward the left side of frame, focusing on the speaking character.",
        2: "Very slow subtle push-in toward the right side of frame, focusing on the reacting character.",
        3: "Locked-off wide static shot. No camera movement. Both characters fully visible.",
        4: "Slow subtle pan right across the frame, then settle. Cinematic drift."
    }
    camera_movement = camera_cycles.get(scene_position, "No camera movement.")
    
    # Character-specific motions - Prioritize extracted action
    action_desc = scene.get("action_description", "")
    if action_desc:
        # Transform action description into motion prompt style
        char_motion = f"Character action: {action_desc}. Facial expressions matching dialogue emotion."
    else:
        # Fallback to legacy static dictionary
        char_motion = get_character_motion(scene_id, character)
    
    # Background ambient motion
    bg_motion = get_background_motion(shot_type)
    
    # Integrate visual context if it contains relevant camera keywords
    extra_instruction = ""
    if visual_context:
        v_ctx = visual_context.lower()
        if "handheld" in v_ctx:
            extra_instruction = " Handheld camera shake style."
        elif "steady" in v_ctx or "smooth" in v_ctx:
            extra_instruction = " Ultra smooth sleek stabilization."
        elif "dynamic" in v_ctx:
            extra_instruction = " Dynamic active camera motion."
        elif "static" in v_ctx:
            extra_instruction = " Tripod static shot."
            
    # Construct full prompt
    motion_prompt = f"{char_motion} {bg_motion} {camera_movement}{extra_instruction} {base_motion}"
    
    return motion_prompt


def get_character_motion(scene_id: int, character: str) -> str:
    """
    Get character motion based on scene and role.
    
    Args:
        scene_id: Scene number (1-3)
        character: 'protagonist' or 'antagonist'
    
    Returns:
        Character motion description
    """
    
    motions = {
        1: {
            "antagonist": "Character talking animatedly, hand gestures, head movements, facial expressions changing, blinking frequently.",
            "protagonist": "Character listening calmly, subtle blinking, minimal head movement, coffee steam rising from cup in foreground."
        },
        2: {
            "protagonist": "Character speaking calmly, lips syncing to dialogue, slight eyebrow raise, minimal hand gesture, confident gaze.",
            "antagonist": "Character reacting with surprise, defensive body language, blinking, slight head tilt."
        },
        3: {
            "protagonist": "Character delivering final point, calm confident expression, slight lean forward, knowing smile forming, steady eye contact.",
            "antagonist": "Character looking increasingly frustrated or speechless, looking away briefly, resigned expression."
        }
    }
    
    return motions.get(scene_id, {}).get(character, "Subtle blinking and breathing.")


def get_background_motion(shot_type: str) -> str:
    """
    Get ambient background motion based on shot type.
    
    Args:
        shot_type: The shot type (Close-up, Wide Shot, etc.)
    
    Returns:
        Background motion description
    """
    
    if "Close-up" in shot_type:
        return "Background city lights flickering subtly through window, soft bokeh lights twinkling."
    elif "Wide" in shot_type:
        return "City skyline visible with twinkling lights, subtle curtain movement from AC, ambient room lighting pulsing gently."
    else:
        return "Background windows showing Lagos night skyline with subtle light changes, ambient purple glow."


def add_lip_sync_note(motion_prompt: str, has_dialogue: bool = True) -> str:
    """
    Add lip sync instructions if scene has dialogue.
    
    Args:
        motion_prompt: Base motion prompt
        has_dialogue: Whether scene has spoken dialogue
    
    Returns:
        Enhanced motion prompt with lip sync notes
    """
    
    if has_dialogue:
        return f"{motion_prompt} Lips syncing accurately to dialogue audio track."
    else:
        return f"{motion_prompt} Character silent, closed mouth."


def get_motion_duration_guide(scene_duration: str) -> dict:
    """
    Get technical specs for motion duration.
    
    Args:
        scene_duration: Duration string like "0-10s"
    
    Returns:
        dict with technical motion parameters
    """
    
    # Parse duration
    if "-" in scene_duration:
        end_time = scene_duration.split("-")[1].replace("s", "")
        duration = int(end_time)
    else:
        duration = 10  # default
    
    return {
        "total_duration": f"{duration}s",
        "motion_intensity": "subtle" if duration < 15 else "moderate",
        "recommended_fps": 24,
        "loop_seamless": False,
        "motion_type": "organic"
    }


def generate_runway_specific_prompt(scene: dict) -> dict:
    """
    Generate Runway Gen-3 specific format.
    
    Args:
        scene: Scene object
    
    Returns:
        dict with Runway-formatted parameters
    """
    
    base_motion = generate_motion_prompt(scene)
    
    return {
        "prompt": base_motion,
        "duration": 10,  # Runway default
        "motion_bucket_id": 127,  # Low motion for subtle animations
        "style": "2D Animation",
        "aspect_ratio": "9:16"  # Vertical for TikTok/Reels
    }


def generate_luma_specific_prompt(scene: dict) -> dict:
    """
    Generate Luma Dream Machine specific format.
    
    Args:
        scene: Scene object
    
    Returns:
        dict with Luma-formatted parameters
    """
    
    base_motion = generate_motion_prompt(scene)
    
    return {
        "prompt": base_motion,
        "keyframes": {
            "frame_0": "Starting position",
            "frame_end": "Ending position with minimal change"
        },
        "loop": False,
        "aspect_ratio": "9:16"
    }


if __name__ == "__main__":
    # Test motion prompt generation
    test_scenes = [
        {
            "scene_id": 1,
            "shot_type": "Close-up (Antagonist)",
            "character": "antagonist",
            "duration": "0-10s"
        },
        {
            "scene_id": 2,
            "shot_type": "Wide Shot (Both Characters)",
            "character": "protagonist",
            "duration": "10-30s"
        },
        {
            "scene_id": 3,
            "shot_type": "Close-up (Protagonist)",
            "character": "protagonist",
            "duration": "30-60s"
        }
    ]
    
    # Mock visual context for testing
    mock_context = "Handheld camera feel with moody lighting"
    
    print("✅ Generated Motion Prompts (with Context integration):\n")
    for scene in test_scenes:
        prompt = generate_motion_prompt(scene, visual_context=mock_context)
        print(f"Scene {scene['scene_id']}:")
        print(f"{prompt}\n")
        
        # Show Runway format
        runway = generate_runway_specific_prompt(scene)
        print(f"Runway Format: {runway}\n")
