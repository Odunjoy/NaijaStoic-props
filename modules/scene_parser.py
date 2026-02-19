"""
Module B: Scene & Dialogue Parsing
Breaks transformed scripts into 13 distinct viral scenes for 90-second format.
"""


def parse_scenes(transformed_dialogue: list, story_mode: str = "single") -> list:
    """
    Take raw transformed scenes and add metadata for shot types and timing.
    Supports both single and multi-location story modes.
    """
    
    # 13-scene template for single-location 90-second format
    single_templates = {
        1: {"shot_type": "Close-up (Chioma)", "camera_angle": "Close-up", "phase": "Hook", "character": "antagonist", "duration": "0-7s"},
        2: {"shot_type": "Medium shot (Chioma)", "camera_angle": "Medium", "phase": "Hook", "character": "antagonist", "duration": "7-14s"},
        3: {"shot_type": "Wide shot (Chioma)", "camera_angle": "Wide", "phase": "Hook", "character": "antagonist", "duration": "14-21s"},
        4: {"shot_type": "Over-shoulder (Chioma)", "camera_angle": "Over-shoulder", "phase": "Build", "character": "antagonist", "duration": "21-28s"},
        5: {"shot_type": "Close-up (Chioma)", "camera_angle": "Close-up", "phase": "Build", "character": "antagonist", "duration": "28-35s"},
        6: {"shot_type": "Medium shot (Odogwu)", "camera_angle": "Medium", "phase": "Build", "character": "protagonist", "duration": "35-42s"},
        7: {"shot_type": "Close-up (Odogwu)", "camera_angle": "Close-up", "phase": "Pivot", "character": "protagonist", "duration": "42-49s"},
        8: {"shot_type": "Two-shot", "camera_angle": "Two-shot", "phase": "Pivot", "character": "both", "duration": "49-56s"},
        9: {"shot_type": "Medium shot (Chioma)", "camera_angle": "Medium", "phase": "Pivot", "character": "antagonist", "duration": "56-63s"},
        10: {"shot_type": "Close-up (Odogwu)", "camera_angle": "Close-up", "phase": "Dunk", "character": "protagonist", "duration": "63-70s"},
        11: {"shot_type": "Medium shot (Odogwu)", "camera_angle": "Medium", "phase": "Dunk", "character": "protagonist", "duration": "70-77s"},
        12: {"shot_type": "Wide shot (Odogwu & Chioma)", "camera_angle": "Wide", "phase": "Dunk", "character": "protagonist", "duration": "77-84s"},
        13: {"shot_type": "Final Close-up (Odogwu)", "camera_angle": "Close-up", "phase": "Dunk", "character": "protagonist", "duration": "84-91s"}
    }
    
    # Simple dynamic template fallback for multi-mode or unexpected counts
    def get_dynamic_template(scene_id, total):
        if scene_id == 1:
            return {"shot_type": "Close-up", "camera_angle": "Close-up", "phase": "Hook", "character": "antagonist"}
        if scene_id == total:
            return {"shot_type": "Final Close-up", "camera_angle": "Close-up", "phase": "Dunk", "character": "protagonist"}
        
        # Cycle through some basic angles
        angles = ["Medium", "Wide", "Over-shoulder", "Close-up"]
        phases = ["Hook", "Build", "Pivot", "Dunk"]
        
        idx = (scene_id - 1) % len(angles)
        phase_idx = min(3, (scene_id - 1) // (max(1, total // 4)))
        
        return {
            "shot_type": f"{angles[idx]} shot",
            "camera_angle": angles[idx],
            "phase": phases[phase_idx],
            "character": "protagonist" if scene_id > total // 2 else "antagonist"
        }

    enriched_scenes = []
    total_scenes = len(transformed_dialogue)
    
    for i, scene in enumerate(transformed_dialogue):
        scene_id = scene.get("scene_id", i + 1)
        
        if story_mode == "single" and scene_id in single_templates:
            template = single_templates[scene_id]
        else:
            template = get_dynamic_template(scene_id, total_scenes)
            
        enriched_scene = {
            "scene_id": scene_id,
            "shot_type": scene.get("shot_type") or template["shot_type"],
            "camera_angle": scene.get("camera_angle") or template["camera_angle"],
            "description": scene.get("description") or f"Scene {scene_id}",
            "duration": f"{i*7}-{(i+1)*7}s", # Default 7s per scene
            "dialogue": scene.get("dialogue", ""),
            "character": scene.get("character") or template["character"],
            "phase": scene.get("phase") or template["phase"],
            "action_description": scene.get("action_description", ""),
            "location_context": scene.get("location_description", "") # Preserve if coming from multi-mode
        }
        
        enriched_scenes.append(enriched_scene)
    
    return enriched_scenes


def validate_scene_structure(scenes: list) -> dict:
    """
    Validate that the scene structure follows the Hook-Build-Pivot-Dunk formula.
    
    Args:
        scenes: List of scene objects
    
    Returns:
        dict with validation results
    """
    
    issues = []
    
    # Check we have exactly 13 scenes
    if len(scenes) != 13:
        issues.append(f"Expected 13 scenes, got {len(scenes)}")
    
    # Check scene IDs are sequential
    expected_ids = list(range(1, 14))
    actual_ids = [scene.get("scene_id") for scene in scenes]
    
    if actual_ids != expected_ids:
        issues.append(f"Scene IDs not sequential. Expected {expected_ids}, got {actual_ids}")
    
    # Check all scenes have dialogue
    for scene in scenes:
        if not scene.get("dialogue", "").strip():
            issues.append(f"Scene {scene.get('scene_id')} has no dialogue")
    
    # Check dialogue length (should be 10-15 words for 7 seconds)
    for scene in scenes:
        word_count = len(scene.get("dialogue", "").split())
        if word_count > 20:  # Warning if too long
            issues.append(f"Scene {scene.get('scene_id')} has {word_count} words (should be 10-15 for 7 sec)")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues
    }


