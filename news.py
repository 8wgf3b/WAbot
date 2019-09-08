from newsapi import NewsApiClient
import os
newsapi = NewsApiClient(api_key=os.environ.get('NEWS_API_KEY', ''))

def headlines(terms = None):
    top_headlines = newsapi.get_top_headlines(q = terms)
    articles =top_headlines['articles']
    s = 'For refined news use /news <search terms>\n\n News about ' + terms+ '\n\n'
    for art in articles:
        s += art['title'] + '\n'
        s += art['url'] + '\n'
        s += '\n\n'
    return s

if __name__ == '__main__':
    print(headlines('boris johnson'))


#    sources = newsapi.get_sources()
