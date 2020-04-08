import urllib,requests
from urllib import request
from bs4 import BeautifulSoup as bs
import time
import re
import csv
import numpy as np
import pandas as pd
import time

def all_info(url,startpage,endpage):
	all_house_url = []

	# 抓取所有的主页URL
	for page in range(startpage,endpage):
		# 构造翻页的url
		page_url = url+'pg'+str(page)+'/#contentList'
		# 把该页的URL传给Spider_main进行抓取
		url_list = spider_main(page_url)
		all_house_url.append(url_list)

	# 得到每一页的URL中的房屋链接，下面可以抓取相应的信息
	# print(all_house_url)
	# 开始抓取每一页的房屋数据，用all_houst_detail_list存储每个发那个屋的信息
	all_house_detail_list = []
	for i in range(len(all_house_url)):
		print("第"+str(i+1)+"页房屋数据")
		url_page = all_house_url[i]
		
		# 进入每一页的房屋信息主页进行抓取
		for page in url_page:
			# 构造房屋的每一页url
			each_house_url = 'https://sh.lianjia.com'+page+'?nav=0'
			# print(each_house_url)
			# 将url传入到抓取房屋信息的house_details函数
			detail_list = house_details(each_house_url)
			if detail_list==None:
				continue

			all_house_detail_list.append(detail_list)
			time.sleep(4)

		print("完成第"+str(i+1)+"页房屋数据")
		time.sleep(18)
	# print(all_house_detail_list)
	return all_house_detail_list


# 构造配套设施的列表
# 有的配套设施列表
is_equip = ['<i style="background-image: url(https://image1.ljcdn.com/rent-front-image/03401a4eddd82179ae3774b43e382238.1524906085686_abc8a9ce-3748-4317-9955-2452322f07d9);"></i>',
 			'<i style="background-image: url(https://image1.ljcdn.com/rent-front-image/f01e63a2d0b36d2b6b92269dac7210a8.1524905973505_6a9e4bde-4acb-4699-ba93-32f4dc13304a);"></i>', 
 			'<i style="background-image: url(https://image1.ljcdn.com/rent-front-image/b45b25b8cbdbcbf1393999d1140d6729.1524906592660_dfa64012-e42c-4b11-a874-e2888e6dce4c);"></i>', 
 			'<i style="background-image: url(https://image1.ljcdn.com/rent-front-image/2c5080db6cb434413d39fe816faddafe.1524906138308_77f21b82-5983-4448-8348-ef9346263338);"></i>', 
 			'<i style="background-image: url(https://image1.ljcdn.com/rent-front-image/82e5b44b21844b608071ac426a5eb7e6.1524906411157_ae925a22-d95e-48bf-975c-447a27dd4ce9);"></i>', 
 			'<i style="background-image: url(https://image1.ljcdn.com/rent-front-image/c40aee40a80ebcaa8d716a2c9ae14391.1524906024762_ac4fb64e-8467-46de-b6f5-7f9ba1ce2622);"></i>',
 			'<i style="background-image: url(https://image1.ljcdn.com/rent-front-image/4c7c1728139585a142553edd47ecf2cd.1525926713820_83d52079-9922-41af-af95-45f889eb5c00);"></i>', 
 			'<i style="background-image: url(https://image1.ljcdn.com/rent-front-image/b2abaa59759a7f4ae327ed67c6fbc6d8.1524906246773_6b435b4a-03d6-4292-acd8-6d3af96a791d);"></i>',
  			'<i style="background-image: url(https://image1.ljcdn.com/rent-front-image/b024f9fdd5797563ead74f237105fd5a.1524906626107_4b1c45fe-0266-40af-b39c-6311887b0aaa);"></i>', 
  			'<i style="background-image: url(https://image1.ljcdn.com/rent-front-image/aa2df480d8496d0851febe38022b1da2.1524906515169_c731df5b-234f-4716-ba42-0058f833204c);"></i>'
]

