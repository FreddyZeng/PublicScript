#!/usr/bin/python3
from requests import Request, Session
from datetime import date, datetime
import json
import sys, getopt



# 请求超时
timeout = 3

specify_day = None # specify_day = '2021-04-27' 指定日期预约。每天8点。默认无

login = False # 是否需要登录步骤, 默认否
config = False # 是否需要登录步骤, 默认否

# token appId
token = '' # 通过charles抓包获取
appId = '' # 通过charles抓包获取

# 疫苗id
vaccCode = 2401 #设置为None查询疫苗，疫苗状态为1充足可预约或2紧张可预约都可以预约，疫苗状态3没库存不可预约。 通过抓包获取
reucId = '' # 通过抓包获取，getBindUserList


# 医院信息

#容桂社区花溪预防接种门诊 每周一二三四五六
#顺德容桂桂州大道中11号
depaId = 'ECD56DA3-2AAF-48D5-AFA8-AA76597FBC0B'
depaCode = '4406060231'



# 设置终端代理
#export HTTP_PROXY=127.0.0.1:8080
#export HTTPS_PROXY=127.0.0.1:8080
#export FTP_PROXY=127.0.0.1:8080



headers = {
	'appId': appId,
	'Referer': 'https://jmyy.wjj.foshan.gov.cn/mobile/?appId=' + appId,
	'token': token,
	'Cookie': 'lg-token=' + token,



	'Host': 'jmyy.wjj.foshan.gov.cn',
	'Accept': 'application/json, text/plain, */*',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1320.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63010200)',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.5;q=0.4',
	'Connection': 'keep-alive'
	}

s = Session()

def get_login():
	url = 'https://jmyy.wjj.foshan.gov.cn/mobile/oauth/login?code=' + token
	headers_copy = dict(headers)

	req = Request('GET',  url, headers=headers_copy)

	prepped = s.prepare_request(req)

	r = s.send(prepped,
    timeout=timeout
	)
	response = r.json()
	print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))
	

def get_config():
	url = 'https://jmyy.wjj.foshan.gov.cn/mobile/wxapi/getConfig?url=https%253A%252F%252Fjmyy.wjj.foshan.gov.cn%252Fmobile%252F%253FappId%253D' + appId

	headers_copy = dict(headers)
	headers_copy['Cache-Control'] = 'max-age=0'

	req = Request('GET',  url, headers=headers_copy)

	prepped = s.prepare_request(req)

	r = s.send(prepped,
    timeout=timeout
	)
	response = r.json()
	print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))

def query_hospital():
	print('\n查询医院\n')
	url = 'https://jmyy.wjj.foshan.gov.cn/mobile/outpatient/nearby'
	payload = {
	'pageNum': 1, 
	'numPerPage': 45, 
	'areaId': '440600', 
	'outpName': '', 
	'outpMapLongitude': '', 
	'outpMapLatitude': '', 
	}
	print(json.dumps(payload, indent=4, sort_keys=True, ensure_ascii=False))
	headers_copy = dict(headers)
	headers_copy['Origin'] = 'https://jmyy.wjj.foshan.gov.cn'
	headers_copy['Content-Type'] = 'application/json;charset=UTF-8'

	req = Request('POST',  url, headers=headers_copy, data=json.dumps(payload))

	prepped = s.prepare_request(req)

	r = s.send(prepped,
    timeout=timeout
	)

	print('状态码：' + str(r.status_code))
	response = r.json()
	print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))

def get_vaccCode(depaCode, ouatId):
	url = 'https://jmyy.wjj.foshan.gov.cn/mobile/vaccineInventory/getDepaVaccineList?depaCode='+ depaCode +'&ouatId=' + ouatId

	headers_copy = dict(headers)
	headers_copy['Cache-Control'] = 'max-age=0'

	req = Request('GET',  url, headers=headers_copy)

	prepped = s.prepare_request(req)

	r = s.send(prepped,
    timeout=timeout
	)
	response = r.json()
	print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))

def get_day_is_alivable(today_date):
	global vaccCode

	url = 'https://jmyy.wjj.foshan.gov.cn/mobile/reservationStock/list?depaId=' + depaId + '&restDate=' + today_date

	req = Request('GET',  url, headers=headers)

	prepped = s.prepare_request(req)

	r = s.send(prepped,
    timeout=timeout
	)
	#print('状态码：' + str(r.status_code))
	#print(r.json())

	response = r.json()
	print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))

	if str(r.status_code) != '200':
		exit(-1)
	if str(response['ecode']) != '1000':
		exit(-1)
	data_array = response['data']
	for i, day in enumerate(data_array):
		rest_surplus = day['restSurplus']
		if rest_surplus > 0 or vaccCode == None: # > 0当天可预约
			rest_date = day['restDate']
			return rest_date.split(' ', 1)[0]


