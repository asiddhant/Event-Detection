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

def contentcrawler(link,uid):
    try:
        page = urllib2.urlopen(link)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print("Unable to Access SubLink "+str(uid))
    else:
        try:
            soup = BeautifulSoup(page)
            
            newshead=soup.find('div',{"class":'main-text'}).text
            
            textsoup = soup.find('div',{"class":'article-text clearfix'})
            newstext = textsoup.text
            
            imagesoup = soup.find('div',{"class":'related-photo-container'}).find('img')
            imagelink = imagesoup['src']
            image = urllib2.urlopen(imagelink).read()

            datesoup = soup.find('div',{"class":'dateModified'})['content']
            currdate = date(int(datesoup[:4]),int(datesoup[6:7]),int(datesoup[9:10]))
            
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("Error in Scraping SubLink "+str(uid))
        else:
            
            imagedir = os.getcwd()+'/ie_image/'
            imagename = imagedir+ str(uid)+'.jpg'
            f = open(imagename,'wb')
            f.write(image)
            f.close()
            
            outputfile='ie_news.csv'
            df=pd.DataFrame([[uid,newshead,newstext,currdate,link,imagelink]])
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
            linksoup=soup.find('div',{"id":'insidemidpanel'})
            for link in linksoup.find_all('a', href=True):
                templink=link['href']
                if (templink.find('http://archive.indianexpress.com/')==0):
                    newslinks+=[templink]
            
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            print("Error in Scraping MainLink "+str(date))
    
    count=1
    for link in newslinks:
        uid='N'+str(date[0])+"%02d" % date[1]+"%05d" % count
        if uid>lastuid:
            contentcrawler(link,uid)
        count+=1
    

def linksgenerator(startdate,enddate,lastuid):
    
    startmonth = [startdate.month]+[1]*(enddate.year-startdate.year)
    endmonth = [12]*(enddate.year-startdate.year)+[enddate.month]

    index=0
    for year in range(startdate.year,enddate.year+1):
        for month in range(startmonth[index],endmonth[index]+1):
            mainlink='http://http://archive.indianexpress.com/'+str(year)+'-'+str("%02d" % month)+'.html'
            linkscrawler(mainlink,[year,month],lastuid)
        index+=1

def main():
    
    if not os.path.exists(os.getcwd()+'/ie_news.csv'):
        outputfile='ie_news.csv'
        df=pd.DataFrame([["Uid","Headline","Body","Date","NewsLink","ImageLink"]])
        df.to_csv(outputfile,header=False,index=False)
        lastuid = 'IE00000000000'
    else:
        lastuid = get_last_row('ie_news.csv')
    
    startdate = date(2016,03,15)
    enddate = date(2017,03,14)
    linksgenerator(startdate,enddate,lastuid)

main()