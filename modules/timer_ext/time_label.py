#!/usr/bin/python
#-*- coding:utf-8 -*-
import os,sys,re,common
from time_base import TimeBase
#标记对象以及链接的网络
class TimeLabel(TimeBase):

	def encode(self,struct,time_conf):
		try:
			if not struct.has_key('SomeNum'): return False;
			if not struct.has_key('TimeLabel'):
				struct['TimeLabel'] = list();
			struct['tmp_text'] = struct['text'];
			#标记时间信息前 处理数字组合
			#先匹配汉字时间词语，不然会有冲突 比如七夕节 - 7数字会被特殊处理而造成错误匹配
			self.mark_objs_text(struct);
			self.prev_num2text(struct);
			self.mark_time_label(struct);
			self.mark_timeln_text(struct);
#			self.mark_objs_text(struct);
			#重新处理一遍分词结果
			self.reseg_text(struct);
			return;
			#根据分词排序TimeLabel
			self.sort_label(struct);
			if struct.has_key('tmp_text'):
				del struct['tmp_text']
			#寻找TimeN+TimeN的组合
			self.mark_timec_label(struct);
			#再次修复分词和排序
			self.reseg_text(struct);
			self.sort_label(struct);
		except Exception as e: raise e;

	def mark_time_label(self,struct):
		for key in self.data.keys():
			if not key == 'Date' and not key == 'Time' and \
				not key == 'TimeSet' and not key == 'TimeD': continue;
			item = self.data[key];
			if item.has_key('reg'):
				for reg in item['reg']:
					self._match_time_stc(struct,reg,key,item);
			else:
				for ikey in item.keys():
					iitem = item[ikey];
					if iitem.has_key('reg'):
						for reg in iitem['reg']:
							if ikey == 'weekend':
								self._match_weekend_stc(struct,reg,key,iitem);
							else:
								self._match_time_stc(struct,reg,key,iitem);

	def _match_time_stc(self,struct,reg,key,iitem):
		amatch = re.findall(reg,struct['tmp_text']);
		for tstr in amatch:
			if len(tstr) == 0: continue;
			tdic = dict();
			tdic['str'] = tstr;
			tdic['label'] = key;
			tdic['type'] = key;
			if iitem.has_key('type'):
				tdic['type'] = iitem['type'];
			struct['TimeLabel'].append(tdic);
			tdic['num'] = list();
			#D时D分D秒 如果匹配到结果则需要对 词语进行解析恢复数字的本来面目
			tm_str = tstr;
			index = tm_str.find('D');
			while True:
				if index == -1: break;
				for key in struct['SomeNum'].keys():
					item = struct['SomeNum'][key];
					if len(item['start']) <= 0: continue;
					tm_str = tm_str.replace("D",item['value'],1);
					tdic['num'].append(item);
					item['start'].pop();
				index = tm_str.find('D');
			tdic['str'] = tm_str;
			struct['tmp_text'] = struct['tmp_text'].replace(tstr,tm_str,1);

	def _match_weekend_stc(self,struct,reg,key,iitem):
		amatch = re.findall(reg,struct['tmp_text']);
		for tstr in amatch:
			if len(tstr) == 0: continue;
			tdic = dict();
			tdic['str'] = tstr;
			tdic['label'] = key;
			tdic['type'] = key;
			if iitem.has_key('type'):
				tdic['type'] = iitem['type'];
			struct['TimeLabel'].append(tdic);
			tdic['num'] = list();
			#D时D分D秒 如果匹配到结果则需要对 词语进行解析恢复数字的本来面目
			num = dict();
			num['start'] = [];
			num['type'] = 'NUM';
			num['label'] = 'D';
			num['value'] = 7;
			tdic['num'].append(num);

	def mark_objs_text(self,struct):
		try:
			for key in self.data.keys():
				if key == 'Date': continue;
				if key == 'Time': continue;
				if key == 'TimeSet': continue;
				if key == 'TimdD': continue;
				if key == 'TimeLN': continue;
				item = self.data[key];
				if item.has_key('reg'):
					for reg in item['reg']:
						amatch = re.findall(reg,struct['tmp_text']);
						for tstr in amatch:
							if len(tstr) == 0: continue;
							tdic = dict();
							tdic['str'] = tstr;
							tdic['label'] = key;
							tdic['type'] = key;
							if item.has_key('type'):
								tdic['type'] = item['type'];
							struct['TimeLabel'].append(tdic);
							struct['tmp_text'] = struct['tmp_text'].replace(tstr,key,1);
				else:
					for ikey in item.keys():
						iitem = item[ikey];
						if iitem.has_key('reg'):
							for reg in iitem['reg']:
								amatch = re.findall(reg,struct['tmp_text']);
								for tstr in amatch:
									if len(tstr) == 0: continue;
									tdic = dict();
									tdic['str'] = tstr;
									tdic['label'] = key;
									tdic['type'] = key;
									if iitem.has_key('type'):
										tdic['type'] = iitem['type'];
									struct['TimeLabel'].append(tdic);
									struct['tmp_text'] = struct['tmp_text'].replace(tstr,key,1);
		except Exception as e: raise e;

	def mark_timeln_text(self,struct):
		try:
			for key in self.data.keys():
				if not key == 'TimeLN': continue;
				item = self.data[key];
				if item.has_key('reg'):
					for reg in item['reg']:
						amatch = re.findall(reg,struct['tmp_text']);
						for tstr in amatch:
							if len(tstr) == 0: continue;
							tdic = dict();
							tdic['str'] = tstr;
							tdic['label'] = key;
							tdic['type'] = key;
							if item.has_key('type'):
								tdic['type'] = item['type'];
							struct['TimeLabel'].append(tdic);
							struct['tmp_text'] = struct['tmp_text'].replace(tstr,key,1);
				else:
					for ikey in item.keys():
						iitem = item[ikey];
						if iitem.has_key('reg'):
							for reg in iitem['reg']:
								amatch = re.findall(reg,struct['tmp_text']);
								for tstr in amatch:
									if len(tstr) == 0: continue;
									tdic = dict();
									tdic['str'] = tstr;
									tdic['label'] = key;
									tdic['type'] = key;
									if iitem.has_key('type'):
										tdic['type'] = iitem['type'];
									struct['TimeLabel'].append(tdic);
									struct['tmp_text'] = struct['tmp_text'].replace(tstr,key,1);
		except Exception as e: raise e;

	def prev_num2text(self,struct):
		for key in struct['SomeNum'].keys():
			item = struct['SomeNum'][key];
			item['start'] = list();
			index = struct['tmp_text'].find(item['value']);
			while True:
				if index == -1: break;
				item['start'].append(index);
				struct['tmp_text'] = struct['tmp_text'].replace(item['value'],item['label'],1);
				index = struct['tmp_text'].find(item['value']);

	#重新修复分词的结果通过匹配的词语
	def reseg_text(self,struct):
		for item in struct['TimeLabel']:
#			if item['label'] == 'TimeN' or item['label'] == 'Time' or item['label'] == 'REL' \
#				or item['label'] == 'TimeSet' or item['label'] == 'Date' or item['label'] == 'TimeC' \
#				or item['label'] == 'TimeD' or item['label'] == 'RELA' or item['label'] == 'Direct':
				istr = list(item['str']);
				reg = ' *'.join(istr);
				amatch = re.findall(reg,struct['seg_text']);
				for tstr in amatch:
					if len(tstr) == 0: continue;
					struct['seg_text'] = struct['seg_text'].replace(tstr," " + item['str'],1);

	def sort_label(self,struct):
		timelabel = list();
		for istr in struct['seg_text'].split(' '):
			if len(istr) == 0: continue;
			for item in struct['TimeLabel']:
				if istr == item['str']:
					timelabel.append(item);
		if len(timelabel) > 0:
			struct['TimeLabel'] = timelabel;

	def mark_timec_label(self,struct):
		timelabel = list();
		prev_item = None;
		for item in struct['TimeLabel']:
			timelabel.append(item);
			if item['label'] == 'TimeN':
				if not prev_item is None:
					if prev_item['type'] != "ONEDAY" and item['type'] == "ONEDAY":
						tdic = dict();
						tdic['type'] = 'TimeC';
						tdic['label'] = 'TimeC';
						tdic['str'] = prev_item['str'] + item['str'];
						tdic['list'] = [prev_item,item];
						timelabel.pop();
						timelabel.pop();
						timelabel.append(tdic);
					else:
						prev_item = None;
				else:
					prev_item = item;
			else:
				prev_item = None;
		struct['TimeLabel'] = timelabel;