def estimate_duration(dialogue: str) -> float:
    """
    Estimate dialogue duration based on word count.
    Average speaking rate: ~150 words per minute = 2.5 words per second.
    
    Args:
        dialogue: The dialogue text
    
    Returns:
        Estimated duration in seconds
    """
    word_count = len(dialogue.split())
    duration = word_count / 2.5  # words per second
    return round(duration, 1)


def get_scene_beats(scenes: list) -> dict:
    """
    Extract the 'beat' or emotional/narrative purpose of each scene.
    
    Args:
        scenes: List of scene objects
    
    Returns:
        dict mapping scene_id to beat description
    """
    
    beats = {
        1: "Hook - Opening trigger",
        2: "Hook - Emotional escalation",
        3: "Hook - Bold demand",
        4: "Build - Argument continues",
        5: "Build - Emotional peak",
        6: "Build - Calm observation",
        7: "Pivot - First trap question",
        8: "Pivot - Tension builds",
        9: "Pivot - Defensive reaction",
        10: "Dunk - Logic begins",
        11: "Dunk - Nigerian context",
        12: "Dunk - Conclusion",
        13: "Dunk - Mic drop"
    }
    
    return {scene["scene_id"]: beats.get(scene["scene_id"], "Unknown") for scene in scenes}


if __name__ == "__main__":
    # Test scene parsing with 13 scenes
    test_scenes = [
        {"scene_id": i, "dialogue": f"Test dialogue for scene {i}"} 
        for i in range(1, 14)
    ]
    
    parsed = parse_scenes(test_scenes)
    
    print("✅ Parsed 13 Scenes:")
    for scene in parsed:
        print(f"\nScene {scene['scene_id']}: {scene['shot_type']} ({scene['phase']})")
        print(f"Duration: {scene['duration']}")
        print(f"Camera: {scene['camera_angle']}")
    
    # Validate
    validation = validate_scene_structure(parsed)
    print(f"\n{'✅' if validation['valid'] else '❌'} Validation: {validation}")
