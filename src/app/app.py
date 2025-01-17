from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for Angular frontend

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_url(self, url, selectors=None):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if not selectors:
                # Default scraping behavior
                data = {
                    'title': soup.title.string if soup.title else '',
                    'links': [{'text': a.text, 'href': a['href']} 
                             for a in soup.find_all('a', href=True)],
                    'text_content': soup.get_text(separator=' ', strip=True)
                }
            else:
                # Custom selector-based scraping
                data = {}
                for key, selector in selectors.items():
                    elements = soup.select(selector)
                    data[key] = [elem.get_text(strip=True) for elem in elements]
            
            return {'success': True, 'data': data}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

scraper = WebScraper()

@app.route('/api/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')
    selectors = data.get('selectors')
    
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'}), 400
        
    result = scraper.scrape_url(url, selectors)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)