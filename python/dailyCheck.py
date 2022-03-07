import requests
import json
import time

print("自动打卡系统运行中......")
cookie = ["873cc495-485f-4fbe-909e-5bb3e1781c0d","",""]
namelist = ["刘柘","",""]

#打卡状态查询 方法GET
url1 = "https://jzsz.uestc.edu.cn/wxvacation/api/epidemic/checkRegisterNew"
#打卡信息上报 方法POST
url2 = "https://jzsz.uestc.edu.cn/wxvacation/api/epidemic/monitorRegisterForReturned"
#共用请求头
headers = {
	"Host":"jzsz.uestc.edu.cn",
    "Connection":"keep-alive",
    "Cookie":"",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "X-Tag":"flyio",
    "content-type":"application/json",
    "encode":"false",
    "Referer":"https://servicewechat.com/wx521c0c16b77041a0/28/page-frame.html",
    "Accept-Encoding":"gzip, deflate, br"
	}
#二级token获取 方法GET
url3 = "https://jzsz.uestc.edu.cn/wxvacation/api/user/getLoginUser?sessionId=" + cookie[0]
req3 = requests.get(url3,headers=headers)
cookie[0] = req3.headers["Set-Cookie"]
#自动填写数据
post_data = {"healthCondition":"正常","todayMorningTemperature":"36°C~36.5°C","yesterdayEveningTemperature":"36°C~36.5°C","yesterdayMiddayTemperature":"36°C~36.5°C","location":"四川省成都市郫都区西源大道2006号电子科技大学","healthColor":"绿色"}

for i in range(0,len(cookie)):
    headers['Cookie'] = cookie[i]   
    req1 = requests.get(url1,headers=headers)
    data1 = json.loads(req1.text)
    if(data1['data'] == None):
        print("%s打卡失败，原因：%s" % (namelist[i],data1['message']))
    elif(data1['data']['appliedTimes'] == 0):
        print("今天%s还没打卡，正在打卡......" % namelist[i]) 
        req2 = requests.post(url2,json=post_data,headers=headers)
        data2 = json.loads(req2.text)
        #print(data2)
        if(data2['status'] == True):print("提交成功，查询打卡状态......") #根据response判断打卡是否成功
        req3 = requests.get(url1,headers=headers)
        data3 = json.loads(req3.text)
        if(data3['data']['appliedTimes'] == 1):print("%s打卡成功" % namelist[i])
        else:print("打卡失败，请检查脚本")
    else:print("今天%s已打卡" % namelist[i])
#input()
print(time.strftime('%Y-%m-%d %H:%M:%S'))
