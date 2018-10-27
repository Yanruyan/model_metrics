###################################################
# desc : calculate mAUC( group by <uuid,session_id> )
# author : qiangz2012@yeah.net
##################################################

def pre_rank(x):
	sorted_x = sorted(zip(x,range(len(x))))
	r = [0 for k in x]
	cur_val = sorted_x[0][0]
	last_rank = 0
	for i in list( range(len(sorted_x)) ):
		if cur_val != sorted_x[i][0]:
			cur_val = sorted_x[i][0]
			for j in list( range(last_rank, i) ):
				r[sorted_x[j][1]] = float(last_rank+1+i)/2.0
			last_rank = i
		if i==len(sorted_x)-1:
			for j in list( range(last_rank, i+1) ): 
				r[sorted_x[j][1]] = float(last_rank+i+2)/2.0
	return r

def cal_auc( y_actual, y_pred ):
	r = pre_rank(y_pred)
	num_positive = len([0 for x in y_actual if x==1])
	num_negative = len(y_actual)-num_positive
	sum_positive = sum([r[i] for i in list(range(len(r))) if y_actual[i]==1])
	auc = ((sum_positive - num_positive*(num_positive+1)/2.0) / (num_negative*num_positive))
	return auc

def cal_mauc( groupId, y_actual, y_pred ):
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
	# calculate mean AUC
	sumAUC = 0.0
	cnt = 0
	for gid in gLabel.keys():
		groupLabel = gLabel[gid]
		groupPred = gPred[gid]
		groupAUC = cal_auc( groupLabel, groupPred )
		cnt += 1
		sumAUC += groupAUC
	return (sumAUC/(cnt*1.0))
	
