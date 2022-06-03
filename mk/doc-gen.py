#!/usr/bin/env python3

# Extract godoc HTML documentation for our packages,
# remove some nonsense, update some links and make it ready
# for inclusion in Confluent doc tree.


import subprocess
import re
from bs4 import BeautifulSoup


def convert_path(url, relative_path):
    basename = url.split('/')[-1]
    if basename == "style.css":
        basename = "styles.css"
    return f'{relative_path}/{basename}'


if __name__ == '__main__':

    # Use godoc client to extract our package docs
    html_in = subprocess.check_output(
        'godoc -url=/pkg/github.com/confluentinc/confluent-kafka-go/kafka ' +
        '| egrep -v "^using (GOPATH|module) mode"', shell=True)

    # Parse HTML
    soup = BeautifulSoup(html_in, 'html.parser')

    # Remove topbar (Blog, Search, etc)
    topbar = soup.find(id='topbar').decompose()

    # Remove "Subdirectories"
    soup.find(id='pkg-subdirectories').decompose()
    soup.find(attrs={'class': 'pkg-dir'}).decompose()
    for t in soup.find_all(href='#pkg-subdirectories'):
        t.decompose()

    # Use golang.org for external resources (such as CSS and JS)
    for t in soup.find_all(href=re.compile(r'^/')):
        t['href'] = 'https://go.dev/' + convert_path(t['href'], "css")

    for t in soup.find_all(src=re.compile(r'^/')):
        t['src'] = 'https://go.dev/' + convert_path(t['src'], "js")

    # Write updated HTML to stdout
    print(soup.prettify())
