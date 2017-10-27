import pandas as pd  
import urllib2
from bs4 import BeautifulSoup
from datetime import date, timedelta as td
import os
from collections import deque
import csv

proxy = urllib2.ProxyHandler({'http': 'http://satya:satya@172.16.115.42:3128',
                              'https': 'https://satya:satya@172.16.115.42:3128'})
auth = urllib2.HTTPBasicAuthHandler()
opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
urllib2.install_opener(opener)

def contentcrawler(link,date,uid):
    try:
        page = urllib2.urlopen(link)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Unable to Access SubLink "+str(uid))
    else:
        try:
            soup = BeautifulSoup(page)
            
            newshead=soup.find('article',{"class":'heading1'}).text
            
            textsoup = soup.find('article',{"itemprop":'articleBody'})
            newstext = textsoup.text
            
            imagesoup = soup.find('section',{"class":'highlight clearfix'}).find('img')
            imagelink = 'http://www.thehindu.com/archive/'+ imagesoup['src']
            image = urllib2.urlopen(imagelink).read()
            
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("Error in Scraping SubLink "+str(uid))
        else:
            
            imagedir = os.getcwd()+'/hindu_image/'
            imagename = imagedir+ str(uid)+'.jpg'
            f = open(imagename,'wb')
            f.write(image)
            f.close()
            
            outputfile='hindu_news.csv'
            df=pd.DataFrame([[uid,newshead,newstext,date,link,imagelink]])
            with open(outputfile, 'a') as f:
                (df).to_csv(f, header=False,index=False,encoding='utf-8')
            
            print("Successfully Scraped "+str(uid))

def get_last_row(filename):
    with open(filename, 'r') as f:
        lastrow = deque(csv.reader(f), 1)[0]
    return lastrow[0]
    
def linkscrawler(link,date,lastuid):
    newslinks = []
    try:
		page = urllib2.urlopen(link)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Unable to Access MainLink "+str(date))
    else:
        try:
            soup = BeautifulSoup(page)
            linksoups = soup.find_all('td',{"align":"left"})
            for linksoup in linksoups:
                for link in linksoup.find_all('a', href=True):
                    templink=link['href']
                    if (templink.find('http://www.thehindu.com/archive//')==-1):
                        templink='http://www.thehindu.com/archive//'+templink
                    newslinks+=[templink]
            newslinks=newslinks[:100]+newslinks[500:]
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("Error in Scraping MainLink "+str(date))
    
    count=1
    for link in newslinks:
        uid='T'+date.isoformat().replace('-','')[2:]+"%04d" % count
        if uid>lastuid:
        	contentcrawler(link,date,uid)
        count+=1

def linksgenerator(startdate,enddate,lastuid):
    delta = enddate-startdate
    basedate = date(1900,1,1)
    for i in range(delta.days + 1):
        currdate = startdate + td(days=i)
        mainlink = 'http://www.thehindu.com/archive/'+str(currdate.year)+'/'+str(currdate.month)+'/'+str(currdate.day)+'/archivelist/year-'+str(currdate.year)+',month-'+str(currdate.month)+',starttime-'+str((currdate-basedate).days+2)+'.cms'
        linkscrawler(mainlink,currdate,lastuid)

def main():
    if not os.path.exists(os.getcwd()+'/hindu_news.csv'):
        outputfile='hindu_news.csv'
        df=pd.DataFrame([["Uid","Headline","Body","Date","NewsLink","ImageLink"]])
        df.to_csv(outputfile,header=False,index=False)
        lastuid = 'T0000000000'

    else:
        lastuid = get_last_row('hindu_news.csv')
    
    startdate = date(2016,03,15)
    enddate = date(2017,03,14)

    linksgenerator(startdate,enddate,lastuid)

main()