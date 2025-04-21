import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from cachetools import TTLCache

# Cache setup (max size 100, TTL 600 seconds = 10 minutes)
cache = TTLCache(maxsize=100, ttl=600)

base_url = 'https://gogoanime3.co'
ua = UserAgent()

# Reuse session for requests
session = requests.Session()
session.headers.update({"User-Agent": ua.random})

# Reusable function to fetch and parse a page
def fetch_page(url):
    if url in cache:
        return cache[url]  # Return cached page

    try:
        res = session.get(url)
        res.raise_for_status()  # This will raise an exception for HTTP errors (e.g., 404, 500)
        soup = BeautifulSoup(res.text, 'html.parser')
        cache[url] = soup  # Cache the parsed page
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {url}: {e}")
        return None

def search_anime(query):
    url = f"{base_url}/search.html?keyword={query}"
    soup = fetch_page(url)
    if not soup:
        return []

    results = []
    for a in soup.select('.last_episodes li'):
        title = a.select_one('p.name a').text
        slug = a.select_one('p.name a')['href'].split('/')[-1]
        image = a.select_one('div.img a img')['src']
        results.append({"title": title, "slug": slug, "image": image})
    return results

def get_episodes(slug):
    url = f"{base_url}/category/{slug}"
    soup = fetch_page(url)
    if not soup:
        return []

    ep_range = soup.select_one('#episode_page li:last-child a')
    if not ep_range:
        return []

    ep_max = int(ep_range['ep_end'])
    return list(range(1, ep_max + 1))

def get_stream_url(episode_id):
    watch_url = f"{base_url}/{episode_id}"
    soup = fetch_page(watch_url)
    if not soup:
        return None

    iframe = soup.find('iframe')
    return iframe['src'] if iframe else None
