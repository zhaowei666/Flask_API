import urllib2
import re
import HTMLParser
import json
import os



imdb_address = 'http://www.imdb.com/list/ls000029269/'
data_address = os.getcwd() + '/data_collection/quotes.json'
pars = HTMLParser.HTMLParser()


def main():
    response = urllib2.urlopen(imdb_address)
    html = response.read()
    pattern = "<p>(&quot;|&#39;)(.*)(&quot;|&#39;)"
    quote_result = re.findall(pattern, html)
    pattern = '>(.*)</a>\n    <span class="lister-item-year text-muted unbold">\((\d{4})\)</span>'
    movie_result = re.findall(pattern, html)
    quotes = []
    if len(quote_result) != len(movie_result):
        raise ValueError('Inconsistent number of movie and quotes')
    for i in range(len(quote_result)):
        try:
            quote = pars.unescape(quote_result[i][1])
            movie_name = pars.unescape(movie_result[i][0])
            movie_year = pars.unescape(movie_result[i][1])
        except:
            continue
        quotes.append({
            'quote': quote,
            'movie_name': movie_name,
            'movie_year': movie_year
        })
    with open(data_address, 'w') as f:
        json.dump(quotes, f, indent=4)


if __name__ == '__main__':
    main()

