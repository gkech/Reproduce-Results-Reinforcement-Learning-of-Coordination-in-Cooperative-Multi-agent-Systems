##Georgios Kechagias
##Test final_mas.py, Same Directory
##1000 Experiments Results Evaluation and plots
##
##
import final_mas
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline

def check_table7(count):

	for i in range(0,1000):
		result=final_mas.main()
			
		if(np.argmax(result)==0):
			count[0]=count[0]+1
		elif(np.argmax(result)==1):
			count[1]=count[1]+1
		elif(np.argmax(result)==2):
			count[2]=count[2]+1
		elif(np.argmax(result)==3):
			count[3]=count[3]+1
		elif(np.argmax(result)==4):
			count[4]=count[4]+1
		elif(np.argmax(result)==5):
			count[5]=count[5]+1
		elif(np.argmax(result)==6):
			count[6]=count[6]+1
		elif(np.argmax(result)==7):
			count[7]=count[7]+1
		elif(np.argmax(result)==8):
			count[8]=count[8]+1
	return count

def plot_me(exps):
	#for printing
	result=final_mas.main()
	
	##PLOT CODE
	plt.ylim(0.0,1.03,0.1)
	plt.xlim(500,2000,1)
	t = np.arange(0, exps+1, 1)
	xnew = np.linspace(t.min(),t.max(),300)
	power_smooth = spline(t,result,xnew)
	plt.plot(xnew,power_smooth,'r',label= 'FMQ(c=5)')
	plt.legend(loc=4)
	plt.show()

count=np.zeros(9)
exps=2000

if __name__ == '__main__':
    # and here we test
    # do some testing..abAout 1000times func
	##
	##before uncomment, remember to change the return from script final_mas.py
	##
	
	##table 7 results - default option
	print check_table7(count)

	##plots preview
	#plot_me(exps)
