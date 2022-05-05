import jsonpath
import requests
import base64
import re
from m3u8download_hecoter import m3u8download
from playwright.sync_api import sync_playwright
import os


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
    'cookie': 'pgv_pvid=4331793015; eas_sid=H1h6q4U7H5q9M652q8G6S4D2F9; RK=btVx/bHBee; ptcz=9bfa9d14b2107392c520e16cdbc92bfdfbcd5a07022db22b1c33d784ad4b74ee; ts_refer=cn.bing.com/; iswebp=1; auth_version=2.0; mix_login_mode=true; ptui_loginuin=1967416560; luin=o1967416560; lskey=000100006f4006ca0f64a90bd2dda240b22c4da0704832ac8ef76b2fc679035c9f04b85324d080c96fe1d1c6; p_lskey=000400009cbdc1b24ee9171008e57653d734afbebcd6d6d7b098597937a8930d124c2ac0651bec6e953da1f5; uid_type=0; uin=1967416560; p_uin=1967416560; p_luin=1967416560; uid_uin=1967416560; uid_origin_uid_type=0; uid_origin_auth_type=0; ke_login_type=1; sessionPath=16516774470057034474434; _pathcode=0.17126931133406575; tdw_auin_data=-; tdw_data_testid=; tdw_data_flowid=; tdw_first_visited=1; pgv_info=ssid=s9771023168; ts_last=ke.qq.com/; ts_uid=9571296640; Hm_lvt_0c196c536f609d373a16d246a117fd44=1651643810,1651654054,1651677448; Hm_lpvt_0c196c536f609d373a16d246a117fd44=1651677448; tdw_data={"ver4":"cn.bing.com","ver5":"","ver6":"","refer":"cn.bing.com","from_channel":"","path":"aB-0.17126931133406575","auin":"-","uin":"1967416560","real_uin":"967416560"}; tdw_data_new_2={"auin":"-","sourcetype":"","sourcefrom":"","ver9":"1967416560","uin":"1967416560","visitor_id":"7631666100227017","ver10":"","url_page":"","url_module":"","url_position":"","sessionPath":"16516774470057034474434"}',
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
print('----------------------------------------')
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
    cname=course_list['name']
    print(cname)
    terms=course_list['terms']
    if len(terms)>1:
        for project in terms:
            print(terms.index(project),project['name'])
        project_num=eval(input('请输入你的课程编号:'))
        sub_course_list = jsonpath.jsonpath(terms[project_num], '$..sub_info')
        # print(sub_course_list)
        for sub_course in sub_course_list[0]:
            print('-------')
            # print(sub_course)
            part_name = sub_course['name']
            print(part_name)
            task_list = sub_course['task_info']
            for task in task_list:
                if task['type'] == 3:
                    continue
                if task['type'] == 1:
                    title = task['name'].replace('/','-')
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
                    title = task['name']
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
        for sub_course in sub_course_list[0]:
            print('-------')
            # print(sub_course)
            part_name=sub_course['name']
            print(part_name)
            task_list=sub_course['task_info']
            for task in task_list:
                if task['type']==3:
                    continue
                if task['type']==1:
                    title = task['name']
                    try:
                        resid_list=str(re.findall(r"\b\d+\b", str(task['resid_list']))[0])
                    except:
                        print('已过期，无法下载')
                        break

                if task['type']==2:
                    title=task['name']
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








