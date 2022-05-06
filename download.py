import jsonpath
import requests
import base64
import re
from m3u8download_hecoter import m3u8download
from playwright.sync_api import sync_playwright
import os

print('---------程序正在启动打开本地浏览器---------')
with sync_playwright() as p:
    browser = p.chromium.launch(channel='msedge', headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://ke.qq.com/")
    print('获取cookie中.......')
    html = page.inner_html('[class="mod-entry-user-schedule"]')
    assert "我的课表 " in html
    storage = context.storage_state()
    cookies_list= {}
    for k in storage['cookies']:
        cookies_list[k['name']]=k['value']
    string=''
    for item in cookies_list:
        string+='{}={};'.format(item,cookies_list[item])
    cookie=string.strip(';')
    print('获取cookie完成')
    page.close()
    context.close()
    browser.close()

uin=cookies_list['uid_uin']
try:
    uid_a2=cookies_list['uid_a2']
except:
    uid_a2=''
try:
    uid_appid=cookies_list['uid_appid']
except:
    uid_appid=''
uid_type=cookies_list['uid_type']
uid_origin_uid_type=cookies_list['uid_origin_uid_type']
uid_origin_auth_type=cookies_list['uid_origin_auth_type']
try:
    p_skey=cookies_list['p_skey']
except:
    p_skey=''
try:
    p_lskey=cookies_list['p_lskey']
except:
    p_lskey=''
try:
    skey=cookies_list['skey']
except:
    skey=''

print('--------------以下为已有课程--------------')
course_list={}
i=1
while True:
  url4 = "https://ke.qq.com/cgi-proxy/user/user_center/get_plan_list?page={}&count=10&bkn=801997445&t=0.8229".format(i)
  headers4 = {
    'authority': 'ke.qq.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': cookie,
    'referer': 'https://ke.qq.com/user/index/index.html',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/101.0.1210.32'
  }
  response4 = requests.get(url4, headers=headers4)
  # print(response.text)
  i+=1
  if jsonpath.jsonpath(response4.json(),'$..map_list')[0]==[]:
    break
  else:
    for item in jsonpath.jsonpath(response4.json(),'$..map_courses'):
      for course in item:
        c_name=course['cname']
        cid=course['cid']
        course_list[c_name]=cid
        print(c_name)
print('---------------------------------------')
while True:
    try:
        cid=str(course_list[input('请输入要下载课程名:')])
        break
    except:
        print('请输入正确的课程名,重新输入')

def get_realurl(term_id,resid_list):
    url2 = "https://ke.qq.com/cgi-proxy/rec_video/describe_rec_video"
    params2 = {
        "course_id": cid,
        "file_id": resid_list,
        "header": "{\"srv_appid\":201,\"cli_appid\":\"ke\",\"uin\":\""+uin+"\",\"cli_info\":{\"cli_platform\":3}}",
        "term_id": term_id,
        "vod_type": "0",
        "bkn": "359971155",
        "r": "0.0920"
    }
    headers2 = {
        'authority': 'ke.qq.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'cookie': cookie,
            "referer": "https://ke.qq.com/webcourse/"+cid+"/"+term_id,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
    }
    response2 = requests.get(url2, headers=headers2, params=params2)
    # print(response2.json())
    key_url=jsonpath.jsonpath(response2.json(),'$..url')[0]
    if skey=='':
        str = "uin={};skey=;pskey=;plskey=;ext={};uid_appid={};uid_type={};uid_origin_uid_type={};uid_origin_auth_type={};cid={};term_id={};vod_type=0".format(uin,uid_a2,uid_appid,uid_type,uid_origin_uid_type,uid_origin_auth_type,cid,term_id).encode()
    else:
        str ='uin={};skey={};pskey={};plskey={};ext=;uid_type={};uid_origin_uid_type={};uid_origin_auth_type={};cid={};term_id={};vod_type=0'.format(uin,skey,p_skey,p_lskey,uid_type,uid_origin_uid_type,uid_origin_auth_type,cid,term_id).encode()
    key = base64.b64encode(str).decode()
    # print(key)
    list1 = key_url.split('/')
    list1.insert(6, 'voddrm.token.{}.'.format(key) + list1[6])
    del list1[7]
    # print(list1)
    real_url = '/'.join(list1)
    return real_url

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "-", title)  # 替换为-
    return new_title

