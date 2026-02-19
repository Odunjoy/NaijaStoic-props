"""
Module C: Visual Asset Generation (Image Prompts)
Generates prompts for DALL-E 3 or Midjourney to create the "Naija Lofi" aesthetic.
UPDATED: Single location (Lagos rooftop lounge) - only camera angles change.
UPDATED: Supports 2D Lofi Anime and 3D CGI animation styles.
"""

import google.generativeai as genai
import PIL.Image
import json

# Animation style presets
ANIMATION_STYLES = {
    "2d_lofi": {
        "name": "2D Lofi Anime",
        "base_style": "2D lofi anime style, clean flat colors, minimalist shading",
        "aspect_ratio": "vertical 9:16"
    },
    "3d_cgi": {
        "name": "3D CGI Pixar Style",
        "base_style": "3D CGI animated film style, large expressive eyes, smooth shading",
        "aspect_ratio": "vertical 9:16"
    }
}

# DEFAULT LOCATION (Fallback)
DEFAULT_LOCATION = "high-end bedroom with a large wardrobe in the background, modern Nigerian interior design, softly lit, luxury Lekki home"

# BASE CHARACTER PROMPTS (Strict physical anchors for consistency)
# BASE CHARACTER PROMPTS (Strict physical anchors for consistency)
CHARACTERS = {
    "odogwu": {
        "base_desc": "Full image of a muscular Nigerian man, 30s, dark skin, wearing only English style clothing, short-cropped buzz cut hairstyle, sharp goatee, high cheekbones",
        "name": "Odogwu",
        "display_name": "Odogwu (Dad)"
    },
    "antagonist": {
        "base_desc": "Full image of a tall curvy Nigerian woman, 30s, medium dark skin, wearing only English style clothing, large round afro hairstyle, wearing stylish black frame glasses, bold red lipstick",
        "name": "Chioma",
        "display_name": "Mom/Chioma"
    },
    "dad": {
        "base_desc": "Full image of a muscular Nigerian man, 30s, dark skin, wearing only English style clothing, short-cropped buzz cut hairstyle, sharp goatee",
        "name": "Odogwu"
    },
    "mom": {
        "base_desc": "Full image of a curvy Nigerian woman, 30s, medium dark skin, wearing only English style clothing, large round afro hairstyle, wearing black glasses, bold red lipstick",
        "name": "Amaka"
    },
    "triplet": {
        "base_desc": "Full image of a pretty young Nigerian woman, 20s, dark skin, wearing only English style clothing, long braided cornrows hairstyle, expressive big eyes",
        "name": "Ngozi"
    },
    "segun": {
        "base_desc": "Full image of a handsome Nigerian man, 20s, medium skin, wearing only English style clothing, stylish low-fade haircut, clean shaven",
        "name": "Segun"
    }
}

# OUTFIT POOLS (Diverse Nigerian Styles)
OUTFIT_POOLS = {
    "odogwu": [
        "a sharp tailored grey blazer over a black turtleneck and slim-fit trousers",
        "a fitted cream hoodie with dark cargo pants and clean streetwear sneakers",
        "a crisp white linen button-down shirt with dark blue fitted denim jeans",
        "a classic-fit denim jacket over a white t-shirt and charcoal chinos",
        "a sleek navy blue bomber jacket with a plain t-shirt and dark jeans",
        "a structured tan trench coat over a high-neck sweater and dress pants",
        "a premium cotton polo shirt with well-fitted chinos",
        "casual wear featuring a high-quality beautiful shirt and stylish trousers",
        "a smart-casual look with a leather jacket over a simple tee and jeans"
    ],
    "antagonist": [
        "a sophisticated long floral maxi dress with a high neckline and elegant long sleeves",
        "a modest knee-length floral midi dress with a high neckline and long sleeves",
        "high-waisted long denim jeans with a crisp white tailored button-down shirt",
        "a tailored beige blazer over a full-length maxi skirt and simple top",
        "a tailored blazer over a professional knee-length pencil skirt and blouse",
        "elegant wide-leg trousers with a fitted turtleneck sweater and gold jewelry",
        "a sophisticated English-style wrap midi dress that hits just at the knee",
        "a modest silk blouse with a high-neck and structured full-length trousers",
        "a beautiful fitted shirt with a stylish knee-length skirt",
        "premium casual wear with designer jeans and a chic top"
    ]
}

