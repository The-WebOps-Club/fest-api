import os 

def viewset_response(message,data):
	temp={}	
	temp['status']=0
	temp['message']=message
	temp['data']=data	
	if not message:
		temp['status']=1
		temp['message']='success'
	return temp

def handle_uploaded_file(f, fname):
	os.makedirs(os.path.dirname(fname)) # Create directories in path
	with open(fname, 'wb+') as destination: # save it
		for chunk in f.chunks():
			destination.write(chunk)
