
import sys, os, re
from HTMLParser import HTMLParser
import urllib, urllib2

pbs_url = 'http://www.pbs.org/newshour/bb/great-day-beach-stranded-great-white-shark/'

prefix = 'great-day-beach-stranded-great-white-shark'

start_transcript = 'TRANSCRIPT'
end_transcript = 'SHARE ON FACEBOOK'

in_file = prefix + '.html'
out_file = prefix + '.txt'

mp3_downloaded = prefix + '.mp3'

class MyHTMLParser(HTMLParser):
    #def __init__(self):
    #    pass

    def my_init(self):
        self.start = False
        self.end = False
        self.mp3 = []

    def handle_data(self, data):
        if re.search(start_transcript, data):
            self.start = True
        if re.search(end_transcript, data):
            self.end = True

        if self.start and not self.end:
            out_f.write("%s\r\n" % data.strip())


    def handle_starttag(self, tag, attrs):
        if (tag != 'a'):
            return

        for k, v in attrs:
            if (k == 'href'):
                if re.search('mp3', v):
                    self.mp3 = v;
                    print self.mp3

    def down_mp3(self):
        if self.mp3:
            urllib.urlretrieve(self.mp3, filename = mp3_downloaded)


parser = MyHTMLParser()
parser.my_init()

urllib.urlretrieve(pbs_url, in_file)

in_f = open(in_file, 'r')
out_f = open(out_file, 'w+')

in_html = in_f.read()

parser.feed(in_html)
parser.down_mp3()

in_f.close()
out_f.close()