url = "https://ke.qq.com/cgi-bin/course/basic_info"
params = {
    "cid": cid,
    "bkn": "359971155",
    "t": "0.0695"
}
headers = {
  'authority': 'ke.qq.com',
  'accept': '*/*',
  'accept-language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
  'cookie': cookie,
  "referer": "https://ke.qq.com/letter/index.html",
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}

response = requests.get(url, headers=headers,params=params)
# print(response.json())
for course_list in jsonpath.jsonpath(response.json(),'$..course_detail'):
    # for course in course_list:
        # print(course)
    # cname=jsonpath.jsonpath(course_list,'$..cname')[0]
    cname=validateTitle(course_list['name'])
    print(cname)
    terms=course_list['terms']
    if len(terms)>1:
        for project in terms:
            print(terms.index(project),project['name'])
        project_num=eval(input('请输入你的课程编号:'))
        sub_course_list = jsonpath.jsonpath(terms[project_num], '$..sub_info')
        # print(sub_course_list)
        for sub_course1 in sub_course_list:
            print('-------')
            # print(len(sub_course1))
            for sub_course in sub_course1:
                part_name = validateTitle(sub_course['name'])
                print(part_name)
                task_list = sub_course['task_info']
                for task in task_list:
                    if task['type'] == 3:
                        continue
                    if task['type'] == 1:
                        title = validateTitle(task['name'])
                        # print(task['resid_list'])
                        try:
                            resid_list = str(re.findall(r"\b\d+\b", str(task['resid_list']))[0])
                        except:
                            print('已过期，无法下载')
                            break
                        term_id = str(task['term_id'])
                        realurl = get_realurl(term_id, resid_list)
                        filedir = r'.\视频'+'\{}\{}'.format(cname,part_name)
                        if os.path.exists(filedir+'\\'+title+'.mp4'):
                            print(title)
                            print('已下载，不重复下载')
                        else:
                            m3u8download(realurl, title=title, work_dir=filedir)
                        # print(title)
                        # print(resid_list)
                        # print(filedir)
                    if task['type'] == 2:
                        title = validateTitle(task['name'])
                        resid_list = str(task['resid_list'])
                        term_id = str(task['term_id'])
                        # print(title)
                        realurl = get_realurl(term_id, resid_list)
                        # print(realurl)

                        filedir = r'.\视频' + '\{}\{}'.format(cname, part_name)
                        if os.path.exists(filedir+'\\'+title+'.mp4'):
                            print(title)
                            print('已下载，不重复下载')
                        else:
                            m3u8download(realurl, title=title, work_dir=filedir)

    else:
        sub_course_list=jsonpath.jsonpath(course_list,'$..sub_info')
        # print(sub_course_list)
        for sub_course1 in sub_course_list:
            print('-------')
            # print(len(sub_course1))
            for sub_course in sub_course1:
                part_name=validateTitle(sub_course['name'])
                print(part_name)
                task_list=sub_course['task_info']
                for task in task_list:
                    if task['type']==3:
                        continue
                    if task['type']==1:
                        title = validateTitle(task['name'])
                        try:
                            resid_list=str(re.findall(r"\b\d+\b", str(task['resid_list']))[0])
                        except:
                            print('已过期，无法下载')
                            break

                    if task['type']==2:
                        title=validateTitle(task['name'])
                        resid_list=str(task['resid_list'])
                        term_id=str(task['term_id'])
                        # print(title)
                        realurl=get_realurl(term_id,resid_list)
                        # print(realurl)

                        filedir = r'.\视频'+'\{}\{}'.format(cname,part_name)
                        if os.path.exists(filedir+'\\'+title+'.mp4'):
                            print(title)
                            print('已下载，不重复下载')
                        else:
                            m3u8download(realurl, title=title, work_dir=filedir)








