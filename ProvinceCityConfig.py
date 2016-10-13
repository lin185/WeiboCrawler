#!/usr/bin/env python
# coding: utf-8
from xml.etree import ElementTree

#1. All Chinese characters are in ascii, you might want to decode them into utf-8
#2. Ids are in str

class ProvinceCityConfig:


	# Consturctor
	def __init__(self):

		#variabls
		self.province = []
		self.province_id = []
		self.city = []
		self.city_id = []

		#parsing xml
		tree = ElementTree.parse('ProvinceCityCode.xml')
		root = tree.getroot()
		for node in tree.findall('.//Province/Pname'):
			self.province.append(node.text.encode('utf-8'))
		for node in tree.findall('.//Province/Pcode'):
			self.province_id.append(node.text)
		for child in root:
			temp=[]
			for node in child.findall('Cities/City/Cname'):
				temp.append(node.text.encode('utf-8'))
			self.city.append(temp)
		for child in root:
			temp=[]
			for node in child.findall('Cities/City/Ccode'):
				temp.append(node.text)
			self.city_id.append(temp)


	# Functions:

	#Get provinces names
	def getProvinceList(self):

		return self.province

	#Get province id given its name
	def getProvinceID(self, province_name):

		return self.province_id[self.province.index(province_name.encode('utf-8'))]

	#Get province name given its id
	def getProvinceName(self, province_number):

		return self.province[self.province_id.index(province_number)].decode('utf-8')

	#Get city id given the name of provicne and city
	def getCityID(self, province_name, city_name):

		return self.city_id[self.province.index(province_name.encode('utf-8'))][self.city[self.province.index(province_name.encode('utf-8'))].index(city_name.encode('utf-8'))]

	#Get city name given the id of province and city
	def getCityName(self, province_number, city_number):

		return self.city[self.province_id.index(province_number)][self.city_id[self.province_id.index(province_number)].index(city_number)].decode('utf-8')

	#Get names of cities in a given province
	def getCitiesOfProvince(self, province_number):

		return self.city[self.province_id.index(province_number)]



# Test code stard here

#test = ProvinceCityConfig()

#prov_list = test.getProvinceList()
#for item in prov_list:
#	print item.decode('utf-8') 

#prov_id = test.getProvinceID('天津')
#print prov_id

#prov_name = test.getProvinceName('12')
#print prov_name.decode('utf-8')

#city_id = test.getCityID('天津','静海县')
#print city_id

#city_name = test.getCityName('12','23')
#print  city_name.decode('utf-8')

#cities_of_prov = test.getCitiesOfProvince('12')
#for item in cities_of_prov:
#	print item.decode('utf-8')

