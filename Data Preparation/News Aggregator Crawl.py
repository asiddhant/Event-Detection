import pandas as pd  
import urllib2
from bs4 import BeautifulSoup

proxy = urllib2.ProxyHandler({'http': 'http://a.siddhant:iitGece@202.141.80.24:3128',
                              'https': 'https://a.siddhant:iitGece@202.141.80.24:3128'})
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)

def textscraper(soup,source):
    
    if source=="in.reuters.com":
        fulltext=soup.find('span',{"id":'article-text'}).text
    elif source=="www.nasdaq.com":
        fulltext=soup.find('div',{"id":"articleText"}).text
    elif source=="www.latimes.com":
        fulltext=soup.find('div',{"itemprop":"articleBody"}).text
    elif source=="www.washingtonpost.com":
        fulltext=soup.find('article',{"itemprop":'articleBody'}).text
    elif source=="www.forbes.com":
        fulltext=soup.find('div',{"class":'article-text clearfix'}).text
    elif source=="www.nydailynews.com":
        fulltext=soup.find('article',{"id":'ra-body'}).text
    elif source=="time.com":
        fulltext=soup.find('article',{"class":'row'}).text
        
    return fulltext

def imagescraper(soup,source):
    
    if source=="in.reuters.com":
        imagesoup = soup.find('div',{"class":'related-photo-container'}).find('img')
        imagelink = imagesoup['src']
        image = urllib2.urlopen(imagelink).read()
    elif source=="www.nasdaq.com":
        imagesoup = soup.find('div',{"class":"article-image-wrap"}).find('img')
        imagelink = imagesoup['src']
        image = urllib2.urlopen(imagelink).read()
    elif source=="www.latimes.com":
        imagesoup = soup.find('div',{"class":"trb_embed_media"}).find('img')
        imagelink = imagesoup['srcset'].split(',')[0].split(' ')[0]
        image = urllib2.urlopen(imagelink).read()
    elif source=="www.forbes.com":
        imagesoup = soup.find('figure',{"class":"article-featured-image ratio16x9  ng-scope"}).find('img')
        imagelink = imagesoup['src']
        image = urllib2.urlopen(imagelink).read()
    elif source=="www.nydailynews.com":
        imagesoup = soup.find('figure',{"class":"ra-figure"}).find('img')
        imagelink = imagesoup['srcset'].split(',')[0].split(' ')[0]
        image = urllib2.urlopen(imagelink).read()
    elif source=="time.com":
        imagesoup = soup.find('picture').find('img')
        imagelink = imagesoup['src']
        image = urllib2.urlopen(imagelink).read()
        
    return image
        
def textcrawl(link,source):
    try:
        page = urllib2.urlopen(link)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Unable to Access URL")
        newstext="Unable to Access URL"
    else:
        try:
            soup = BeautifulSoup(page)
            newstext=textscraper(soup,source)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("Error in Scraping")
            newstext="Error in Scraping"
    return newstext

def imagecrawl(link,source):
    try:
        page = urllib2.urlopen(link)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Unable to Access URL")
        image="Unable to Access URL"
    else:
        try:
            soup = BeautifulSoup(page)
            image=imagescraper(soup,source)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("Error in Scraping")
            image="Error in Scraping"
    return image

def main():
    
    cur_set=1
    print 'Loading Data'
    newslinks=pd.read_csv('newslinks_set'+str(cur_set)+'.csv')
    print 'Data Load Complete'
    
    start=0
    end=newslinks.shape[0]    
    
    outputfile='newstexts_set'+str(cur_set)+'.csv'
    print 'Output File Created'
    df=pd.DataFrame([["ID","TITLE","FULLTEXT"]])
    df.to_csv(outputfile,header=False,index=False)

        
    print 'Crawling Started'
    for rowno in range(start,end):
        label=newslinks.ID[rowno]
        title=newslinks.TITLE[rowno]
        link=newslinks.URL[rowno]
        source=newslinks.HOSTNAME[rowno]
        newstext=textcrawl(link,source).encode('utf-8')
        
        if(newstext=="Unable to Access URL" or newstext=="Error in Scraping"):
            df=pd.DataFrame([[label,title,newstext]])
            with open(outputfile, 'a') as f:
                (df).to_csv(f, header=False,index=False)

        image = imagecrawl(link,source)
        if(image!="Unable to Access URL" and image!="Error in Scraping"):
            imagedir = os.getcwd()+'/images_set'+str(cur_set)+'/'
            imagename = imagedir+ str(label)+'.jpg'
            f = open(imagename,'wb')
            f.write(image)
            f.close()
        
        if rowno%10==9:
            print str((float(rowno+1)/(end-start))*100)+'% Complete'

main()

        



