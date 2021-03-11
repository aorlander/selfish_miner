import random


#The Simulate function simulates the selfish miners strategy
#Returns the proportion of blocks in the chain that belongs to the selfish miners. 
#The function defines different states of the state machine that is discussed in the slides. 
#Your task is to update different variables that show the length of the blockchain and 
#SelfishRevenue that presents the revenue of the selfish mining pool in each state.


#alpha: selfish miners mining power (percentage),
#gamma: the ratio of honest miners choose to mine on the selfish miners pool's block
#N: number of simulations run
def Simulate(alpha,gamma,N, seed):
    
    # DO NOT CHANGE. This is used to test your function despite randomness
    random.seed(seed)
  
    #the same as the state of the state machine in the slides 
    state=0
    # the length of the blockchain
    ChainLength=0
    # the revenue of the selfish mining pool
    SelfishRevenue=0

    hidden=0

    #A round begin when the state=0
    for i in range(N):
        r=random.random()
        #print("ROUND", i)
        #print("before: state=", state, "// hidden=", hidden, " // chain length=", ChainLength, " // selfish revenue=", SelfishRevenue)

        if state==0: 
            #print("state 0")
            #The selfish pool has 0 hidden block.
            if r<=alpha:
                #print("selfish pool found a block")
                #The selfish pool mines a block.
                #They don't publish it. 
                hidden=1
                state=1
            else:
                #print("honest miner found a block")
                #The honest miners found a block.
                #The round is finished : the honest miners found 1 block and the selfish miners found 0 block.
                ChainLength+=1
                state=0

        elif state==1: #lead is 1
            #The selfish pool has 1 hidden block.
            if r<=alpha:
                #print("selfish pool found a block")
                #The selfish miners found a new block.
                #Pool appends one block to its private branch, increasing its lead on the public branch by 1. 
                #Revenue will be determined later.
                hidden=2
                state=2
            else:
                #print("honest miner found a block")
                #The honest miners found a block. 
                #Currently there are two branches of length 1. Pool publishes its single secret block. 
                #Revenue will be determined later.
                ChainLength+=1
                hidden=0
                state=-1

        elif state==-1: 
            #There are two branches of length 1 (0' in lecture)
            if r<=alpha:   
                #print("selfish pool found a block")
                # Pool finds a block
                # Pool publishes its secret branch of length 2. Pool obtains revenue of 2.
                ChainLength+=1
                SelfishRevenue+=2
                hidden=0
                state=0
            elif r<=alpha+(1-alpha)*gamma:
                #print("honest miner found a block after pool head")
                # Others find a block after pool head
                # Pool and others each obtain revenue 1
                hidden=0
                ChainLength+=1
                SelfishRevenue+=1
                state=0
            else:
                #print("honest miner found a block after others' head")
                # Others find a block after others' head
                # Pool gets nothing and others obtain a revenue of 2
                ChainLength+=1
                hidden=0
                state=0
            

        elif state==2:
            #The selfish pool has 2 hidden block.
            if r<=alpha: #Pool finds a block so it appends a block to its private branch. Revenue will be determined later.
                #print("selfish pool found a block")
                hidden=3
                state=3
            else:
                print("honest miner found a block")
                #The honest miners found a block.
                #Others find a block (close the gap, lead drops to 1), the pool publishes its private branch and the system drops to a lead of 0
                #Pool obtains revenue of two
                ChainLength+=2
                SelfishRevenue+=2
                hidden=0
                state=0

        elif state>2:
            # If lead > 2 and others win something (decrease the lead), which is still at least 2, they still obtain nothing
            # When the pool sees the new block coming from the public side, it reveals its block at the same height. 
            # Pool reveals the i-th block and obtains a revenue of 1.
            if r<=alpha:
                #print("selfish pool found a block")
                #The selfish miners found a new block
                hidden+=1
                state+=1
            else:
                print("honest miner found a block")
                #The honest miners found a block
                hidden=hidden-1
                ChainLength+=1
                SelfishRevenue+=1
                state=state-1

        #print("after: state=", state, "// hidden=", hidden, " // chain length=", ChainLength, " // selfish revenue=", SelfishRevenue)
        #print(" ------------------------------------------------------------------------------------- ")

    #print(N)
    #print(float(SelfishRevenue)/ChainLength)
    #print(alpha,gamma,N, seed)
    return float(SelfishRevenue)/ChainLength


# The python interpreter actually executes the function body here
#print("Answer: ")
#Simulate(.35,.5,50,20)