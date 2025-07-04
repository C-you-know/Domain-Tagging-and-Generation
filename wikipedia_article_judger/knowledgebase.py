import requests
from bs4 import BeautifulSoup, SoupStrainer
from typing import List,Dict
from . import paragraphs as pg
from urllib.parse import urljoin
from collections import Counter

def search_wikipedia_pages(keywords, lang='en'):
    url = f"https://{lang}.wikipedia.org/w/api.php"
    user_agent = "MyWikipediaSearchScript/1.0 (https://example.com; myemail@example.com)"
    headers = {
        "User-Agent": user_agent
    }
    results = {}
    for keyword in keywords:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': keyword,
            'srlimit': 5
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            search_results = [
                {
                    'title': page['title'],
                    'url': f"https://{lang}.wikipedia.org/wiki/{page['title'].replace(' ', '_')}"
                }
                for page in data['query']['search']
            ]
            results[keyword] = search_results
        else:
            results[keyword] = []

    return results

def extract_unique_url(relevant_pages:dict[str,str]) -> list[str]:
    url_set = set()

    for keyword, entries in relevant_pages.items():
        for entry in entries:
            url_set.add(entry['url'])

    return list(url_set)

def fetch_content(urls):
    content_dict = {}

    for url in urls:
        try:
            strainer = SoupStrainer(['title', 'h1', 'p'])
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser', parse_only=strainer)
            
            title = soup.find('title').get_text() if soup.find('title') else 'No title'
            subtitle = soup.find('h1').get_text() if soup.find('h1') else 'No subtitle'
            paragraphs = [pg.clean(para.get_text()) for para in soup.find_all('p')]

            content_dict[url] = {
                'title': title,
                'subtitle': subtitle,
                'paragraphs': paragraphs
            }

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            content_dict[url] = {
                'title': 'Error',
                'subtitle': 'Error',
                'paragraphs': []
            }

    return content_dict

def get_summary_valid_hrefs(url: str) -> List[str]:
    """
    Fetches all valid href links from the first two paragraphs, summary section,
    or everything before the first subheading on a given Wikipedia page.

    Parameters:
        url (str): The URL to scrape for href links.

    Returns:
        List[str]: A list of valid href links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.find(id="mw-content-text")
        if not content:
            print(f"Could not find content section in URL: {url}")
            return []

        paragraphs = content.find_all('p', limit=2)  
        first_heading = content.find('h2')  

        valid_content = []
        for element in content.children:
            if element == first_heading:
                break
            if element.name == 'p':
                valid_content.append(element)

        combined_content = paragraphs + valid_content

        hrefs = []
        for section in combined_content:
            hrefs.extend(a['href'] for a in section.find_all('a', href=True))

        valid_hrefs = ["https://en.wikipedia.org"+href for href in hrefs if '#' not in href]

        return valid_hrefs
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing URL '{url}': {e}")
        return []
    
def get_global_valid_hrefs(url: str) -> List[str]:
    """
    Fetches all valid internal Wikipedia href links from the given Wikipedia page,
    excluding references, related sections, and other external links.

    Parameters:
        url (str): The URL to scrape for href links.

    Returns:
        List[str]: A list of valid internal Wikipedia href links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.find(id="mw-content-text")
        if not content:
            print(f"Could not find content section in URL: {url}")
            return []

        hrefs = []
        for a_tag in content.find_all('a', href=True):
            href = a_tag['href']
            
            if href.startswith('/wiki/') and not href.startswith(('#', '/wiki/Help:', '/wiki/Wikipedia:')):
                full_url = "https://en.wikipedia.org" + href if not href.startswith('http') else href
                hrefs.append(full_url)

        return hrefs
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while processing URL '{url}': {e}")
        return []

def get_hrefs_from_urls(urls: List[str], verbose:bool = False, global_:bool = False) -> Dict[str, List[str]]:
    """
    Fetches valid href links from multiple URLs and returns them in a dictionary.

    Parameters:
        urls (List[str]): A list of URLs to scrape for href links.

    Returns:
        Dict[str, List[str]]: A dictionary with the URL as the key and a list of valid href links as the value.
    """
    if not isinstance(urls, list) or not all(isinstance(url, str) for url in urls):
        raise ValueError("The `urls` parameter must be a list of strings.")

    hrefs_ = []
    for url in urls:
        if verbose:
            print(f"Processing URL: {url}")

        if global_:
            valid_hrefs = get_global_valid_hrefs(url)  
        else:
            valid_hrefs = get_summary_valid_hrefs(url)  
            
        hrefs_.extend(valid_hrefs)

    return hrefs_

def tests(urls: List[str]) -> None:
    """
    Fetches and prints the first two valid href names from the summary section of each Wikipedia page in a list of URLs.

    Parameters:
        urls (List[str]): A list of URLs to scrape for href names.

    Returns:
        None
    """
    for url in set(urls):
        try:
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            content = soup.find(id="mw-content-text")
            if not content:
                print(f"Could not find content section in URL: {url}")
                continue

            paragraphs = content.find_all('p', limit=2)
            
            hrefs = []
            for section in paragraphs:
                hrefs.extend(a['href'] for a in section.find_all('a', href=True))

            # Filter valid href links and extract names
            valid_hrefs = [
    href.split('/')[-1].replace('_', ' ')
    for href in hrefs
    if (
        '#' not in href and
        ':' not in href and
        not href.endswith(('.ogg', '.mp3', '.jpg', '.png', '.svg', '.jpeg')) and
        href.startswith('/wiki/'))
    ]


            # Get the first two unique names
            filtered_names = []
            for name in valid_hrefs:
                if name not in filtered_names:
                    filtered_names.append(name)
                if len(filtered_names) == 2:
                    break

            # Print the names
            print(f"URL: {url}")
            if filtered_names:
                print("First two names:", filtered_names)
            else:
                print("No valid names found.")
            print()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while processing URL '{url}': {e}")

