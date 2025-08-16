#!/usr/bin/env python3
import feedparser
import requests
import sys

def test_feed(url):
    print(f"Testing feed: {url}")
    
    try:
        # Test with requests
        print("Testing with requests...")
        response = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        print(f"Status code: {response.status_code}")
        print(f"Content type: {response.headers.get('content-type', 'Unknown')}")
        print(f"Content length: {len(response.text)}")
        
        if response.status_code == 200:
            print(f"First 300 chars:\n{response.text[:300]}")
            
        # Test with feedparser
        print("\nTesting with feedparser...")
        d = feedparser.parse(url)
        
        print(f"Feedparser bozo: {d.bozo}")
        if d.bozo:
            print(f"Bozo exception: {d.bozo_exception}")
            
        print(f"Feed keys: {list(d.feed.keys()) if hasattr(d, 'feed') else 'No feed'}")
        print(f"Feed title: {getattr(d.feed, 'title', 'No title')}")
        print(f"Number of entries: {len(d.entries)}")
        
        if d.entries:
            first = d.entries[0]
            print(f"\nFirst entry:")
            print(f"  Title: {first.get('title', 'No title')}")
            print(f"  Published: {first.get('published', 'No date')}")
            print(f"  Link: {first.get('link', 'No link')}")
            print(f"  Summary length: {len(first.get('summary', ''))}")
        
        return len(d.entries) > 0
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_feed("https://promisingparagraphs.substack.com/feed")
    sys.exit(0 if success else 1)
