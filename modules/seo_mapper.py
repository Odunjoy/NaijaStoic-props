"""
Module F: SEO & Data Management
Reads CSV and maps SEO data to generated content.
"""

import pandas as pd
import os
from typing import Optional


def load_seo_database(csv_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load the SEO content database from CSV.
    
    Args:
        csv_path: Optional path to CSV file (uses default if not provided)
    
    Returns:
        pandas DataFrame with SEO content
    """
    
    if csv_path is None:
        # Use default path
        csv_path = os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "data", 
            "seo_content.csv"
        )
    
    try:
        df = pd.read_csv(csv_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"SEO database not found at {csv_path}")
    except Exception as e:
        raise Exception(f"Error loading SEO database: {str(e)}")


def match_content(script_text: str, seo_db: pd.DataFrame, row_id: Optional[int] = None) -> dict:
    """
    Match script content to SEO data.
    
    Args:
        script_text: The script or dialogue text
        seo_db: SEO database DataFrame
        row_id: Optional specific row ID to use (1-58)
    
    Returns:
        dict with title, tags, hashtags
    """
    
    # If specific row ID provided, use that
    if row_id is not None:
        row = seo_db[seo_db['id'] == row_id]
        if not row.empty:
            return row_to_dict(row.iloc[0])
    
    # Otherwise, try to match based on keywords
    matched_row = keyword_match(script_text, seo_db)
    
    if matched_row is not None:
        return row_to_dict(matched_row)
    else:
        # Return default/generic SEO
        return get_default_seo()


def keyword_match(script_text: str, seo_db: pd.DataFrame) -> Optional[pd.Series]:
    """
    Match script to SEO row based on keyword analysis.
    
    Args:
        script_text: Script text to analyze
        seo_db: SEO database
    
    Returns:
        Best matching row or None
    """
    
    script_lower = script_text.lower()
    
    # Define keyword groups
    keyword_groups = {
        "breakfast": [1, 4],  # Breakup/dating issues
        "money": [2, 5, 15, 29],  # Financial topics
        "bills": [2, 5, 13, 20],  # Bill-splitting
        "emotional": [3, 28, 48],  # Emotional labor
        "independent": [11, 49],  # Independent woman
        "provider": [5, 21, 52],  # Provider role
        "prize": [25],  # Prize mentality
        "marriage": [9, 10, 36, 46],  # Marriage topics
        "format": [4, 35],  # Double standards
        "sapa": [2, 34],  # Financial struggle
    }
    
    # Score each keyword group
    scores = {}
    for keyword, row_ids in keyword_groups.items():
        if keyword in script_lower:
            for row_id in row_ids:
                scores[row_id] = scores.get(row_id, 0) + 1
    
    # Get best match
    if scores:
        best_id = max(scores, key=scores.get)
        return seo_db[seo_db['id'] == best_id].iloc[0]
    
    return None


def row_to_dict(row: pd.Series) -> dict:
    """
    Convert database row to SEO dict.
    
    Args:
        row: pandas Series from database
    
    Returns:
        dict with SEO data
    """
    
    # Parse tags and hashtags (they're stored as comma-separated)
    tags = row['tags'].split(',') if pd.notna(row['tags']) else []
    hashtags = row['hashtags'].split(',') if pd.notna(row['hashtags']) else []
    
    return {
        "title": row['naija_title'],
        "tags": [tag.strip() for tag in tags],
        "hashtags": [tag.strip() for tag in hashtags],
        "row_id": int(row['id']) if pd.notna(row['id']) else None
    }


def get_default_seo() -> dict:
    """
    Get default SEO data for unmatched content.
    
    Returns:
        dict with generic Nigerian Stoic SEO
    """
    
    return {
        "title": "Naija Stoic Logic 🧠",
        "tags": ["Stoicism", "Nigeria", "Relationships", "Logic"],
        "hashtags": ["#nogreeforanybody", "#naija", "#stoic", "#logic"]
    }


def get_trending_hashtags() -> list:
    """
    Get current trending Nigerian hashtags.
    
    Returns:
        List of trending hashtags
    """
    
    return [
        "#nogreeforanybody",
        "#fearwomen",
        "#naija",
        "#Lagos",
        "#relationships",
        "#stoic",
        "#redpill",
        "#sapa",
        "#breakfast"
    ]


def enhance_seo(seo_data: dict, add_trending: bool = True) -> dict:
    """
    Enhance SEO data with additional trending tags.
    
    Args:
        seo_data: Base SEO data dict
        add_trending: Whether to add trending hashtags
    
    Returns:
        Enhanced SEO data
    """
    
    if add_trending:
        trending = get_trending_hashtags()
        current_hashtags = seo_data.get("hashtags", [])
        
        # Add trending tags not already present
        for tag in trending[:3]:  # Add top 3 trending
            if tag not in current_hashtags:
                current_hashtags.append(tag)
        
        seo_data["hashtags"] = current_hashtags
    
    return seo_data


def get_seo_by_id(row_id: int, csv_path: Optional[str] = None) -> dict:
    """
    Get SEO data for a specific row ID.
    
    Args:
        row_id: Row ID (1-58)
        csv_path: Optional CSV path
    
    Returns:
        SEO data dict
    """
    
    seo_db = load_seo_database(csv_path)
    row = seo_db[seo_db['id'] == row_id]
    
    if not row.empty:
        return row_to_dict(row.iloc[0])
    else:
        return get_default_seo()


def list_all_titles(csv_path: Optional[str] = None) -> list:
    """
    List all available Naija titles from database.
    
    Args:
        csv_path: Optional CSV path
    
    Returns:
        List of tuples (id, naija_title)
    """
    
    seo_db = load_seo_database(csv_path)
    return list(zip(seo_db['id'], seo_db['naija_title']))


if __name__ == "__main__":
    # Test SEO mapper
    print("✅ Loading SEO Database...\n")
    
    db = load_seo_database()
    print(f"Loaded {len(db)} SEO entries")
    
    # Test keyword matching
    test_script = "She want me to pay all the bills but refuse to cook. That's not relationship, that's employment!"
    
    seo = match_content(test_script, db)
    print(f"\n📊 Matched SEO:")
    print(f"Title: {seo['title']}")
    print(f"Tags: {', '.join(seo['tags'])}")
    print(f"Hashtags: {', '.join(seo['hashtags'])}")
    
    # Test listing
    print("\n📝 First 5 Titles:")
    titles = list_all_titles()
    for id, title in titles[:5]:
        print(f"  {id}. {title}")
