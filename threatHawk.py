#!/usr/bin/env python
"""
SYNOPSIS
       __  __                    __  __  __               __  
      / /_/ /_  ________  ____ _/ /_/ / / /___ __      __/ /__
     / __/ __ \/ ___/ _ \/ __ `/ __/ /_/ / __ `/ | /| / / //_/
    / /_/ / / / /  /  __/ /_/ / /_/ __  / /_/ /| |/ |/ / ,<   
    \__/_/ /_/_/   \___/\__,_/\__/_/ /_/\__,_/ |__/|__/_/|_|  

    threatHawk.py [-h,--help] [--version] [-q, --query] [-s, --source] [-o, --output]

DESCRIPTION

    This is used to query a variety of sources on the Internet based upon a search
    string. The primary use of this tool is to assist in gathering threat intel on 
    your organization. This tool has the ability to query Twitter, Shodan, and Google, 
    with the hopes of adding more sources in the future. You will need a Twitter API 
    key in order to use the Twitter search feature of this. You will also need a Shodan 
    API key in order to use the Shodan feature of this tool. See the GitHub page for 
    details on obtaining the API keys, and where to place the API keys.

EXAMPLES

    python threatHawk.py -s all -q searchTerm
    python threatHawk.py -q searchTerm -s all
    python threatHawk.py -q "Search Term" --source=twitter
    python threatHawk.py --query=searchTerm -s google -o outputFileName.txt
    python threatHawk.py --query=searchTerm --source=all --output=outputFileName.txt

VALID SOURCES

    all - Searches all sources available for query specified
    twitter - Searches Twitter for query specified
    google - Searches Google for query specified
    shodan - Searches Shodan for query specified

AUTHOR

    Name: Brett Hawkins, @hawkbluedevil
    Date Created: 12/9/2015

LICENSE

    This script is in the public domain, free from copyrights or restrictions.

VERSION

    1.0 - Initial Release
"""

import sys
import os
import traceback
import optparse
import time
import urllib
import shodan
import re
import urllib, urllib2
from pygoogle import pygoogle
from twitter import *

# valid sources that can be used
validSources = ['all','twitter','google','shodan']

#=================================
# method to search twitter
#=================================
def searchTwitter(searchTerm):

    print ''
    print 'Searching Twitter...'
    print ''

    # create twitter object and perform search
    twitter=Twitter(auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))
    tweetQuery=twitter.search.tweets(q=searchTerm)

    print '*********************************'
    print 'Twitter Results'
    print '*********************************'
    print ''

    # display all results
    for result in tweetQuery["statuses"]:
        dateCreated = result["created_at"]
        user = result["user"]["screen_name"]
        result = result["text"]
        print 'Date: ' + dateCreated
        print 'User: ' + user
        print 'Tweet: ' + result.encode('ascii', 'ignore')
        print ''

    print ''
    print '*********************************'
    print ''

#=================================
# method to search shodan
#=================================
def searchShodan(searchTerm):

    print ''
    print 'Searching Shodan...'
    print ''

    #initialize Shodan object
    SHODAN_API_KEY = config['shodan_api_key']
    api = shodan.Shodan(SHODAN_API_KEY)

    try:
        # Search Shodan
        results = api.search(searchTerm)

        print '*********************************'
        print 'Shodan Results'
        print '*********************************'
        print ''

        # Show the results
        print 'Total Results Found: %s' % results['total']
        print ''
        for result in results['matches']:
            print 'IP: ' + result['ip_str']
            print result['data']
            print ''

        print ''
        print '*********************************'
        print ''
    
    except shodan.APIError, e:
            print 'Error: %s' % e

#=================================
# method to search google
#=================================
def searchGoogle(searchTerm): 

    print ''
    print 'Searching Google...'
    print ''

    googler = pygoogle(searchTerm) # initialize pygoogle object with search term
    googler.pages = 3 # set max pages

    print '*********************************'
    print 'Google Results'
    print '*********************************'
    print ''

    # display google results in a formatted way
    for keys, values in googler.search().items():
        theKey=keys.replace("&#39;","'")
        theKey=theKey.replace("&amp;","&")
        theValue=values.replace("&#39;","'")
        theValue=theValue.replace("&amp;","&")
        print 'Title: ' + (theKey.encode('ascii', 'ignore'))
        print 'URL: ' + (theValue.encode('ascii', 'ignore'))
        print ''
    print ''
    print '*********************************'
    print ''

#=================================
# Main method
#=================================
def main ():

    # define global variables
    global options, args, config

    # load config file
    config={}
    execfile('config.py', config)

    print ''
    print 'threatHawk searching.......'
    print '================================='
    print 'Search Term: ' + query
    print 'Source: ' + source
    print '================================='
    print ''

    # if user wants to search twitter
    if source=='twitter':
        searchTwitter(query)

    # if user wants to search google
    elif source=='google':
        searchGoogle(query)

    # if user wants to search shodan
    elif source=='shodan':
        searchShodan(query)

    # if user wants to search all sources
    elif source=='all':
        searchTwitter(query)
        searchGoogle(query)
        searchShodan(query)

if __name__ == '__main__':

    try:

        # define global variables
        global source, query

        # add all arguments and switches that can be given
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), usage=globals()['__doc__'], version='$Id$')
        parser.add_option('-q', '--query', dest='query',help='term to search')
        parser.add_option('-s', '--source', dest='source',help='source to search')
        parser.add_option('-o', '--output', dest='output',help='output file')
        (options, args) = parser.parse_args()
        
       
        # if query and source were not entered, display message and exit
        if options.query == None or options.source == None:
            print ''
            print 'Query and Source not entered. Please see help below.'
            print ''
            parser.print_help()
            sys.exit(0)

        # if valid source was not given, display message and exit
        if options.source.lower() not in validSources:
            print ''
            print 'Please give valid option for source.'
            print ''
            parser.print_help()
            sys.exit(0)

        # initialize searching source and query variables
        source=options.source.lower()
        query=options.query

        # if output file specified, print to output file
        if options.output:
            sys.stdout = open(options.output,'w')

        # proceed to main
        main()

    except KeyboardInterrupt, e: # Ctrl-C
        raise e

    except SystemExit, e: # sys.exit()
        raise e

    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
