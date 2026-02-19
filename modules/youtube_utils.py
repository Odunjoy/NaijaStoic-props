import os
import cv2
import yt_dlp
import glob

def download_video(url, output_path="downloads"):
    """
    Download a YouTube video using yt-dlp.
    
    Args:
        url (str): YouTube video URL
        output_path (str): Directory to save the video
        
    Returns:
        str: Path to the downloaded video file, or None if failed
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Configure yt-dlp to download best quality mp4 that doesn't require ffmpeg merging
    ydl_opts = {
        'format': 'best[ext=mp4]/best',  # Prefer mp4, fallback to best
        'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info['id']
            ext = info['ext']
            return os.path.join(output_path, f"{video_id}.{ext}")
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

def extract_frames(video_path, output_path="frames", num_frames=6):
    """
    Extract frames from a video file at regular intervals.
    
    Args:
        video_path (str): Path to the video file
        output_path (str): Directory to save frames
        num_frames (int): Number of frames to extract
        
    Returns:
        list: List of paths to extracted frame images
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    # Clear existing frames
    files = glob.glob(os.path.join(output_path, "*"))
    for f in files:
        try:
            os.remove(f)
        except:
            pass
            
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        return []
        
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps > 0 else 0
    
    extracted_paths = []
    
    if total_frames > 0:
        interval = total_frames // (num_frames + 1)
        
        for i in range(num_frames):
            frame_id = interval * (i + 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
            ret, frame = cap.read()
            
            if ret:
                frame_path = os.path.join(output_path, f"frame_{i+1}.jpg")
                cv2.imwrite(frame_path, frame)
                extracted_paths.append(frame_path)
                
    cap.release()
    return extracted_paths

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
