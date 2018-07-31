#!/usr/bin/python
#-*- coding:utf-8 -*-
import re,common,time
import time_common as TimeCommon
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
big = u'大';
up = u'上';
down = u'下';

class TimeParse(TimeBase):

	def encode(self,struct,time_conf):
		try:
			if not struct.has_key('TimeLamda'): return;
			struct['TimeParse'] = dict();
			self.parse_time_lamda(struct);
			self.calc_time_lamda(struct,time_conf);
			self.reseg_text(struct);
			self.repair_time(struct);
		except Exception as e: raise e;

	def parse_time_lamda(self,struct):
		try:
			for item in struct['TimeLamda']:
				if item['label'] == 'TimeC':
					for iitem in item['list']:
						if self.data.has_key(iitem['type']):
							mdata = self.data[iitem['type']];
							for idata in mdata:
								p = re.compile(idata['reg']);
								amatch = p.search(iitem['str']);
								if amatch is None: continue;
								iitem['func'] = idata;
				elif item['label'] == 'TimeD' or item['label'] == 'TimeDD':
					if self.data.has_key(item['type']):
						mdata = self.data[item['type']];
						for idata in mdata:
							tstr = self.prev_num2text(item);
							p = re.compile(idata['reg']);
							amatch = p.search(tstr);
							if amatch is None: continue;
							item['func'] = idata;
				else:
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
			ret = False;
			for item in struct['TimeLamda']:
				if item['label'] == 'TimeN' and item.has_key('func'):
					ret = self.calc_timen_stc(item,struct,time_lamda);
				elif item['label'] == 'Other' and item.has_key('func'):
					struct['TimeParse'][item['func']['scope']] = item['func']['region'];
					struct['TimeParse']['strs'].append(item['str']);
					ret = True;
				elif item['label'] == 'TimeC':
					ret = self.calc_timec_stc(item,struct,time_lamda);
				elif item['label'] == 'Time':
					ret = self.calc_time_stc(item,struct,time_lamda);
				elif item['label'] == 'Date':
					ret = self.calc_date_stc(item,struct,time_lamda);
				elif item['label'] == 'REL':
					ret = self.calc_timerel_stc(item,struct,time_conf);
				elif item['label'] == 'TimeD':
					ret = self.calc_timed_stc(item,struct,time_conf);
				elif item['label'] == 'TimeSet':
					ret = self.calc_timeset_stc(item,struct,time_conf);
				elif item['label'] == 'Direct':
					struct['TimeParse']['dir'] = item['func'];
					struct['TimeParse']['dir']['times'] = 0;
					for tdd in item['str']:
						struct['TimeParse']['dir']['times'] = struct['TimeParse']['dir']['times'] + 1;
					struct['TimeParse']['strs'].append(item['str']);
				elif item['label'] == 'TimeDD':
					ret = self.calc_timedd_stc(item,struct,time_conf);
				else:
					time_lamda.append(item);
					ret = False;
			if len(time_lamda) == 0 and struct.has_key('TimeLamda'):
				del struct['TimeLamda'];
			else:
				struct['TimeLamda'] = time_lamda;
			if time_conf['time_fill'] == True and ret == True:
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

	def calc_timen_stc(self,item,struct,time_lamda):
		if item['func']['type'] == "JIEJIARI" or item['func']['type'] == "JIEQI":
			date = item['func']['date'];
			struct['TimeParse']['month'] = int(date.split('/')[0]);
			struct['TimeParse']['day'] = int(date.split('/')[1]);
			struct['TimeParse']['strs'].append(item['str']);
			if item['func'].has_key('year_type'):
				struct['TimeParse']['year_type'] = item['func']['year_type'];
		elif item['func']['type'] == "ONEDAY":
			 struct['TimeParse'][item['func']['scope']] = item['func']['region'];
			 struct['TimeParse']['strs'].append(item['str']);
			 if item['func']['region'][0] > 12:
			 	struct['TimeParse']['hour_flag'] = 12;
			 else:
			 	struct['TimeParse']['hour_flag'] = 0;
		elif item['func']['type'] == 'JIJIE':
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
			return False;
		return True;
	
	def calc_timec_stc(self,item,struct,time_lamda):
		for iitem in item['list']:
			if iitem['label'] == 'TimeN' and iitem.has_key('func'):
				if iitem['func']['type'] == "JIEJIARI" or iitem['func']['type'] == "JIEQI":
					date = iitem['func']['date'];
					struct['TimeParse']['month'] = int(date.split('/')[0]);
					struct['TimeParse']['day'] = int(date.split('/')[1]);
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
		return True;
	
	def calc_time_stc(self,item,struct,time_lamda):
		#解析小时级别
		p = re.compile(u'[时点]');
		amatch = p.search(item['str']);
		if not amatch is None:
			hour = item['num'].pop(0);
			if struct['TimeParse'].has_key('hour_flag'):
				struct['TimeParse']['hour'] = int(hour['value']) + struct['TimeParse']['hour_flag'];
			else:
				struct['TimeParse']['hour'] = int(hour['value']);
		#解析分钟级别
		p = re.compile(u'[分]');
		amatch = p.search(item['str']);
		if not amatch is None:
			minute = item['num'].pop(0);
			struct['TimeParse']['minute'] = int(minute['value']);
		#解析秒级别
		p = re.compile(u'[秒]');
		amatch = p.search(item['str']);
		if not amatch is None:
			second = item['num'].pop(0);
			struct['TimeParse']['second'] = int(second['value']);
		struct['TimeParse']['strs'].append(item['str']);
		return True;

	def calc_date_stc(self,item,struct,time_lamda):
		#解析年级别
		p = re.compile(u'年');
		amatch = p.search(item['str']);
		if not amatch is None:
			year = item['num'].pop(0);
			struct['TimeParse']['year'] = int(year['value']);
		#解析月级别
		p = re.compile(u'月');
		amatch = p.search(item['str']);
		if not amatch is None:
			month = item['num'].pop(0);
			struct['TimeParse']['month'] = int(month['value']);
		#解析日级别
		p = re.compile(u'[日号]');
		amatch = p.search(item['str']);
		if not amatch is None:
			day = item['num'].pop(0);
			struct['TimeParse']['day'] = int(day['value']);
		struct['TimeParse']['strs'].append(item['str']);
		return True;

	def calc_timeset_stc(self,item,struct,time_conf):
		if time_conf.has_key('time_origin') and time_conf['time_fill'] == True:
			if struct['TimeParse'].has_key('dir'):
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
				(struct['TimeParse']['year'],struct['TimeParse']['month'],struct['TimeParse']['day']) \
					= TCalendarTool.GetWeekDay(
						int(struct['TimeParse']['year']),
						int(struct['TimeParse']['month']),
						int(struct['TimeParse']['day']),
						int(item['num'].pop()['value'])
					);
				if struct['TimeParse']['dir']['dir'] == 'prev':
					struct['TimeParse']['day'] = struct['TimeParse']['day'] - 7 * struct['TimeParse']['dir']['times'];
				else:
					struct['TimeParse']['day'] = struct['TimeParse']['day'] + 7 * struct['TimeParse']['dir']['times'];
				struct['TimeParse']['strs'].append(item['str']);
				del struct['TimeParse']['dir'];
				return True;
		return False;
	def calc_timerel_stc(self,item,struct,time_conf):
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
				tstr = big+item['str'];
				while True:
					index = struct['text'].find(tstr);
					if index == -1: break;
					print func['func'];
					if func['func'] == 'prev' or func['func'] == 'prev2':
						struct['TimeParse'][func['scope']] = struct['TimeParse'][func['scope']] - 1;
					else:
						struct['TimeParse'][func['scope']] = struct['TimeParse'][func['scope']] + 1;
					tstr = big + tstr;
					struct['TimeParse']['strs'].append(big);
			struct['TimeParse']['strs'].append(item['str']);
			return True;
		return False;
	def calc_timed_stc(self,item,struct,time_conf):
		#print common.print_dic(item);
		if struct['TimeParse'].has_key('dir'):
			if item['type'] == 'Normal':
				if time_conf.has_key('time_origin'):
					time_stc = time.localtime(time_conf['time_origin']);
					func = item['func'];
					value = item['num'].pop()['value'];
					if  struct['TimeParse']['dir']['dir'] == 'prev':
						struct['TimeParse'][func['scope']] = \
							[time_stc[date_index[func['scope']]] - int(value),time_stc[date_index[func['scope']]]];
					elif struct['TimeParse']['dir']['dir'] == 'next':
						struct['TimeParse'][func['scope']] = \
							[time_stc[date_index[func['scope']]],time_stc[date_index[func['scope']]] + int(value)];
				struct['TimeParse']['strs'].append(item['str']);
				return True;
		return False;

	def calc_timedd_stc(self,item,struct,time_conf):
		#print common.print_dic(item);
		if item['type'] == 'Normal':
			mydir = item['dir'];
			if not self.data.has_key(mydir['type']): return False;
			mdata = self.data[mydir['type']];
			for idata in mdata:
				p = re.compile(idata['reg']);
				amatch = p.search(mydir['str']);
				if amatch is None: continue;
				mydir['func'] = idata;
				break;
			if not mydir.has_key('func'): return False;

			mydir['times'] = 0;
			for tdd in mydir['str']:
				mydir['times'] = mydir['times'] + 1;

			if time_conf.has_key('time_origin'):
				time_stc = time.localtime(time_conf['time_origin']);
				func = item['func'];
				value = item['num'].pop()['value'];
				if mydir['func']['dir'] == 'prev':
					struct['TimeParse'][func['scope']] = time_stc[date_index[func['scope']]] - int(value);
					struct['TimeParse']['type'] = 'past';
				elif mydir['func']['dir'] == 'next':
					struct['TimeParse'][func['scope']] = time_stc[date_index[func['scope']]] + int(value);
					struct['TimeParse']['type'] = 'future';
				struct['TimeParse']['strs'].append(item['str']);
				struct['TimeParse']['strs'].append(mydir['str']);
				return True;
		return False;
	#重新修复分词的结果通过匹配的词语
	def reseg_text(self,struct):
		if struct.has_key('TimeParse') and struct['TimeParse'].has_key('strs'):
			istr = struct['TimeParse']['strs'];
			reg = ' *'.join(istr);
			value = ''.join(istr);
			amatch = re.findall(reg,struct['seg_text']);
			for tstr in amatch:
				if len(tstr) == 0: continue;
				struct['seg_text'] = struct['seg_text'].replace(tstr,value,1);

	def prev_num2text(self,item):
		tstr = item['str'];
		if not item.has_key('num'): return tstr;
		for inum in item['num']:
			tstr = tstr.replace(inum['value'],inum['label'],1);
		return tstr;


	def repair_time(self,struct):
		if struct.has_key('TimeParse'):
			if struct['TimeParse'].has_key('year') and type(struct['TimeParse']['year']) == list: return;
			if struct['TimeParse'].has_key('month') and type(struct['TimeParse']['month']) == list: return;
			if struct['TimeParse'].has_key('day') and type(struct['TimeParse']['day']) == list: return;
			if struct['TimeParse'].has_key('hour') and type(struct['TimeParse']['hour']) == list: return;
			if struct['TimeParse'].has_key('minute') and type(struct['TimeParse']['minute']) == list: return;
			if struct['TimeParse'].has_key('second') and type(struct['TimeParse']['second']) == list: return;
			TimeCommon._make_sure_time(struct['TimeParse']);