def get_ouatId_of_alivableDay(day):
	global vaccCode

	url = 'https://jmyy.wjj.foshan.gov.cn/mobile/reservationStock/timeNumber?depaId=' + depaId + '&date=' + day

	req = Request('GET',  url, headers=headers)

	prepped = s.prepare_request(req)

	r = s.send(prepped,
    timeout=timeout
	)
	print('状态码：' + str(r.status_code))
	response = r.json()
	print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))

	if str(r.status_code) != '200':
		exit(-1)
	if str(response['ecode']) != '1000':
		exit(-1)
	data_array = response['data']
	for i, time_range in enumerate(data_array):
		rest_surplus = time_range['restSurplus']
		if rest_surplus > 0 or vaccCode == None: # > 0当天可预约
			return time_range['ouatId']

def save_appointment(day, ouatId, reucId):
	print('\n开始预约\n')
	url = 'https://jmyy.wjj.foshan.gov.cn/mobile/reservation/saveAppointment'
	payload = {
	'reucId': reucId, # 孩子id
	'depaId': depaId, # 医院id
	'reseDate': day, # 打疫苗日期
	'ouatId': ouatId, # 打疫苗时段
	'vaccCode': vaccCode, # 打疫苗的类型
	}
	print(json.dumps(payload, indent=4, sort_keys=True, ensure_ascii=False))
	headers_copy = dict(headers)
	headers_copy['Origin'] = 'https://jmyy.wjj.foshan.gov.cn'
	headers_copy['Content-Type'] = 'application/json;charset=UTF-8'

	req = Request('POST',  url, headers=headers_copy, data=json.dumps(payload))

	prepped = s.prepare_request(req)

	r = s.send(prepped,
    timeout=timeout
	)

	print('状态码：' + str(r.status_code))
	response = r.json()
	print(json.dumps(response, indent=4, sort_keys=True, ensure_ascii=False))
	

def main(argv):
	global login
	global config
	global vaccCode
	global specify_day
	global reucId

	ouatId_time = 0

	try:
	   opts, args = getopt.getopt(argv,"hv:c:lqd:at:",["vaccCode=","child=","login=","query=","day=","address=", "time="])
	except getopt.GetoptError:
	   print('抢号 vaccine.py -v 2401 -c 2 -d 2021-04-13 -t 0')
	   print('抢号参数解析 vaccine.py -v 疫苗id编号 -c 孩子id编号 -d 日期 -t 时段偏移:8点起，8点为0，t每增加1增加30分钟时段')
	   print('查询可预约日期或获取疫苗id vaccine.py -q')
	   print('查询医院信息 vaccine.py -a')
	   print('登录 vaccine.py -l')
	   sys.exit(2)
	for opt, arg in opts:
		if opt == 'h':
			print('抢号 vaccine.py -v 2401 -c 2 -d 2021-04-13 -t 0')
			print('抢号参数解析 vaccine.py -v 疫苗id编号 -c 孩子id编号 -d 日期 -t 时段偏移:8点起，8点为0，t每增加1增加30分钟时段')
			print('查询可预约日期或获取疫苗id vaccine.py -q')
			print('查询医院信息 vaccine.py -a')
			print('登录 vaccine.py -l')
			sys.exit()
		elif opt in ("-v", "--vaccCode"):
			vaccCode = arg
		elif opt in ("-c", "--child"):
			reucId = arg # xing标记孩子id，getBindUserList
		elif opt in ("-d","--day"):
			specify_day = str(arg)
		elif opt in ("-t", "--time"):
			ouatId_time = int(arg)
		elif opt in ("-l", "--login"):
			login = True
			config = True
			get_config()
			get_login()
			exit(0)
		elif opt in ("-q", "--query"):
			vaccCode = None
		elif opt in ("-a", "--address"):
			query_hospital()
			exit(0)

	day = specify_day
	
	if specify_day == None:
		today = date.today()
		today_date = today.strftime("%Y-%m-%d")
		print('请求可预约的日期')
		day = get_day_is_alivable(today_date)
		
	if day == None:
		print('\n找不到可预约的日期\n')
		exit(-1)
	
	print('日期' + day + '\n')
	day_date = datetime.strptime(day, '%Y-%m-%d')
	print('\n星期几：' + str(day_date.weekday() + 1))

	#预约时段 ouatId, 不同的疫苗注射地点上班时间不一样，一般是周一至周六上班，周日休息
	#星期一 3722 8:00-8:30 ，如要预约9:00-9:30需要设置为3723
	#星期二 3738
	#星期三 3754
	#星期四 3770
	#星期五 3786
	#星期六 3806
	#星期日 3706
	ouatIds = [3722, 3738, 3754, 3770, 3786, 3860, 3706]
	ouatId =  ouatIds[day_date.weekday()]
	ouatId += ouatId_time

	if specify_day == None:
		ouatId = get_ouatId_of_alivableDay(day)
		if ouatId == None:
			print('\n找不到可预约的时段\n')
			exit(-1)

	if vaccCode == None:
		get_vaccCode(depaCode, ouatId)
		exit(-1)
	
	save_appointment(day, ouatId, reucId)

if __name__ == '__main__':
	main(sys.argv[1:])