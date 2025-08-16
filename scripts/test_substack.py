#!/usr/bin/env python3
import feedparser
import requests

url = "https://promisingparagraphs.substack.com/feed"
print(f"Testing feed: {url}")

try:
    # Test with requests first
    response = requests.get(url, timeout=30)
    print(f"HTTP status: {response.status_code}")
    print(f"Content length: {len(response.text)}")
    print(f"First 200 chars: {response.text[:200]}")
    
    # Test with feedparser
    d = feedparser.parse(url)
    print(f"Feed title: {getattr(d.feed, 'title', 'No title')}")
    print(f"Number of entries: {len(d.entries)}")
    
    if d.entries:
        first = d.entries[0]
        print(f"First entry title: {first.get('title', 'No title')}")
        print(f"First entry date: {first.get('published', 'No date')}")
        
except Exception as e:
    print(f"Error: {e}")
