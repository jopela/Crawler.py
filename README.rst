================================================================================
crawler.py user manual
================================================================================

Installation
================================================================================
Before running the script, make sure you have the following packages 
accessible from your python path:

1. argparse
2. urllib2
3. urlparse
4. BeautifulSoup

You can install them using easy_install at your command prompt, ex:

    easy_install BeautifulSoup

You should then be ready to go!


Usage
================================================================================
Usage details are available in the standard help and can be accessed with:
    
    ./crawler.py --help

Usually you will use the script like this:

    ./crawler.py www.polymtl.ca email

Replace www.polymtl.ca and email to suit your needs.

Known issues
================================================================================
The script does not recognize KeyboardInterrupt, so it needs to be terminated
using the kill command. Other than that, seems to work fine. Have fun !

Contact
================================================================================
jonathan.pelletier1@gmail.com

