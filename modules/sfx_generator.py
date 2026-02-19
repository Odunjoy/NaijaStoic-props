"""
Module E: Sound Effects (SFX) & Audio
Generates SFX suggestions based on script beats and scene timing.
"""


def suggest_sfx(scene: dict) -> list:
    """
    Suggest sound effects for a scene based on its beat and content.
    
    Args:
        scene: Scene object with scene_id, character, dialogue
    
    Returns:
        List of SFX suggestion strings
    """
    
    scene_id = scene.get("scene_id", 1)
    character = scene.get("character", "protagonist")
    
    # Get base SFX for scene type
    base_sfx = get_scene_sfx(scene_id, character)
    
    # Add ambient background
    ambient = get_ambient_sfx()
    
    # Combine
    return base_sfx + ambient


def get_scene_sfx(scene_id: int, character: str) -> list:
    """
    Get primary SFX for scene based on the viral formula beat.
    
    Args:
        scene_id: Scene number (1-3)
        character: 'protagonist' or 'antagonist'
    
    Returns:
        List of primary SFX
    """
    
    sfx_library = {
        1: {
            "intro": [
                "Low-tempo slowed + reverb Afrobeats instrumental (Burna Boy style)",
                "Muffled city noise in background",
                "Soft lofi hip-hop beat starting"
            ]
        },
        2: {
            "pivot": [
                "Record scratch sound effect",
                "Brief silence for dramatic pause (1-2s)",
                "Tension-building string note",
                "Subtle heartbeat sound emerging"
            ]
        },
        3: {
            "dunk": [
                "Deep bass thud on key logic points",
                "Heartbeat intensifying",
                "Mic drop sound effect at end",
                "Cinematic boom/impact sound"
            ]
        }
    }
    
    # Map scene to beat
    if scene_id == 1:
        return sfx_library[1]["intro"]
    elif scene_id == 2:
        return sfx_library[2]["pivot"]
    else:
        return sfx_library[3]["dunk"]


def get_ambient_sfx() -> list:
    """
    Get ambient background SFX that run throughout.
    
    Returns:
        List of ambient SFX
    """
    
    return [
        "Lagos city ambiance (distant traffic, city hum)",
        "Wind chime or subtle bell tones",
        "Coffee shop ambiance (very subtle)",
        "Light rain against window (optional for mood)"
    ]


def get_music_prompt() -> dict:
    """
    Get music generation prompt for background score.
    
    Returns:
        dict with music prompts for different sections
    """
    
    return {
        "intro": {
            "prompt": "Slowed + reverb Afrobeats instrumental, lofi hip-hop vibe, purple aesthetic, 80 BPM, Burna Boy style, chill and moody",
            "duration": "10s",
            "fade": "fade_in"
        },
        "pivot": {
            "prompt": "Tension-building minimalist beat, slowed tempo, suspenseful strings, dramatic pause moment",
            "duration": "20s",
            "fade": "crossfade"
        },
        "dunk": {
            "prompt": "Epic bass drop, cinematic boom, triumphant undertone, Afrobeats percussion, powerful finish",
            "duration": "30s",
            "fade": "fade_out"
        }
    }


def get_timing_markers(scenes: list) -> dict:
    """
    Calculate exact timing for SFX placement.
    
    Args:
        scenes: List of scene objects with durations
    
    Returns:
        dict with timestamp markers for key SFX moments
    """
    
    markers = {
        "intro_music_start": "0:00",
        "hook_dialogue": "0:02",
        "record_scratch": "0:10",
        "pivot_question": "0:12",
        "tension_build": "0:20",
        "first_bass_thud": "0:32",
        "second_bass_thud": "0:45",
        "mic_drop": "0:58",
        "outro_fade": "1:00"
    }
    
    return markers


def generate_sfx_manifest(scenes: list) -> dict:
    """
    Generate a complete SFX manifest for the entire video.
    
    Args:
        scenes: List of all scene objects
    
    Returns:
        Complete SFX manifest with timing and layering
    """
    
    manifest = {
        "music_tracks": get_music_prompt(),
        "ambient_layer": get_ambient_sfx(),
        "scene_sfx": [],
        "timing_markers": get_timing_markers(scenes)
    }
    
    # Add SFX for each scene
    for scene in scenes:
        scene_sfx = {
            "scene_id": scene.get("scene_id"),
            "sfx_list": suggest_sfx(scene),
            "volume": get_volume_level(scene.get("scene_id")),
            "layering": get_layer_priority(scene.get("scene_id"))
        }
        manifest["scene_sfx"].append(scene_sfx)
    
    return manifest


def get_volume_level(scene_id: int) -> dict:
    """
    Get recommended volume levels for scene.
    
    Args:
        scene_id: Scene number
    
    Returns:
        dict with volume recommendations
    """
    
    levels = {
        1: {"music": 0.6, "dialogue": 1.0, "sfx": 0.4, "ambient": 0.3},
        2: {"music": 0.3, "dialogue": 1.0, "sfx": 0.7, "ambient": 0.2},
        3: {"music": 0.8, "dialogue": 1.0, "sfx": 0.9, "ambient": 0.3}
    }
    
    return levels.get(scene_id, levels[1])


def get_layer_priority(scene_id: int) -> list:
    """
    Get audio layer priority (what should be most prominent).
    
    Args:
        scene_id: Scene number
    
    Returns:
        List of layers in priority order
    """
    
    priorities = {
        1: ["dialogue", "music", "ambient", "sfx"],
        2: ["dialogue", "sfx", "ambient", "music"],
        3: ["dialogue", "sfx", "music", "ambient"]
    }
    
    return priorities.get(scene_id, priorities[1])


if __name__ == "__main__":
    # Test SFX generation
    test_scenes = [
        {"scene_id": 1, "character": "antagonist"},
        {"scene_id": 2, "character": "protagonist"},
        {"scene_id": 3, "character": "protagonist"}
    ]
    
    print("✅ Generated SFX Manifest:\n")
    manifest = generate_sfx_manifest(test_scenes)
    
    print("🎵 Music Tracks:")
    for section, details in manifest["music_tracks"].items():
        print(f"  {section}: {details['prompt']}")
    
    print("\n🔊 Scene SFX:")
    for scene_sfx in manifest["scene_sfx"]:
        print(f"\n  Scene {scene_sfx['scene_id']}:")
        for sfx in scene_sfx["sfx_list"]:
            print(f"    - {sfx}")
