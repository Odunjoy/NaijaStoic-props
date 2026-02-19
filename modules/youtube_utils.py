import os
import yt_dlp
import requests
import glob

def download_video(url, output_path="downloads"):
    """
    Kept for compatibility. On Streamlit Cloud, actual video download
    is not possible without ffmpeg. Use extract_frames_from_url instead.
    Returns None gracefully so the UI can fall back.
    """
    return None

def extract_frames_from_url(url, output_path="frames", num_frames=6):
    """
    Cloud-safe frame extraction: uses yt-dlp to get thumbnail/storyboard URLs
    and downloads them as image frames — no ffmpeg or video download needed.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save frames
        num_frames (int): Number of frames to extract
        
    Returns:
        list: List of paths to extracted frame images
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Clear existing frames
    for f in glob.glob(os.path.join(output_path, "*")):
        try:
            os.remove(f)
        except:
            pass
    
    extracted_paths = []
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'write_thumbnail': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        # Strategy 1: Use storyboard/heatmap thumbnails if available
        thumbnails = info.get('thumbnails', [])
        
        # Filter to images only (not storyboards which are webp sequences)
        image_thumbs = [
            t for t in thumbnails
            if t.get('url') and
            not any(x in t.get('url','') for x in ['storyboard', 'sb=', 'M'])
        ]
        
        # Sort by resolution descending and pick most distinct ones
        image_thumbs.sort(key=lambda t: (t.get('width', 0) * t.get('height', 0)), reverse=True)
        
        # Pick evenly spaced thumbnails to simulate scene extraction
        if image_thumbs:
            # Deduplicate by URL
            seen_urls = set()
            unique_thumbs = []
            for t in image_thumbs:
                if t['url'] not in seen_urls:
                    seen_urls.add(t['url'])
                    unique_thumbs.append(t)
            
            # Select num_frames evenly spaced
            step = max(1, len(unique_thumbs) // num_frames)
            selected = unique_thumbs[::step][:num_frames]
            
            # If we have fewer than requested, pad with the main thumbnail
            if not selected:
                thumb_url = info.get('thumbnail')
                if thumb_url:
                    selected = [{'url': thumb_url}] * min(num_frames, 3)
        else:
            # Fallback: just use the main thumbnail duplicated
            thumb_url = info.get('thumbnail')
            selected = [{'url': thumb_url}] * min(num_frames, 1) if thumb_url else []
        
        # Download the selected thumbnail images
        headers = {'User-Agent': 'Mozilla/5.0'}
        for i, thumb in enumerate(selected):
            try:
                resp = requests.get(thumb['url'], headers=headers, timeout=10)
                if resp.status_code == 200:
                    frame_path = os.path.join(output_path, f"frame_{i+1}.jpg")
                    with open(frame_path, 'wb') as f:
                        f.write(resp.content)
                    extracted_paths.append(frame_path)
            except Exception as e:
                print(f"Frame {i+1} download error: {e}")
        
    except Exception as e:
        print(f"Error extracting frames: {e}")
    
    return extracted_paths


def extract_frames(video_path, output_path="frames", num_frames=6):
    """
    Legacy function kept for compatibility.
    On Streamlit Cloud, video download is unavailable.
    Returns empty list — caller should use extract_frames_from_url instead.
    """
    return []


def get_video_info(url):
    """
    Get video title and duration without downloading.
    """
    ydl_opts = {'quiet': True, 'no_warnings': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get('title', 'Unknown Title'),
                "duration": info.get('duration', 0),
                "thumbnail": info.get('thumbnail', None)
            }
    except:
        return None
def get_transcript(url):
    """
    Extract transcript from a YouTube video.
    """
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        # Extract video ID from URL
        video_id = None
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            
        if not video_id:
            return None
            
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t['text'] for t in transcript_list])
        return transcript_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None
