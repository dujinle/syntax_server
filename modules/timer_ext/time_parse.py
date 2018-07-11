#!/usr/bin/python
#-*- coding:utf-8 -*-
import re,common
from time_base import TimeBase
#标记对象以及链接的网络
class TimeParse(TimeBase):

	def encode(self,struct):
		try:
			struct['TimeParse'] = dict();
			self.parse_time_lamda(struct);
			self.calc_time_lamda(struct);
		except Exception as e: raise e;

	def parse_time_lamda(self,struct):
		try:
			for item in struct['TimeLamda']:
				if item['label'] == 'TimeN':
					if self.data.has_key(item['type']):
						mdata = self.data[item['type']];
						for idata in mdata:
							p = re.compile(idata['reg']);
							amatch = p.search(item['str']);
							if amatch is None: continue;
							item['func'] = idata;
				elif item['label'] == 'TimeC':
					for iitem in item['list']:
						if self.data.has_key(iitem['type']):
							mdata = self.data[iitem['type']];
							for idata in mdata:
								p = re.compile(idata['reg']);
								amatch = p.search(iitem['str']);
								if amatch is None: continue;
								iitem['func'] = idata;
		except Exception as e: raise e;

	def calc_time_lamda(self,struct):
		try:
			struct['TimeParse']['strs'] = list();
			for item in struct['TimeLamda']:
				if item['label'] == 'TimeN' and item.has_key('func'):
					if item['func']['type'] == "JIEJIARI" or item['func']['type'] == "JIEQI":
						date = item['func']['date'];
						struct['TimeParse']['month'] = date.split('/')[0];
						struct['TimeParse']['day'] = date.split('/')[1];
						struct['TimeParse']['strs'].append(item['str']);
						if item['func'].has_key('year_type'):
							struct['TimeParse']['year_type'] = item['func']['year_type'];
					elif item['func']['type'] == "ONEDAY":
						 struct['TimeParse'][item['func']['scope']] = item['func']['region'];
						 struct['TimeParse']['strs'].append(item['str']);
				elif item['label'] == 'TimeC':
					for iitem in item['list']:
						if iitem['label'] == 'TimeN' and iitem.has_key('func'):
							if iitem['func']['type'] == "JIEJIARI" or iitem['func']['type'] == "JIEQI":
								date = iitem['func']['date'];
								struct['TimeParse']['month'] = date.split('/')[0];
								struct['TimeParse']['day'] = date.split('/')[1];
								struct['TimeParse']['strs'].append(iitem['str']);
								if iitem['func'].has_key('year_type'):
									struct['TimeParse']['year_type'] = iitem['func']['year_type'];
							elif iitem['func']['type'] == "ONEDAY":
						 		struct['TimeParse'][iitem['func']['scope']] = iitem['func']['region'];
						 		struct['TimeParse']['strs'].append(iitem['str']);
				elif item['label'] == 'Time':
					#解析小时级别
					p = re.compile(u'[时点]');
					amatch = p.search(item['str']);
					if not amatch is None:
						hour = item['num'].pop(0);
						struct['TimeParse']['hour'] = hour['value'];
					#解析分钟级别
					p = re.compile(u'[分]');
					amatch = p.search(item['str']);
					if not amatch is None:
						minute = item['num'].pop(0);
						struct['TimeParse']['minute'] = minute['value'];
					#解析秒级别
					p = re.compile(u'[秒]');
					amatch = p.search(item['str']);
					if not amatch is None:
						second = item['num'].pop(0);
						struct['TimeParse']['second'] = second['value'];
		except Exception as e: raise e;




