import random


def Simulate(alpha,gamma,N, seed):
    
    # DO NOT CHANGE. This is used to test your function despite randomness
    random.seed(seed)
  
    state=0
    ChainLength=0
    SelfishRevenue=0
    hidden=0

    for i in range(N):
        r=random.random()
        #print("ROUND", i)
        #print("before: state=", state, "// hidden=", hidden, " // chain length=", ChainLength, " // selfish revenue=", SelfishRevenue)

        if state==0: 
            #The selfish pool has 0 hidden block.
            if r<=alpha:
                #The selfish pool mines a block.
                #They don't publish it. 
                hidden=1
                state=1
            else:
                #The honest miners found a block.
                #The round is finished : the honest miners found 1 block and the selfish miners found 0 block.
                ChainLength+=1
                state=0

        elif state==1: #lead is 1
            #The selfish pool has 1 hidden block.
            if r<=alpha:
                #The selfish miners found a new block.
                #Pool appends one block to its private branch, increasing its lead on the public branch by 1. 
                #Revenue will be determined later.
                hidden=2
                state=2
            else:
                #The honest miners found a block. 
                #Currently there are two branches of length 1. Pool publishes its single secret block. 
                #Revenue will be determined later.
                ChainLength+=1
                hidden=0
                state=-1


        elif state==-1: 
            #There are two branches of length 1 (0' in lecture)
            if r<=alpha:
                # Pool finds a block
                # Pool publishes its secret branch of length 2. Pool obtains revenue of 2.
                SelfishRevenue+=2
                state = 0
                ChainLength+=1
                hidden=0
            elif r<=alpha+(1-alpha)*gamma:
                # Others find a block after pool head
                # Pool and others each obtain revenue 1
                SelfishRevenue+=1
                state = 0
                ChainLength+=1
                hidden=0
            else:
                # Others find a block after others' head. Pool gets nothing 
                SelfishRevenue+=0
                state = 0
                ChainLength+=1
                hidden=0
 
        elif state==2:
            #The selfish pool has 2 hidden block.
            if r<=alpha: 
                # Pool finds a block so it appends a block to its private branch. Revenue will be determined later.
                hidden=3
                state=3
            else:
                #Others find a block (close the gap), the pool publishes its private branch and the system drops to 0. Pool obtains revenue of two
                ChainLength+=2
                SelfishRevenue+=2
                hidden=0
                state=0

        elif state>2:

            if r<=alpha:
                #The selfish miners found a new block
                hidden+=1
                state+=1
            else:
                #The honest miners found a block
                # When the pool sees the new block coming from the public side, it reveals its block at the same height. 
                # Pool reveals the i-th block and obtains a revenue of 1.
                hidden=hidden-1
                ChainLength+=1
                SelfishRevenue+=1
                state=state-1
                
    
        #print("after: state=", state, "// hidden=", hidden, " // chain length=", ChainLength, " // selfish revenue=", SelfishRevenue)
        #print(" ------------------------------------------------------------------------------------- ")

    #print(N)
    print(float(SelfishRevenue)/ChainLength)
    #print(alpha,gamma,N, seed)
    return float(SelfishRevenue)/ChainLength


# The python interpreter actually executes the function body here
#print("Answer: ")
#Simulate(.35,.5,250,30)
#Simulate(.35,.5,1250,40)
#Simulate(.35,.5,6250,50)
#Simulate(.35, .5, 31250, 60)
#Simulate(.35, .5, 156250, 70)
#Simulate(.35, .5, 781250, 80)