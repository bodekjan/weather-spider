from bs4 import BeautifulSoup
import requests
import json



file = open("cityid.txt",'r')
wFile=open('result.txt','a')

while True:
    line = file.readline()
    if not line:
        break
    srts = line.split('=')
    try:
        cityid = srts[0] #这是每一行的cityid值
        url = 'http://www.weather.com.cn/weather1d/'+cityid+'.shtml'
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')
        body = soup.body
        data = body.find('p',{'class':'tem'})
        tem = data.find('span').string #这是当前温度，如需要更多的数据的话，可以按这种方法找到对应的html标签就行，用标签的class或id来定位
        url2 = "http://api.map.baidu.com/geocoder/v2/?output=json&address="+srts[1]+"&city="+srts[1]+"&ak=你的baidu map api key"
        resp2 = requests.get(url2)
        resp2.encoding = 'utf-8'
        baiduJson = json.loads(resp2.text)
        if(baiduJson['status']!=0):
            continue
        bLong = baiduJson['result']['location']['lng'] # 经度
        bLat = baiduJson['result']['location']['lat'] # 纬度
        wFile.write(srts[1].replace('\n','')+','+tem+','+str(bLong)+','+str(bLat)+'\n')
        print('已获取'+srts[1].replace('\n','')+'的数据\n')
    except Exception as err:
        print('ERR :: 获取'+srts[1].replace('\n','')+'的数据时出错，一略过\n')
        continue
wFile.close()
file.close()
print('!!!!!!!!!!!! 结束 !!!!!!!!!!!!!!!')
