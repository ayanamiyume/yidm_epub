import os,multiprocessing,time
def worker():
	os.system('python run.py')
	worker()

if __name__=='__main__':
	p1=multiprocessing.Process(target=worker,args=())
	p2=multiprocessing.Process(target=worker,args=())
	p3=multiprocessing.Process(target=worker,args=())
	p4=multiprocessing.Process(target=worker,args=())
	p5=multiprocessing.Process(target=worker,args=())



	p1.start()
	time.sleep(2)
	p2.start()
	time.sleep(2)
	p3.start()
	time.sleep(2)
	p4.start()
	time.sleep(2)
	p5.start()



	p1.join()
	p2.join()
	p3.join()
	p4.join()
	p5.join()
