import requests
from bs4 import BeautifulSoup
import re
import time


def get_twitter_handle_from_twitch(username):
    """
    Scrapes a Twitch channel about page and extracts the Twitter handle.
    
    Args:
        username: Twitch username (e.g., 'TheoryForge')
    
    Returns:
        Twitter handle (without @) or None if not found
    """
    url = f"https://www.twitch.tv/{username}/about"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Method 1: Look for links with href containing twitter.com
        # Based on the image, the structure is <a href="https://twitter.com/TheoryForge">
        twitter_links = soup.find_all('a', href=re.compile(r'twitter\.com/([^/?]+)'))
        
        for link in twitter_links:
            href = link.get('href', '')
            # Extract username from URL
            match = re.search(r'twitter\.com/([^/?]+)', href)
            if match:
                handle = match.group(1)
                # Remove @ if present
                handle = handle.lstrip('@')
                return handle
        
        # Method 2: Look for social-media-link class elements
        social_links = soup.find_all('a', class_=re.compile(r'social-media-link|tw-link'))
        for link in social_links:
            href = link.get('href', '')
            if 'twitter.com' in href:
                match = re.search(r'twitter\.com/([^/?]+)', href)
                if match:
                    handle = match.group(1)
                    handle = handle.lstrip('@')
                    return handle
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return None


def scrape_twitch_usernames(csv_usernames, use_selenium=True):
    """
    Scrapes Twitter handles for a list of Twitch usernames.
    
    Args:
        csv_usernames: List of Twitch usernames
        use_selenium: If True, use Selenium for JavaScript-rendered content (default True)
    
    Returns:
        List of dicts with 'twitch_username' and 'twitter_handle' keys
    """
    results = []
    
    for username in csv_usernames:
        username = username.strip()
        if not username:
            continue
            
        print(f"Scraping {username}...")
        
        # Twitch pages are JavaScript-rendered, so we need Selenium
        handle = get_twitter_handle_with_selenium(username)
        
        results.append({
            'twitch_username': username,
            'twitter_handle': handle if handle else 'Not found'
        })
        
        # Be respectful with rate limiting
        time.sleep(1)
    
    return results


def get_twitter_handle_with_selenium(username):
    """
    Alternative scraper using Selenium for JavaScript-rendered pages.
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        import re
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            url = f"https://www.twitch.tv/{username}/about"
            driver.get(url)
            
            # Wait for page to load (wait for social media links or a timeout)
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                # Additional wait for dynamic content
                time.sleep(3)
            except:
                pass
            
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Method 1: Look for links with href containing twitter.com
            twitter_links = soup.find_all('a', href=re.compile(r'twitter\.com/([^/?]+)'))
            
            for link in twitter_links:
                href = link.get('href', '')
                match = re.search(r'twitter\.com/([^/?]+)', href)
                if match:
                    handle = match.group(1)
                    handle = handle.lstrip('@')
                    return handle
            
            # Method 2: Look for social-media-link class elements
            social_links = soup.find_all('a', class_=re.compile(r'social-media-link|tw-link'))
            for link in social_links:
                href = link.get('href', '')
                if 'twitter.com' in href:
                    match = re.search(r'twitter\.com/([^/?]+)', href)
                    if match:
                        handle = match.group(1)
                        handle = handle.lstrip('@')
                        return handle
            
            return None
            
        finally:
            driver.quit()
            
    except ImportError:
        print("Selenium not available, falling back to requests")
        return get_twitter_handle_from_twitch(username)
    except Exception as e:
        print(f"Selenium error: {e}")
        return None