# STYLING POOLS
HAIRSTYLES = ["a neatly faded haircut", "braided cornrows", "an elegant low bun", "a stylish afro", "short natural hair"]
MAKEUP = ["clean skin and natural look", "bold red lipstick and perfect contour", "shimmery eyeshadow and glossy lips", "a fresh-faced glow"]
ACCESSORIES = ["a luxury wristwatch", "stylish eyeglasses", "a delicate gold necklace"]
SHOES = ["polished loafers", "clean designer sneakers", "elegant high heels", "stylish leather sandals", "classic dress shoes"]

# LOCATION POOL (Diverse fallback locations)
LOCATION_POOL = [
    "high-end bedroom with a large wardrobe in the background, modern Nigerian interior design",
    "luxury Lagos penthouse living room with floor-to-ceiling windows showing city lights",
    "contemporary home office with mahogany furniture and modern minimalist art",
    "exclusive rooftop lounge in Victoria Island with a view of the Atlantic",
    "modern minimalist kitchen with marble countertops and sleek appliances",
    "lush private garden patio with tropical plants and soft ambient lighting",
    "sophisticated private library with wall-to-wall books and leather armchairs"
]

# POSTURE POOL
POSTURE_POOL = [
    "both standing fully visible",
    "both sitting comfortably",
    "Odogwu standing while Chioma is sitting",
    "Chioma standing while Odogwu is sitting"
]


def analyze_visual_style(image_paths: list, api_key: str) -> dict:
    """
    Analyze a set of images using Gemini Vision to extract their visual style AND location.
    
    Args:
        image_paths: List of file paths to images
        api_key: Google Gemini API key
        
    Returns:
        Dictionary with 'style' (lighting, color, vibe) and 'location' (setting description)
    """
    if not image_paths or not api_key:
        return {"style": "", "location": ""}
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Load images
        images = []
        for path in image_paths[:4]: # Limit to 4 images to save tokens/bandwidth
            try:
                img = PIL.Image.open(path)
                images.append(img)
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                
        if not images:
            return {"style": "", "location": ""}
            
        prompt = """
        Analyze these screenshots from a video. Return a JSON object with three keys:
        1. "style": Describe the lighting, color palette, **dominant camera angles/composition** (e.g., low angle, wide shot, dutch tilt), and overall visual vibe (concise, < 50 words).
        2. "location": Describe the physical setting/environment where the scene takes place (e.g., "futuristic neon bar", "cluttered living room", "sunny park") (concise, < 20 words).
        3. "posture": Describe if the characters are mostly standing, sitting, or a mix (e.g., "both standing", "both sitting", "one standing, one sitting").
        
        Output ONLY the JSON string.
        """
        
        response = model.generate_content(images + [prompt])
        text_response = response.text.strip()
        
        # Clean up JSON if response contains markdown blocks
        if "```json" in text_response:
            text_response = text_response.replace("```json", "").replace("```", "")
        
        try:
            return json.loads(text_response)
        except json.JSONDecodeError:
            # Fallback if valid JSON isn't returned
            print(f"JSON Decode Error. Raw response: {text_response}")
            return {"style": text_response, "location": "", "posture": ""}
        
    except Exception as e:
        print(f"Error analyzing images: {e}")
        return {"style": "", "location": "", "posture": ""}


def generate_character_style(character_target: str, outfit_override: str = None) -> str:
    """
    Generate a unique character style by combining outfit, hair, makeup, and accessories.
    """
    import random
    
    outfit = outfit_override or random.choice(OUTFIT_POOLS.get(character_target, OUTFIT_POOLS["odogwu"]))
    hair = random.choice(HAIRSTYLES)
    makeup = random.choice(MAKEUP)
    acc = random.choice(ACCESSORIES)
    shoes = random.choice(SHOES)
    
    # Antagonist gets more makeup emphasis, Odogwu gets more hair/acc emphasis
    if character_target == "antagonist":
        return f"wearing {outfit}, with {hair}, {makeup}, accessorized with {acc}, and wearing {shoes}"
    else:
        return f"wearing {outfit}, with {hair}, looking clean with {makeup}, accessorized with {acc}, and wearing {shoes}"


def generate_base_character_prompt(character_type: str, animation_style: str = "3d_cgi", outfit_override: str = None) -> str:
    """
    Generate a base character reference prompt.
    """
    char = CHARACTERS.get(character_type, CHARACTERS["odogwu"])
    style = ANIMATION_STYLES.get(animation_style, ANIMATION_STYLES["3d_cgi"])
    
    outfit = outfit_override or OUTFIT_POOLS[character_type][0]
    
    return f"{char['display_name']}: {char['base_desc']}, {outfit}. {style['base_style']}, {style['aspect_ratio']}."


