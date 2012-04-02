#!/usr/bin/python
# File: crawler.py
# Description: simple web crawler that extract strings matching regex from
# web pages.
# Author: Jonathan Pelletier.
# Date: Sun Jan 15 03:09:41 EST 2012

# Licence: This software is free software etc etc, bla bla bla.
# Im not responsible for the things you do with this software.

import argparse
import sys
import urllib2
import urlparse
import re

from Queue import Queue
from BeautifulSoup import BeautifulSoup


# global variables
SCHEME = 0
NETLOC = 1
PATH = 2
PARAMS = 3
QUERY = 4
FRAGMENT = 5

IGNORE = ['jpg','css','js','flw','png','gif','jpeg','swf','flv','xml','pdf']

PREDEFINED_PATTERNS = {'email':r"""[\w.-]+@[\w-]+\.\w{2,4}"""}

def main():

    parser = argparse.ArgumentParser(description='extract pattern from the web')

    parser.add_argument(
            'root',
            help = 'root url from which the crawler starts working.',
            )

    parser.add_argument(
            'pattern',
            help = 'pattern (regex) that will be extracted from the web pages'\
                    'it can also be one of the predefined pattern (ex: email)'\
                    'names',
            )

    parser.add_argument(
            '-l',
            '--limit',
            help = 'maximum number of pages that can be explored during '\
                    'execution. Default is 1000.',
            type = int,
            default = 1000,
            )

    parser.add_argument(
            '-i',
            '--internal',
            help = 'specify weither the crawler will only explore pages that '\
                    'are within the root domain or is allowed to explore other '\
                    'domain as well. Default is True',
            action = 'store_true',
            default = True
            )

    parser.add_argument(
            '-o',
            '--output',
            help = 'name of a file that will store the matched results '\
                    '(1 per line).',
            nargs = '?',
            type = argparse.FileType('w'),
            default = sys.stdout
            )


    a = parser.parse_args()

    proto = 'http://'

    root = a.root

    # automatically prefix the root with http:// if its not in there already.
    if not proto in root:
        root = proto + root

    pattern = a.pattern
    limit = a.limit
    internal = a.internal
    output = a.output

    # set to a predefined pattern if need be.
    if pattern in PREDEFINED_PATTERNS.keys():
        pattern = PREDEFINED_PATTERNS[pattern]

    # the crawling function
    crawl(root, pattern, limit, internal, output)

    # close the output file
    output.close()
    return

def crawl(root, pattern, limit, internal, output):
    
    # ready up the data structures.
    # keep tracks of the url already visited.
    s = set()

    # data structure used for web graph traversal. Change this to a lifo 
    # to go from breadth first search to depth first search.
    q = Queue()

    # regular expression program used to match pattern.
    prog_pattern = re.compile(pattern)

    # enqueue the root url.
    q.put(root)

    # a set of already gathered patterns.
    gathered = set()

    # crawl the web.
    while not q.empty():

        # pop a url off the data structure.
        url = q.get()

        # if it's been explored, just continue.
        if url in s:
            continue

        extension = url.split('.')[-1]

        if extension in IGNORE:
            continue

        # get the new current root of the url.
        root = urlparse.urlparse(url).netloc

        # fetch the page.
        #print 'fetching: %s' % url
        try:
            datum = urllib2.urlopen(url).read()
        except:
            continue

        # extract the patterns from the datum.
        patterns = prog_pattern.findall(datum)

        # write them to file if there are some and they havent already been 
        # gathered.
        for p in patterns:
            if p in gathered:
                continue
            print_p = p.encode('utf-8')
            output.write(print_p + '\n')
            gathered.add(p)

        # extract all urls from the datum.
        urls = extract_url(datum, root)

        # if we need to limit them, filter them by making sure they contain the
        # root domain.
        if internal:
            urls = [ u for u in urls if root in u]

        # add all the discovered urls in the exploration queue.
        for item in urls:
            q.put(item)
        
        # mark the url as visited so it's not fetched again and again.
        s.add(url)

        # enforce the max number of links that can be explored.
        if len(s) >= limit:
            break

    return

def extract_url(datum, root):

    # declare the parser for the datum.
    try:
        parser = BeautifulSoup(datum)
    except:
        return []

    # define the return list.
    urls = []

    links = parser.findAll('a')

    for link in links:
        if not link.has_key('href'):
            continue
        url = link['href']
        
        url_atr = list(urlparse.urlparse(url))

        if not url_atr[NETLOC]:
            if './' in url_atr[PATH]:
                url_atr[PATH] = url_atr[PATH][2:]
            elif '../' in url:
                url_atr[PATH] = url_atr[PATH][3:]

            url_atr[SCHEME] = 'http'
            url_atr[NETLOC] = root

        urls.append(urlparse.urlunparse(url_atr))

    return urls

def sig_handler(signal, frame):
    sys.exit(0)


if __name__ == '__main__':
    main()

