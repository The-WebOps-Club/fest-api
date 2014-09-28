
def viewset_response(message,data):
	temp={}	
	temp['status']=0
	temp['message']=message
	temp['data']=data	
	if not message:
		temp['status']=1
		temp['message']='success'
	return temp
