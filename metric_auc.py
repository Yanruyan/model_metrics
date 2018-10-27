############################################
# desc : calculate AUC
# author : qiangz2012@yeah.net
############################################

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

#if __name__ == "__main__":
#	y_actual = [0,1,1,0,0,1,1]
#	y_pred = [0.3,0.5,0.5,0.5,0.5,0.7,0.8]
#	auc = cal_auc( y_actual, y_pred )
#	print(auc)

