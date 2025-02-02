#!/usr/bin/python3

from googleapiclient.discovery import build
from datetime import datetime
import re
import os
from urllib.parse import parse_qs, urlparse
import yaml

# Configuration
# Get API key from: https://console.cloud.google.com/apis/credentials?referrer=search&inv=1&invt=AbofsA&project=piers-rocks-youtube
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')  # Get from environment variable

POSTS_DIR = '_posts'  # Default Jekyll posts directory
YOUTUBE_TEMPLATE = '''---
layout: post
title: "{title}"
date: {date}
categories: youtube
youtube_id: {video_id}
---

<!-- You can customize your embedded video appearance -->
<div class="video-container">
    <iframe 
        width="560" 
        height="315" 
        src="https://www.youtube.com/embed/{video_id}" 
        frameborder="0" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen>
    </iframe>
</div>

{description}'''

def format_description(description):
    """Format YouTube description for kramdown Markdown compatibility."""
    # Split into lines
    lines = description.split('\n')
    formatted_lines = []
    
    # Process each line
    in_timestamps = False
    
    for line in lines:
        stripped_line = line.strip()
        
        # Handle empty lines
        if not stripped_line:
            formatted_lines.append('')
            continue
            
        # Check if this is a timestamp line or timestamp header
        is_timestamp = bool(re.match(r'^\d{1,2}:\d{2}', stripped_line))
        is_timestamp_header = stripped_line.lower() == 'timestamps:'
        
        if is_timestamp_header:
            if not in_timestamps:
                formatted_lines.extend(['', '### Timestamps', ''])
                in_timestamps = True
            continue
            
        if is_timestamp:
            formatted_lines.append(stripped_line + '  ')
        else:
            # Handle URLs
            if 'http' in stripped_line:
                # Find all URLs in the line
                words = stripped_line.split()
                formatted_words = []
                for word in words:
                    if word.startswith('http'):
                        formatted_words.append(f'<{word}>')
                    else:
                        formatted_words.append(word)
                formatted_lines.append(' '.join(formatted_words) + '  ')
            else:
                formatted_lines.append(stripped_line + '  ')
    
    # Join lines with proper line breaks
    return '\n'.join(formatted_lines)

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
    raise ValueError('Invalid YouTube URL')

def get_video_info(video_id, api_key):
    """Fetch video information using YouTube Data API."""
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    
    if not response['items']:
        raise ValueError('Video not found')
        
    video_info = response['items'][0]['snippet']
    return {
        'title': video_info['title'],
        'description': format_description(video_info['description']),
        'date': video_info['publishedAt'][:10]  # YYYY-MM-DD format
    }

def create_blog_post(video_url):
    """Create a new blog post from YouTube video."""
    try:
        # Get video ID and info
        video_id = get_video_id(video_url)
        video_info = get_video_info(video_id, YOUTUBE_API_KEY)
        
        # Create filename with date prefix (Jekyll format)
        date = datetime.strptime(video_info['date'], '%Y-%m-%d')
        title_slug = re.sub(r'[^a-zA-Z0-9-]', '-', video_info['title'].lower())
        filename = f"{date.strftime('%Y-%m-%d')}-{title_slug}.md"
        
        # Ensure posts directory exists
        os.makedirs(POSTS_DIR, exist_ok=True)
        filepath = os.path.join(POSTS_DIR, filename)
        
        # Create post content
        content = YOUTUBE_TEMPLATE.format(
            title=video_info['title'],
            date=video_info['date'],
            description=video_info['description'],
            video_id=video_id
        )
        
        # Write the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Created blog post: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"Error creating blog post: {str(e)}")
        return None

if __name__ == "__main__":
    if not YOUTUBE_API_KEY:
        print("Error: YOUTUBE_API_KEY environment variable not set")
        exit(1)
    
    video_url = input("Enter YouTube video URL: ")
    create_blog_post(video_url)
