###################################################
# desc : calculate MAP( group by <uuid,session_id> )
# author : zhangqiang44@meituan.com
##################################################

def cal_ap( y_actual, y_pred, k ):
	topK = min( len(y_pred), k )
	# sort by pred
	l_zip = list(zip(y_actual,y_pred))
	s_zip = sorted( l_zip, key=lambda x: x[1], reverse=True )
	# topk of rank result
	s_zip_topk = s_zip[:topK]
	num = 0
	rank = 0
	sumP = 0.0
	for item in s_zip_topk:
		rank += 1
		if item[0] == 1:
			num += 1
			sumP += (num*1.0)/(rank*1.0)
	ap = 0.0
	if num > 0:
		ap = sumP/(num*1.0)
	return ap	

def cal_map( groupId, y_actual, y_pred, k=10 ):
	# group
	gLabel = {}
	gPred = {}
	for i in list(range(len(groupId))):
		gid = groupId[i]
		label = y_actual[i]
		pred = y_pred[i]
		if gid not in gLabel:
			gLabel[gid] = []
			gPred[gid] = []
		gLabel[gid].append(label)
		gPred[gid].append(pred)
	# calculate mAP
	sumAP = 0.0
	cnt = 0
	for gid in gLabel.keys():
		groupLabel = gLabel[gid]
		groupPred = gPred[gid]
		AP = cal_ap( groupLabel, groupPred, k )
		cnt += 1
		sumAP += AP
	return (sumAP/(cnt*1.0))
	
	
