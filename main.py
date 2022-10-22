import argparse
import requests
from requests import HTTPError
from bs4 import BeautifulSoup
import os
from datetime import datetime, timezone


class ProcessMetadata():

    def __init__(self, url_content):
        self.url_content = url_content

    def get_img_count(self, url_content):
        soup = BeautifulSoup(url_content, "html.parser")
        return len(soup.find_all('img'))
    
    def get_url_count(self, url_content):
        soup = BeautifulSoup(url_content, "html.parser")
        return len(soup.find_all('a'))

    

class getMetadata():

    def __init__(self, args):
        self.args = args

    def extract_informations(self, args):
        #url path

        site_name = args.metadata.split('/')[-1]
        url_path = args.metadata.split('//')[-1] + ".html"


        print("site: {}".format(site_name))
        with open(url_path, 'rb') as f:
            #process metadata 
            contents = f.read()
            process = ProcessMetadata(contents)
            print("num_links:", process.get_img_count(contents))
            print("images:",process.get_url_count(contents))
            statbuf = os.stat(url_path)
            modified = datetime.fromtimestamp(statbuf.st_mtime, tz=timezone.utc).strftime('%a %b %d %Y %H:%M UTC')
            print("last_fetch: {}".format(modified))





class downloadHTML():

    def __init__(self, args):
        self.args = args

    def download(self, args):

        # get the list of urls 
        list_of_urls = args.url

        #iterate over each url 
        for each_url in list_of_urls:

            try: 
                #opening with GET method
                response = requests.get(each_url, stream = True)
                # print(response.headers)
                # webContent = response.content
                # file name should be in googl.com.html format 
                filename = each_url.split('//')[-1] + ".html"
                # print(filename)
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=128):
                        if chunk:
                            f.write(chunk)

                print("Web contents of URL: {} Saved in the current directory".format(each_url))
                
            except HTTPError as e:
                print(e)




def main():

    parser = argparse.ArgumentParser(description='enter --url or --metadata command foloowed by url name')
    parser.add_argument('--url', nargs='+', help='Enter the url')
    parser.add_argument('--metadata', help='Enter url name to get the metadata')
    args = parser.parse_args()

    if args.url:
        ob  = downloadHTML(args)
        ob.download(args)
    
    elif args.metadata:
        ob = getMetadata(args)
        ob.extract_informations(args)

    else:
        print("Please enter a valid command!")


if __name__=="__main__":
    main()