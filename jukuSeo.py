import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

def analyze_page_content(content):
    soup = BeautifulSoup(content, 'html.parser')

    title = soup.find('title').text.strip() if soup.find('title') else 'No title found'
    meta_description = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_description.get('content').strip() if meta_description else 'No meta description found'

    heading_tags = [soup.find(f'h{i}').text.strip() for i in range(1, 7) if soup.find(f'h{i}')]

    return {
        'Title': title,
        'Meta Description': meta_description,
        'Heading Tags': heading_tags
    }

if __name__ == '__main__':
    url = input("Enter the URL to analyze: ")
    parsed_url = urlparse(url)

    if parsed_url.scheme and parsed_url.netloc:
        page_content = get_page_content(url)
        if page_content:
            analysis = analyze_page_content(page_content)
            print("\nAnalysis Results:")
            for key, value in analysis.items():
                print(f"{key}: {value}")
        else:
            print("Failed to retrieve page content.")
    else:
        print("Invalid URL format.")
