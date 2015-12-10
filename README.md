# threatHawk

**Name:** Brett Hawkins, @hawkbluedevil

**Date Created:** 12/9/2015


#### Description:
The threatHawk tool is used to query a variety of sources on the Internet based upon a search string. The primary use of this tool is to assist in gathering threat intel on your organization. This tool has the ability to query Twitter, Shodan, and Google, with the hopes of adding more sources in the future. You will need a Twitter API key in order to use the Twitter search feature of this. You will also need a Shodan API key in order to use the Shodan feature of this tool. See the Prerequisites section for details on obtaining the API keys, and where to place the API keys.

#### Usage:
- threatHawk.py [-h,--help] [--version] [-q, --query] [-s, --source] [-o, --output]

#### Examples:
- python threatHawk.py -s all -q searchTerm
- python threatHawk.py -q searchTerm -s all
- python threatHawk.py -q "Search Term" --source=twitter
- python threatHawk.py --query=searchTerm -s google -o outputFileName.txt
- python threatHawk.py --query=searchTerm --source=all --output=outputFileName.txt

#### Valid Sources:
- **all:** Searches all sources available for query specified
- **twitter:** Searches Twitter for query specified
- **google:** Searches Google for query specified
- **shodan:** Searches Shodan for query specified

#### Supported Platforms:
- Linux
- Mac OS X

#### Prerequisites:
- Python 2.7+

- Internet connection

- Register for Twitter API Key:
    1. Go to https://apps.twitter.com/app/new
    2. Login with your Twitter account and create an application
    3. You will can then view your API keys in your Twitter account settings.
    4. You will need the below API keys, and place them in the config.py file included with     this tool.
        - **consumer_key**
        - **consumer_secret**
        - **access_key**
        - **access_secret**

- Register for Shodan API Key:
    1. Create a Shodan account at https://developer.shodan.io/
    2. You will then find your API key in your account settings. Add this key in the            config.py file.

- Install Shodan Python API: **sudo easy_install shodan**

- Install PyGoogle Python Module: **sudo pip install pygoogle-simple**

- Install Twitter Python API:
    1. wget https://pypi.python.org/packages/source/t/twitter/twitter-1.12.1.tar.gz
    2. tar -xzf twitter*.tar.gz
    3. cd twitter*
    4. sudo python setup.py build; sudo python setup.py install
