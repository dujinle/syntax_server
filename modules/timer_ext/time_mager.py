#!/usr/bin/python
#-*- coding:utf-8 -*-

import os,sys,common,time
from time_label import TimeLabel
from time_lamda import TimeLamda
from time_parse import TimeParse
class TimeMager():
	def __init__(self):

		self.time_conf = dict();
		#默认的时间方式 阳历
		self.time_conf['year_type'] = 'solar';
		#默认的时间基点 当前时间
		self.time_conf['time_origin'] = time.time();
		#时间不充分自动用当前时间补充
		self.time_conf['time_fill'] = True;
		base_path = os.path.dirname(__file__);
		self.dfiles = [
			os.path.join(base_path,'tdata','time_label.json'),
			os.path.join(base_path,'tdata','time_lamda.json'),
			os.path.join(base_path,'tdata','timen_seq.json')
		]
		self.tag_objs = list();
		self.tag_objs.append(TimeLabel());
		self.tag_objs.append(TimeLamda());
		self.tag_objs.append(TimeParse());

	def init(self):
		try:
			for i,obj in enumerate(self.tag_objs):
				obj.load_data(self.dfiles[i]);
		except Exception as e: raise e;

	def encode(self,struct):
		try:
			for obj in self.tag_objs:
				obj.encode(struct,self.time_conf);
		except Exception as e: raise e;
