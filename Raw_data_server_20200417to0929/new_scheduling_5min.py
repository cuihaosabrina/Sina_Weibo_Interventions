import re
import schedule
from datetime import datetime
import requests
import time
import urllib.request #导入urllib.request库
import urllib.parse
from lxml import etree
import urllib
import pandas as pd
import html5lib
import socket
import http.client

#b = str(input("请输入："))   #提示用户输入信息，并强制类型转换为字符串型
schedule.clear()

def weibo() :
    #user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  #imitate browser
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15'
    headers = { 'User-Agent' : user_agent }
    url = 'https://s.weibo.com/top/summary?'
    try:
        req = urllib.request.Request(url, headers = headers)
        a=urllib.request.urlopen(req, timeout=30) #timeout 设置最长请求时间，如果超时，停止请求
        #a = urllib.urlopen(req)
        #urllib2中的Request和urlopen都合并到urllib.request下
        html = a.read()  #读取网页源码
        html = html.decode("utf-8")  #解码为unicode码
        # print(html)                #打印网页源码
        tree = etree.HTML(html)
        list02 = tree.xpath(u'//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[@class="td-02"]')
        list03 = tree.xpath(u'//*[@id="pl_top_realtimehot"]/table/tbody/tr/td[@class="td-03"]')

        prefix = 'https://s.weibo.com'  # 微博域名
        #weiboSummary = open("微博热搜.txt", 'w')  #打开并写入文件
        #weiboSummary=open(str(datetime.now())+"weibo.txt", 'w')
        weiboSummary=open(str(time.strftime('%Y%m%d%H%M%S',time.localtime()))+"weibo.txt", 'w')
        
        for index, item in enumerate(zip(list02, list03)): 
            
            if index > 0:
                
                a_element = item[0].xpath('.//a')[0]  #item[0] is the first element 
                title = a_element.text # 关键词
                #no need to get the link
                #href = urllib.parse.unquote(a_element.attrib.get('href')) # 链接
                #href = href.replace("#", "%23") #此处是对链接中的#号做一个编码转换，否则无法跳转指定关键词链接
                hot = item[0].xpath('./span')[0].text #热度指数
                #write by myself
                #date = str(time.strftime('%Y%m%d%H%M%S',time.localtime())) 
                date = datetime.now().isoformat()
                
                if item[1].xpath('.//i')==[]:     #item[1] the second element in the zipped two lists
                    properties = "" # empty
                else:
                    properties = item[1].xpath('.//i')[0].text            

                line = str(index) + "\t" + title + "\t" + hot + "\t" + properties + "\t" + date + "\n"    # "\t" + prefix + href + "\n"
                print(line.replace("\n", ""))
                #if href.find("javascript:void(0)") != -1:
                    #line = str(index) + "\t" + title + "\t" + hot + "\t" + date +"\t"
                #写入文件
                weiboSummary.write(line)
               
            else:
                title = '排名\t关键词\t热度\t特征\t时间\n'     #\t链接\n'
                print(title.replace("\n",""))
                weiboSummary.write(title)

        weiboSummary.close() 

  
    except socket.timeout:
        print("The read operation timed out")
    except urllib.error.URLError:
        print('The handshake operation timed out')
    except http.client.RemoteDisconnected:
        print("Remote end closed connection without response")   
    except http.client.IncompleteRead:
        print("IncompleteRead")
    except NameError:
        print("Name Timeout is not defined")
    except error.URLError as err: 
        print("Error description:",err.reason)
    except error.HTTPError as err:
        print("Error description:", err.reason)
    except ConnectionError:
        print("Error description: Socket error timed out.")  

#调用方法
#weibo();
'''
def RunWeibo() :
	try: 
		weibo()
	except:
		weibo()
'''	
#RunWeibo() # it really runs!!!


#schedule.clear()
schedule.every(5).minutes.do(weibo)
#schedule.every().hour.do(weibo)
#schedule.every().day.at("23:59").do(weibo)
#schedule.every().seconds.do(weibo)

while 1:
    schedule.run_pending()
    time.sleep(1)
    
# To clear all functions
# schedule.clear() #!!!!!!!!!
