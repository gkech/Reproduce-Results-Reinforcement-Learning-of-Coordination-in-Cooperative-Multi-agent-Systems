#Special Topics in MultiAgnet Systems - 2016 
#Technical University of Crete
#Georgios Kechagias
#2010030002

#Attempt to Reproduce some of the Resutls 
#Reinforcement Learning of Coordination in Cooperative Multi-Agent Systems
#Spiros Kapetanakis - Daniel Kudenko 
#University of York

import random
import math
import numpy

def main():
##FUNCTIONS

	#temperature 
	def temperature(exps,s,max_temp):
		t=math.exp(-s*exps)*max_temp+1
		return t;
		
		
	def get_reward(agnt_1,agnt_2,game):
		reward=game[agnt_1][agnt_2]
		return reward


	def freq_plus_max(action,reward,max_reward,freq_max_reward,count):
		if(reward>max_reward):
			max_reward=reward
			freq_max_reward=0
			return max_reward*(freq_max_reward/count)
		elif(reward==max_reward):
			freq_max_reward=freq_max_reward+1
			return max_reward*(freq_max_reward/count)
		else:
			return max_reward*(freq_max_reward/count)
			
	def q_learning(action,learning_rate,reward,q_agent):
		q_agent[action]=q_agent[action]+learning_rate*(reward-q_agent[action])
		return q_agent

		
	def propability_action(evaluation,t,prob_action):
		sum_evaluation=0
		for act in range(0 ,3):
			sum_evaluation=sum_evaluation+math.exp(evaluation[act]/t)
		
		for act in range(0 ,3):
			prob_action[act]=math.exp(evaluation[act]/t)/sum_evaluation
		return prob_action


	def weighted_choice(weights):
		totals = []
		running_total = 0

		for w in weights:
			running_total += w
			totals.append(running_total)

		rnd = random.random() * running_total
		for i, total in enumerate(totals):
			if rnd < total:
				return i

	##INITIALIZATION
	s=3
	##AGENT1-VECTORS
	q_agent1=numpy.zeros(s) #q-values for agent1
	times_max_reward1=numpy.zeros(s)
	freq_max_reward1=numpy.zeros(s)
	max_reward1=numpy.zeros(s)
	evaluation1=numpy.zeros(s)
	propability_vec1=[0.33333,0.33333,0.33333]
	count1=numpy.zeros(s)
	##
	##AGENT2-VECTORS
	q_agent2=numpy.zeros(s) #q-values for agent2
	times_max_reward2=numpy.zeros(s)
	freq_max_reward2=numpy.zeros(s)
	max_reward2=numpy.zeros(s)
	evaluation2=numpy.zeros(s)
	propability_vec2=[0.33333,0.33333,0.33333]
	count2=numpy.zeros(s)
	##

	#k=num_rand=random.randint(-100, -50)
	k=0

	#the climbing game table
	g_climbing=numpy.array([[11, -30, 0], [-30, 7, 6], [0, 0, 5]])
	#the penalty game table
	g_penalty=numpy.array([[10, 0, k], [0, 2, 0], [k, 0, 10]])
	#
	stocha_list=[14,0]

	s=0.006
	max_temp=500
	exps=1000
	learning_rate=0.9
	c=10
	results=numpy.zeros(exps+1)
	iterations=0
	count=numpy.zeros(9)
	#################################################################
	#################################################################
	##START

	while iterations<exps :
		
		##refresh stochastic reward for (1,1) every turnd
		stocha=numpy.random.choice(stocha_list,p=[0.5,0.5])
		stochastic_g_climbing=numpy.array([[11, -30, 0], [-30, stocha , 6], [0, 0, 5]])
		
		##every agent calls an action
		agent1_action=weighted_choice(propability_vec1)
		agent2_action=weighted_choice(propability_vec2)	
		
		##we track the action routine
		count1[agent1_action]=count1[agent1_action]+1
		count2[agent2_action]=count2[agent2_action]+1
		#default game g_penalty
		#if you wanna chance the game played, replace g_penalty with g_climbing or stochastic_g_climbing
		reward=get_reward(agent1_action,agent2_action,stochastic_g_climbing) 
		#q-values
		q_agent1=q_learning(agent1_action,learning_rate,reward,q_agent1)
		q_agent2=q_learning(agent2_action,learning_rate,reward,q_agent2)
		
		#temperature calculation
		temper=temperature(iterations,s,max_temp)

		if(reward>max_reward1[agent1_action]):
			max_reward1[agent1_action]=reward
			freq_max_reward1[agent1_action]=freq_max_reward1[agent1_action]+1
			times_max_reward1[agent1_action]= max_reward1[agent1_action]*(freq_max_reward1[agent1_action]/count1[agent1_action])
		elif(reward==max_reward1[agent1_action]):
			freq_max_reward1[agent1_action]=freq_max_reward1[agent1_action]+1
			times_max_reward1[agent1_action]= max_reward1[agent1_action]*(freq_max_reward1[agent1_action]/count1[agent1_action])
		else:
			times_max_reward1[agent1_action]= max_reward1[agent1_action]*(freq_max_reward1[agent1_action]/count1[agent1_action])

		if(reward>max_reward2[agent2_action]):
			max_reward2[agent2_action]=reward
			freq_max_reward2[agent2_action]=freq_max_reward2[agent2_action]+1
			times_max_reward2[agent2_action]= max_reward2[agent2_action]*(freq_max_reward2[agent2_action]/count2[agent2_action])
		elif(reward==max_reward2[agent2_action]):
			freq_max_reward2[agent2_action]=freq_max_reward2[agent2_action]+1
			times_max_reward2[agent2_action]= max_reward2[agent2_action]*(freq_max_reward2[agent2_action]/count2[agent2_action])
		else:
			times_max_reward2[agent2_action]= max_reward2[agent2_action]*(freq_max_reward2[agent2_action]/count2[agent2_action])
			
		#evaluation calculations
		evaluation1[agent1_action]=q_agent1[agent1_action]+c*times_max_reward1[agent1_action]
		evaluation2[agent2_action]=q_agent2[agent2_action]+c*times_max_reward2[agent2_action]

		#propability calculations, useful for the next interation actions
		propability_vec1=propability_action(evaluation1,temper,propability_vec1)
		propability_vec2=propability_action(evaluation2,temper,propability_vec2)
		
		##freq factor bundle
		iterations=iterations+1 #loop counter
		if(agent1_action==0) and (agent2_action==0): 	# Agent1=0 - Agent2=0
			count[0]=count[0]+1
		elif (agent1_action==1) and (agent2_action==1): # Agent1=1 - Agent2=1
			count[1]=count[1]+1
		elif (agent1_action==2) and (agent2_action==2): # Agent1=2 - Agent2=2
			count[2]=count[2]+1
		elif (agent1_action==0) and (agent2_action==1): # Agent1=0 - Agent2=1
			count[3]=count[3]+1
		elif (agent1_action==1) and (agent2_action==0): # Agent1=1 - Agent2=0
			count[4]=count[4]+1
		elif (agent1_action==0) and (agent2_action==2): # Agent1=0 - Agent2=2
			count[5]=count[5]+1
		elif (agent1_action==2) and (agent2_action==0): # Agent1=2 - Agent2=0
			count[6]=count[6]+1
		elif (agent1_action==1) and (agent2_action==2): # Agent1=1 - Agent2=2
			count[7]=count[7]+1
		elif (agent1_action==2) and (agent2_action==1): # Agent1=2 - Agent2=1
			count[8]=count[8]+1
		
		#results[iterations]=propability_vec1[0]							##plot results for climbing
		#results[iterations]=propability_vec1[0]+propability_vec1[2]	##plot results for penalty

	#return results # uncomment for plots
	return count  #uncomment for table 7 results