def generate_scene_setup_prompt(animation_style: str = "3d_cgi", story_context: dict = None, visual_context: dict = None) -> str:
    """
    Generate a comprehensive scene setup prompt that establishes the environment.
    Uses Character Anchors for Dad and Mom to ensure consistency.
    """
    import random
    style = ANIMATION_STYLES.get(animation_style, ANIMATION_STYLES["3d_cgi"])
    
    if story_context is None:
        story_context = {"prop_description": "", "outfit_changes": {}}
        
    # Handle visual context
    if isinstance(visual_context, dict):
        style_desc = visual_context.get("style", "")
        location_desc = visual_context.get("location") or random.choice(LOCATION_POOL)
        posture_desc = visual_context.get("posture") or "standing"
    else:
        style_desc = ""
        location_desc = random.choice(LOCATION_POOL)
        posture_desc = "standing"
    
    # 1. Physical Anchors
    dad_base = CHARACTERS["dad"]["base_desc"]
    mom_base = CHARACTERS["mom"]["base_desc"]
    
    # 2. Styles
    outfits = story_context.get("outfit_changes", {})
    dad_style = generate_character_style("odogwu", outfits.get("odogwu"))
    mom_style = generate_character_style("antagonist", outfits.get("antagonist"))
    
    dad_full = f"Dad (Odogwu): {dad_base}, {dad_style}"
    mom_full = f"Mom (Amaka): {mom_base}, {mom_style}"
    
    # Build context-specific scene elements
    prop_description = story_context.get("prop_description", "")
    context_element = f"The focal point features {prop_description}. " if prop_description else ""
    
    # Incorporate visual context
    style_instruction = f"{style['base_style']}"
    if style_desc:
        style_instruction = f"Visual Style: {style_desc}. {style_instruction}"
    
    # Strictly enforce positioning and Western attire
    return f"""Scene Setup - Clear Wide shot: {dad_full} and {mom_full}. Both characters are positioned professionally for a dialogue scene, with Odogwu standing on the left side and Amaka standing on the right side of the frame. STRICT MANDATE: Characters must wear ONLY English Western style clothing (suites, shirts, jeans) - NO traditional wear or kaftans. Both characters are fully visible in a {location_desc}, maintaining physical anchors (Dad's buzz cut and Mom's Afro/glasses). {context_element}The composition is clean and balanced. {style_instruction}, {style['aspect_ratio']}."""


def generate_establishing_shot(animation_style: str = "3d_cgi") -> str:
    """
    Generate the location establishing shot prompt.
    """
    style = ANIMATION_STYLES.get(animation_style, ANIMATION_STYLES["3d_cgi"])
    return f"Location: Full image of both characters standing in a {DEFAULT_LOCATION}. {style['base_style']}, {style['aspect_ratio']}."