def house_details(url):
	response = request.urlopen(url)
	re_html = response.read().decode('utf-8')
	# print(re_html)
	re_tree = bs(re_html,'html.parser')
	# print(re_tree)

	# title_info = re_tree.find(class_ = re.compile("content__title"))
	# 包含了小区名字，户型，朝向
	title_info = re_tree.find(class_ = "content__title")
	if title_info ==None:
		return
	title_info = re_tree.find(class_ = "content__title").text.split(' ')
	if len(title_info)<3:
		return
	# print(title_info)
	# 小区地址信息
	estate_info = title_info[0]
	if estate_info.startswith('整租'):
		estate_info = estate_info[3:]
	# 户型信息
	shape_info = title_info[1]
	# 朝向信息
	toward_info = title_info[2]
	# 月租金信息
	rent_info = re_tree.find(class_ = "content__aside--title").text

	# 房屋面积信息
	area_info = re_tree.find_all(class_ = "content__article__table")[0]
	area_info = area_info.find_all('span')[2].text[:-1]

	#房屋信息
	base_house = re_tree.find(class_ = "content__article__info")
	# print(base_house)
	base_house_list = base_house.find_all('li')
	base_house_list_info = [x.text for x in base_house_list]
	none_list = base_house_list_info[::3]
	# print(none_list)
	base_list = []
	for i in base_house_list_info:
		if i not in none_list:
			base_list.append(i)
	# print(base_list)

	# 发布日期
	release_date_info = base_list[0][3:]
	# 租期
	rent_period_info = base_list[2][3:]
	# 楼层
	layer_info = base_list[4][3:]
	# 电梯
	lift_info = base_list[5][3:]
	# 停车位
	parking_info = base_list[6][3:]
	# 用水
	water_info = base_list[7][3:]
	# 用电
	eletricity_info = base_list[8][3:]
	

	# 交通信息
	traffic_info = re_tree.find(class_ = 'content__article__info4').find_all('li')
	traffic_list = [x.text for x in traffic_info]
	traffic_dis = []
	if len(traffic_list) != 0:
		for i in range(len(traffic_list)):
			traffic_dis.append(int(traffic_list[i].split()[-1][:-1]))
		# 交通地铁线的数量
		subway_line_info = len(traffic_list)
		# print(subway_line_info)
		# 距离最近的地铁线的距离
		subway_distance_info = min(traffic_dis)
		# print(subway_distance_info)
	else:
		subway_line_info = 0
		subway_distance_info = 0

	# 地址和区域 
	address_list = re_tree.find(class_ = 'bread__nav__wrapper oneline').text.split()

	# print(address_list)
	address_info = address_list[2][:-2]
	district_info = address_list[4][:-2]
	# print(address_info)

	# 配套设施信息
	equipment = re_tree.find(class_ = 'content__article__info2')
	# print(type(equipment))
	# print(equipment.find_all('i'))
	equip_list  = []
	for line in equipment.find_all('i'):
		if str(line) in is_equip:
			equip_list.append(1)
		else:
			equip_list.append(0)
	
	# 是否有电视
	tv_info = equip_list[0]
	# 是否有冰箱
	fridge_info = equip_list[1]
	# 是否有洗衣机
	washer_info = equip_list[2]
	# 空调
	air_info = equip_list[3]
	# 热水器
	heater_info = equip_list[4]
	# 床
	bed_info = equip_list[5]
	# 暖气
	heating_info = equip_list[6]
	# 宽带
	wifi_info = equip_list[7]
	# 衣柜
	closet_info = equip_list[8]
	# 天然气
	gas_info = equip_list[9]
	
	# 图片链接
	pic = re_tree.find_all(class_ = 'content__article__slide__item')
	# print(pic)
	# print(pic[0] )

	pattern = r'img .*? src="(.+?\.jpg)"'
	complie_re = re.compile(pattern)
	imgList = complie_re.findall(re_html)
	img_info = imgList[0]
	time_info  = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
	return [address_info,district_info,estate_info,area_info,rent_info,layer_info,shape_info,toward_info,release_date_info,rent_period_info,lift_info,parking_info,water_info,eletricity_info,
			subway_line_info,subway_distance_info,tv_info,fridge_info,washer_info,air_info,heater_info,bed_info,heating_info,wifi_info,closet_info,gas_info,img_info,time_info]



# 返回主页的URL
def spider_main(url):
	# 伪造头
	# response = requests.get(url,{'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'})
	response = request.urlopen(url)
	re_html = response.read().decode('utf-8')
	# print(re_html)

	re_tree = bs(re_html,'html')
	# 抓取每一页的房屋信息URL
	house_url = re_tree.find_all(href=re.compile("^/zufang/SH"))
	# 将所有的房屋信息URL放入到一个list中
	house_list = []
	for i in range(len(house_url)):
		house_list.append(house_url[i]['href'])
	
	return list(set(house_list))
	# response = urllib.request.urlopen(url)
	# re_content  = response.read().decode('utf-8')
	# re_tree  = bs(re_content,'lxml')
	# print(re_tree)

def writer_csv(all_list,filename):
	with open(filename,"w") as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(["Address","District","Community","Area","RentPrice","Layer","Shape","Toward","Release_Date","Rent_Period","Is_lift","Is_parking","water_way","electricity_way","Subwayline_Number","Subway_Distance",
			'Is_TV','Is_fridge','Is_washer','Is_air','Is_heater','Is_bed','Is_heating','Is_wifi','Is_closet','Is_gas','Img_link'])
		writer.writerow(all_list)

if __name__ == '__main__':
	url = 'https://sh.lianjia.com/zufang/'
	# page_list = [[1,10],[10,12],[12,15],[15,17],[17,20]]
	# page_list=[[20,25],[25,30]]
	# page_list = [[10,16],[16,22],[22,28],[28,34],[34,40],[40,46],[46,51]]
	# page_list = [[51,56],[56,60],[60,65],[65,70],[75,80],[80,85],[85,90]]
	page_list = [[70,75],[80,85],[85,90]]
	name = ["Address","District","Community","Area","RentPrice","Layer","Shape","Toward","Release_Date","Rent_Period","Is_lift","Is_parking","water_way","electricity_way","Subwayline_Number","Subway_Distance",
			'Is_TV','Is_fridge','Is_washer','Is_air','Is_heater','Is_bed','Is_heating','Is_wifi','Is_closet','Is_gas','Is_img','Catch_time']
	for page in page_list:
		all_house_list = all_info(url,page[0],page[1])
		all_house_info = pd.DataFrame(columns = name,data=all_house_list)
		filename = 'F:/个人发展/机器学习/房价信息/houseinfo'+str(page[0])+'.csv'
		all_house_info.to_csv(filename,encoding = 'gbk',index = False)
	# all_house_list = np.array(all_house_list).T
	# writer_csv(all_house_list,'house_info.csv')