#!/usr/bin/python
#-*- coding:utf-8 -*-
import re,common,time
from time_base import TimeBase
import time_calendar as TCalendarTool
#标记对象以及链接的网络
date_index = {
	'year':0,
	'month':1,
	'day':2,
	'hour':3,
	'minute':4,
	'second':5
};
class TimeParse(TimeBase):

	def encode(self,struct,time_conf):
		try:
			struct['TimeParse'] = dict();
			self.parse_time_lamda(struct);
			self.calc_time_lamda(struct,time_conf);
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
				elif item['label'] == 'REL':
					if self.data.has_key(item['type']):
						mdata = self.data[item['type']];
						for idata in mdata:
							p = re.compile(idata['reg']);
							amatch = p.search(item['str']);
							if amatch is None: continue;
							item['func'] = idata;
		except Exception as e: raise e;

	def calc_time_lamda(self,struct,time_conf):
		try:
			struct['TimeParse']['strs'] = list();
			time_lamda = list();
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
					elif item['func']['type'] == 'JIERIWEEK':
						if struct['TimeParse'].has_key('year'):
							(struct['TimeParse']['year'],struct['TimeParse']['month'],struct['TimeParse']['day']) \
							 	= TCalendarTool.GetSolarWeek(
									int(struct['TimeParse']['year']),
									int(item['func']['month']),
									int(item['func']['week_idx']),
									int(item['func']['week']) + 1
								);
							struct['TimeParse']['strs'].append(item['str']);
					else:
						time_lamda.append(item);
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
						 		struct['TimeParse']['hour'] = iitem['func']['region'];
						 		struct['TimeParse']['strs'].append(iitem['str']);
						 		if iitem['func']['region'][0] > 12:
						 			struct['TimeParse']['hour_flag'] = 12;
						 		else:
						 			struct['TimeParse']['hour_flag'] = 0;
				elif item['label'] == 'Time':
					#解析小时级别
					p = re.compile(u'[时点]');
					amatch = p.search(item['str']);
					if not amatch is None:
						hour = item['num'].pop(0);
						if struct['TimeParse'].has_key('hour_flag'):
							struct['TimeParse']['hour'] = int(hour['value']) + struct['TimeParse']['hour_flag'];
						else:
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
					struct['TimeParse']['strs'].append(item['str']);
				elif item['label'] == 'Date':
					#解析小时级别
					p = re.compile(u'年');
					amatch = p.search(item['str']);
					if not amatch is None:
						year = item['num'].pop(0);
						struct['TimeParse']['year'] = year['value'];
					#解析分钟级别
					p = re.compile(u'月');
					amatch = p.search(item['str']);
					if not amatch is None:
						month = item['num'].pop(0);
						struct['TimeParse']['month'] = month['value'];
					#解析秒级别
					p = re.compile(u'[日号]');
					amatch = p.search(item['str']);
					if not amatch is None:
						day = item['num'].pop(0);
						struct['TimeParse']['day'] = day['value'];
					struct['TimeParse']['strs'].append(item['str']);
				elif item['label'] == 'REL':
					if time_conf.has_key('time_origin'):
						time_stc = time.localtime(time_conf['time_origin']);
						if item.has_key('func'):
							func = item['func'];
							if func['func'] == 'prev':
								struct['TimeParse'][func['scope']] = time_stc[date_index[func['scope']]] - 1;
							elif func['func'] == 'prev2':
								struct['TimeParse'][func['scope']] = time_stc[date_index[func['scope']]] - 2;
							elif func['func'] == 'next':
								struct['TimeParse'][func['scope']] = time_stc[date_index[func['scope']]] + 1;
							elif func['func'] == 'next2':
								struct['TimeParse'][func['scope']] = time_stc[date_index[func['scope']]] + 2;
						struct['TimeParse']['strs'].append(item['str']);
				elif item['label'] == 'TimeSet':
					if time_conf.has_key('time_origin') and time_conf['time_fill'] == True:
						time_stc = time.localtime(time_conf['time_origin']);
						if not struct['TimeParse'].has_key('year'):
							time_stc = time.localtime(time_conf['time_origin']);
							struct['TimeParse']['year'] = time_stc[date_index['year']];
						if not struct['TimeParse'].has_key('month'):
							time_stc = time.localtime(time_conf['time_origin']);
							struct['TimeParse']['month'] = time_stc[date_index['month']];
						if not struct['TimeParse'].has_key('day'):
							time_stc = time.localtime(time_conf['time_origin']);
							struct['TimeParse']['day'] = time_stc[date_index['day']];
						print 'time set start.....'
						(struct['TimeParse']['year'],struct['TimeParse']['month'],struct['TimeParse']['day']) \
							= TCalendarTool.GetWeekDay(
								int(struct['TimeParse']['year']),
								int(struct['TimeParse']['month']),
								int(struct['TimeParse']['day']),
								int(item['num'].pop()['value'])
							);
						struct['TimeParse']['strs'].append(item['str']);
				else:
					time_lamda.append(item);
			if len(time_lamda) == 0 and struct.has_key('TimeLamda'):
				del struct['TimeLamda'];
			else:
				struct['TimeLamda'] = time_lamda;
			if time_conf['time_fill'] == True:
				if not struct['TimeParse'].has_key('year'):
					time_stc = time.localtime(time_conf['time_origin']);
					struct['TimeParse']['year'] = time_stc[date_index['year']];
				if not struct['TimeParse'].has_key('month'):
					time_stc = time.localtime(time_conf['time_origin']);
					struct['TimeParse']['month'] = time_stc[date_index['month']];
				if not struct['TimeParse'].has_key('day'):
					time_stc = time.localtime(time_conf['time_origin']);
					struct['TimeParse']['day'] = time_stc[date_index['day']];

			if struct['TimeParse'].has_key('year_type') and struct['TimeParse']['year_type'] == 'lunar':
				if struct['TimeParse'].has_key('year') and struct['TimeParse'].has_key('month') and struct['TimeParse'].has_key('day'):
					(struct['TimeParse']['year'],struct['TimeParse']['month'],struct['TimeParse']['day']) \
						= TCalendarTool.ToSolarDate(
							int(struct['TimeParse']['year']),
							int(struct['TimeParse']['month']),
							int(struct['TimeParse']['day'])
						);
					struct['TimeParse']['year_type'] = 'solar';
		except Exception as e: raise e;