def generate_image_prompt(scene: dict, variation: str = "default", animation_style: str = "3d_cgi", visual_context: dict = None, outfit_override: dict = None) -> str:
    """
    Generate a complete image prompt with character description.
    Supports fixed anchors for Dad/Mom/Triplets AND dynamic looks for others.
    """
    import random
    scene_id = scene.get("scene_id", 1)
    camera_angle = scene.get("camera_angle", "Close-up")
    character_name = scene.get("character", "protagonist").lower()
    phase = scene.get("phase", "Hook")
    
    # Handle visual context and location overriding
    scene_location = scene.get("location_context")
    if isinstance(visual_context, dict):
        style_desc = visual_context.get("style", "")
        location_desc = scene_location or visual_context.get("location") or random.choice(LOCATION_POOL)
        posture_desc = visual_context.get("posture") or "standing"
    else:
        style_desc = ""
        location_desc = scene_location or random.choice(LOCATION_POOL)
        posture_desc = "standing"

    # Get style preset
    style = ANIMATION_STYLES.get(animation_style, ANIMATION_STYLES["3d_cgi"])
    
    # 1. Resolve Character Roles and Physical Anchors
    dad_full = f"Dad (Odogwu): {CHARACTERS['dad']['base_desc']}"
    mom_full = f"Mom (Amaka): {CHARACTERS['mom']['base_desc']}"
    triplet_full = f"Triplet: {CHARACTERS['triplet']['base_desc']}"

    # Detect character type and physical anchor
    focus_char_desc = ""
    display_name = scene.get("character", "Character")
    is_female = False
    
    if "dad" in character_name or "odogwu" in character_name:
        focus_char_desc = dad_full
    elif "mom" in character_name or "amaka" in character_name:
        focus_char_desc = mom_full
        is_female = True
    elif "triplet" in character_name or "ngozi" in character_name or "chioma" in character_name or "princess" in character_name:
        focus_char_desc = triplet_full
        is_female = True
    elif "segun" in character_name:
        focus_char_desc = f"{display_name}: {CHARACTERS['segun']['base_desc']}"
    else:
        # DYNAMIC LOOK for unique story characters
        # We vary skin tone, hair, and simple traits to avoid repetition
        skin = random.choice(["dark", "medium-dark", "rich ebony"])
        hair = random.choice(["short hair", "braided hair", "neat fade", "locs"])
        gender_clue = "woman" if any(x in character_name for x in ["she", "her", "lady", "girl", "auntie", "sister"]) else "man"
        if gender_clue == "woman": is_female = True
        focus_char_desc = f"{display_name}: full image of a Nigerian {gender_clue}, {skin} skin, {hair}"

    # 2. Get Outfit
    outfits = outfit_override or {}
    outfit_key = "antagonist" if is_female else "odogwu"
    char_styling = generate_character_style(outfit_key, outfits.get(outfit_key))
    
    focus_desc_with_outfit = f"{focus_char_desc}, {char_styling}"

    # 3. Get Character Action
    action = scene.get("action_description") or get_scene_action_detailed(phase, "protagonist" if not is_female else "antagonist", scene_id)
    
    # 4. Handle Shot Type
    if "Wide" in camera_angle:
        context = f"wide shot focusing on {focus_desc_with_outfit}."
        action = f"{action}, while {posture_desc}"
    else:
        context = f"close-up shot of {focus_desc_with_outfit}."

    # 5. Style instruction
    style_instruction = f"{style['base_style']}"
    variations = get_style_variations()
    grading = variations.get(variation, "")
    if grading: style_instruction += f", {grading}"
    if style_desc: style_instruction = f"Visual Style: {style_desc}. {style_instruction}"

    # 6. Construct FINAL prompt
    prompt = f"{context} {action}. Background is a {location_desc}. {style_instruction}, {style['aspect_ratio']}."
    
    return prompt


def generate_image_prompt_condensed(scene: dict, variation: str = "default", animation_style: str = "3d_cgi", visual_context: dict = None) -> str:
    """
    Generate a condensed image prompt WITHOUT character visual descriptions.
    Includes only talking context, background, and style instructions.
    Useful for production pipelines where characters are already defined.
    """
    import random
    camera_angle = scene.get("camera_angle", "Medium Shot")
    character = scene.get("character", "protagonist")
    
    # Handle visual context and location overriding
    scene_location = scene.get("location_context")
    
    if isinstance(visual_context, dict):
        style_desc = visual_context.get("style", "")
        location_desc = scene_location or visual_context.get("location") or random.choice(LOCATION_POOL)
    else:
        style_desc = ""
        location_desc = scene_location or random.choice(LOCATION_POOL)

    # Get style preset
    style = ANIMATION_STYLES.get(animation_style, ANIMATION_STYLES["3d_cgi"])
    
    # Determine who is talking to whom
    if character == "protagonist":
        talking_context = f"{CHARACTERS['odogwu']['name']} talking to {CHARACTERS['antagonist']['name']}"
    elif character == "antagonist":
        talking_context = f"{CHARACTERS['antagonist']['name']} talking to {CHARACTERS['odogwu']['name']}"
    else:
        talking_context = f"{CHARACTERS['odogwu']['name']} and {CHARACTERS['antagonist']['name']} in conversation"
    
    # Style instruction
    style_instruction = f"{style['base_style']}"
    variations = get_style_variations()
    grading = variations.get(variation, "")
    if grading:
        style_instruction += f", {grading}"
        
    if style_desc:
        style_instruction = f"Visual Style: {style_desc}. {style_instruction}"

    # Return condensed prompt
    return f"{talking_context}. Background is a {location_desc}. {style_instruction}, {style['aspect_ratio']}."


