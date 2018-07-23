#!/usr/bin/python
#-*- coding:utf-8 -*-
import time,math

month = [31,31,28,31,30,31,30,31,31,30,31,30,31];
leap_mon = [31,31,29,31,30,31,30,31,31,30,31,30,31];

#time['year','month','day','hour','min','sec','week','week_idx','is-enable']

tmenu = {
	'enable':8,
	'week_idx':7,
	'week':6,
	'sec':5,
	'min':4,
	'hour':3,
	'day':2,
	'month':1,
	'year':0
};
def _list_copy(l1,l2,idb,flg = False):
	tlist = list()
	tlist.extend(l1);
	for idx,value in enumerate(l2):
		if tlist[idx] <> 'null' and value <> 'null' and flg == False:
			tlist[idx] = tlist[idx] + value;
		elif tlist[idx] <> 'null' and value <> 'null':
			tlist[idx] = value;
		if value <> 'null': tlist[idx] = value;
		if idb <= idx: break;
	return tlist;

def _list_empty_copy(l1,l2,idb,flg = False):
	tlist = list()
	tlist.extend(l1);
	for idx,value in enumerate(l2):
		if idb <= idx: break;
		if tlist[idx] <> 'null':
			continue;
		else:
			tlist[idx] = value;
	return tlist;

def _create_null_time():
	return ['null','null','null','null','null','null','null','null','null'];

def _is_merge_able(st,et,fal = False):
	if not st.has_key('stime'): return None;
	if not et.has_key('stime'): return None;
	if fal == False and st['scope'] == et['scope']: return None;

	stime = _list_copy(st['stime'],et['stime'],8,fal);
	etime = _list_copy(st['stime'],et['etime'],8,fal);
	return [stime,etime];

def _get_time_stamp(t_time):
	tupletime = list(t_time);
	if tupletime[0] == 'null': return 0;
	if tupletime[1] == 'null': tupletime[1] = 0;
	if tupletime[2] == 'null': tupletime[2] = 0;
	if tupletime[3] == 'null': tupletime[3] = 0;
	if tupletime[4] == 'null': tupletime[4] = 0;
	if tupletime[5] == 'null': tupletime[5] = 0;
	if tupletime[6] == 'null': tupletime[6] = 0;
	if tupletime[7] == 'null': tupletime[7] = 0;
	if tupletime[8] == 'null': tupletime[8] = 0;
	while len(tupletime) < 9: tupletime.append(0);
	return time.mktime(tupletime);

def time_from_stamp(stamp):
	time_tuple = time.localtime(stamp);
	return time_tuple;

def _make_sure_time(mytime):
	#print 'start repiar time';
	if mytime.has_key('second') and mytime.has_key('minute'):
		if mytime['second'] < 0:
			mytime['minute'] -= (math.fabs(mytime['second']) // 60 + 1);
			mytime['second'] = 60 - math.fabs(mytime['second']) % 60;
		if mytime['second'] >= 60:
			mytime['minute'] += (math.fabs(mytime['second']) // 60);
			mytime['second'] = math.fabs(mytime['second']) % 60;

	if mytime.has_key('minute') and mytime.has_key('hour'):
		if mytime['minute'] < 0:
			mytime['hour'] -= (math.fabs(mytime['minute']) // 60 + 1);
			mytime['minute'] = 60 - math.fabs(mytime['minute']) % 60;
		if mytime['minute'] >= 60:
			mytime['hour'] += (math.fabs(mytime['minute']) // 60);
			mytime['minute'] = math.fabs(mytime['minute']) % 60;

	if mytime.has_key('hour') and mytime.has_key('hour'):
		if mytime['hour'] < 0:
			mytime['day'] -= (math.fabs(mytime['hour']) // 24 + 1);
			mytime['hour'] = 24 - math.fabs(mytime['hour']) % 24;
		if mytime['hour'] >= 24:
			mytime['day'] += (math.fabs(mytime['hour']) // 24);
			mytime['hour'] = math.fabs(mytime['hour']) % 24;
	#计算日期需要知道是否 是瑞年

	if not mytime.has_key('year'): return;
	mymonth = month;
	if _is_leap_year(mytime['year']) == True:
		mymonth = leap_mon;

	if mytime.has_key('day') and mytime.has_key('month'):
		mymon = mytime['month'] % 12;
		while mytime['day'] <= 0:
			mytime['day'] = mytime['day'] + mymonth[mymon - 1];
			mytime['month'] = mytime['month'] - 1;
			if mymon == 0: mymon = 12;
			else: mymon = mymon - 1;

		mymon = mytime['month'] % 12;
		while mytime['day'] > mymonth[mymon]:
			mytime['day'] = mytime['day'] - mymonth[mymon];
			mytime['month'] = mytime['month'] + 1;
			mymon = mymon + 1;

	if mytime.has_key('month') and mytime.has_key('year'):
		while mytime['month'] <= 0:
			mytime['month'] = mytime['month'] + 12;
			mytime['year'] = mytime['year'] - 1;
		while mytime['month'] > 12:
			mytime['month'] = mytime['month'] - 12;
			mytime['year'] = mytime['year'] + 1;

def _is_leap_year(myyear):
	if myyear % 400 == 0 or (myyear % 4 == 0 and myyear % 100 <> 0):
		return True;
	return False;

