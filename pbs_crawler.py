
import sys, os, re
import urllib, urllib2
from HTMLParser import HTMLParser
from ConfigParser import SafeConfigParser

class PbsHTMLParser(HTMLParser):
    def init(self, url, prefix):
        self.start_transcript = 'TRANSCRIPT'
        self.end_transcript = 'SHARE ON FACEBOOK'
        self.prefix = prefix
        self.in_file = self.prefix + '.html'
        self.out_file = self.prefix + '.txt'
        self.mp3_downloaded = self.prefix + '.mp3'
        self.pbs_url = url

        self.start = False
        self.end = False
        self.mp3 = []

    def handle_data(self, data):
        if re.search(self.start_transcript, data):
            self.start = True
        if re.search(self.end_transcript, data):
            self.end = True

        if self.start and not self.end:
            self.out_f.write("%s\r\n" % data.strip())

    def handle_starttag(self, tag, attrs):
        if (tag != 'a'):
            return

        for k, v in attrs:
            if (k == 'href'):
                if re.search('mp3', v):
                    self.mp3 = v;

    def down_mp3(self):
        print 'Downloading ' + self.mp3_downloaded + ' ...... ',
        if self.mp3:
            urllib.urlretrieve(self.mp3, filename = self.mp3_downloaded)
        print 'Done'

    def load(self):
        urllib.urlretrieve(self.pbs_url, self.in_file)

        self.in_f = open(self.in_file, 'r')
        self.out_f = open(self.out_file, 'w+')

        self.in_html = self.in_f.read()

        self.feed(self.in_html)
        self.down_mp3()

        self.in_f.close()
        self.out_f.close()
      
        
class PbsCrawler():
    def run(self):
        config_parser = SafeConfigParser()
        config_parser.read('pbs.ini')
        str_pbs_url = config_parser.get('pbs_source', 'pbs_url')
        list_pbs_url = eval(str_pbs_url)
        for url in list_pbs_url:
            prefix = url.split('/')[-2]
            pbs_parser = PbsHTMLParser()
            pbs_parser.init(url, prefix)
            pbs_parser.load()

if __name__ == '__main__':
    PbsCrawler().run()