def get_scene_action_detailed(phase: str, character: str, scene_id: int) -> str:
    """
    Get detailed action/expression for character based on phase.
    """
    # (Existing logic remains the same, assuming generic actions apply to any location)
    # Hook phase (1-3)
    if phase == "Hook":
        if character == "antagonist":
            return "looking emotional or dramatic, using wild hand gestures to emphasize her point, standing with entitled expression"
        else:
            return "standing calmly with arms crossed, neural expression, observing quietly"
    
    # Build phase (4-6)
    elif phase == "Build":
        if character == "antagonist":
            return "gesturing passionately, defensive body language, maintaining strong eye contact"
        else:
            return "listening calmly with hands in pockets, slight head tilt, composed expression, standing still"
    
    # Pivot phase (7-9)
    elif phase == "Pivot":
        if character == "protagonist":
            return "asking a question calmly, slight eyebrow raise, direct gaze, one hand gesturing reasonably"
        elif character == "antagonist":
            return "caught off guard, processing the question with confused expression, slightly defensive posture"
        else:  # both
            return "engaged in tense dialogue, protagonist calm and analytical, antagonist reactive and emotional"
    
    # Dunk phase (10-13)
    elif phase == "Dunk":
        if character == "protagonist":
            if scene_id == 13:  # Final mic drop
                return "delivering final point with calm authority, knowing smile, hands open in explaining gesture, standing confidently"
            else:
                return "explaining logically with measured hand gestures, composed expression, making clear points while standing firm"
        else:
            return "deflated posture, speechless expression, hand dropped to side, argument weakening"
    
    return "standing naturally"


def get_style_variations() -> dict:
    """
    Return available style variations for user selection.
    """
    return {
        "default": "Balanced Naija Lofi - Purple/Blue grading",
        "luxury": "Enhanced Gold - Warmer purple with gold accents",
        "premium": "Deep Teal - Sophisticated purple and teal palette"
    }


def get_animation_styles() -> dict:
    """
    Return available animation styles for user selection.
    """
    return {
        "2d_lofi": "2D Lofi Anime (Flat colors, clean lines)",
        "3d_cgi": "3D CGI Pixar Style (Large eyes, smooth shading)"
    }


def generate_props(animation_style: str = "3d_cgi", story_context: dict = None, visual_context: dict = None, locations: list = None) -> dict:
    """
    Generate a set of reference prompts (props) for the story assets.
    Returns prompts for Hero, Antagonist, and Setting(s).
    """
    import random
    style = ANIMATION_STYLES.get(animation_style, ANIMATION_STYLES["3d_cgi"])
    
    if story_context is None:
        story_context = {"prop_description": "", "outfit_changes": {}}
        
    # Handle visual context
    if isinstance(visual_context, dict):
        style_desc = visual_context.get("style", "")
        base_location = visual_context.get("location") or random.choice(LOCATION_POOL)
    else:
        style_desc = ""
        base_location = random.choice(LOCATION_POOL)
    
    # Get character styling
    outfits = story_context.get("outfit_changes", {})
    odogwu_style = generate_character_style("odogwu", outfits.get("odogwu"))
    chioma_style = generate_character_style("antagonist", outfits.get("antagonist"))
    
    # Style instruction
    style_instruction = f"{style['base_style']}"
    if style_desc:
        style_instruction = f"Visual Style: {style_desc}. {style_instruction}"
        
    props = {
        "hero": f"Character Reference Profile: {CHARACTERS['odogwu']['base_desc']}, {odogwu_style}. Standing against a plain background for reference. {style_instruction}, {style['aspect_ratio']}.",
        "antagonist": f"Character Reference Profile: {CHARACTERS['antagonist']['base_desc']}, {chioma_style}. Standing against a plain background for reference. {style_instruction}, {style['aspect_ratio']}.",
    }
    
    # Generate setting props
    if locations:
        for loc in locations:
            loc_id = loc.get("location_id", 1)
            loc_desc = loc.get("location_description", base_location)
            props[f"setting_loc_{loc_id}"] = f"Environment Reference (Location {loc_id}): Full shot of the {loc_desc} with no characters. Show lighting, architectural details, and atmosphere. {style_instruction}, {style['aspect_ratio']}."
    else:
        props["setting"] = f"Environment Reference: Full shot of the {base_location} with no characters. Show lighting, architectural details, and atmosphere. {style_instruction}, {style['aspect_ratio']}."
        
    return props


if __name__ == "__main__":
    # Test
    print("✅ Visual Generator Loaded (Updated with Dynamic Location & Style)")
