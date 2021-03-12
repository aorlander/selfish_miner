import random


def Simulate(alpha,gamma,N, seed):
    random.seed(seed)
    state=0
    ChainLength=0
    SelfishRevenue=0

    for i in range(N):
        r=random.random()
        #print("ROUND", i)
        #print("before: state=", state, " // chain length=", ChainLength, " // selfish revenue=", SelfishRevenue)

        if state==0: #Pool has 0 hidden block.
            if r<=alpha: #Pool finds a block and appends to private branch. Revenue determined later.
                state=1
                #print("pool finds a block")
            else: #Others find a block. The round is finished : the honest miners found 1 block and the selfish miners found 0 block.
                ChainLength+=1
                state=0
                #print("others find a block")

        elif state==1: #Pool has 1 hidden block. 
            if r<=alpha: #Pool finds a block and appends to private branch. Revenue determined later.
                state=2
                #print("pool finds a block")
            else: #Others find a block. Currently there are two branches of length 1. Pool publishes its single secret block. Revenue determined later.
                #ChainLength+=1
                state=-1
                #print("others find a block")

        elif state==-1: #Two branches of length 1 
            if r<=alpha: #Pool finds a block on its previously private branch. Pool publishes its private branch of length 2. Pool obtains revenue of 2.
                SelfishRevenue+=2
                ChainLength+=2
                state = 0
                #print("pool finds a block")
            elif r<=alpha+(1-alpha)*gamma: # Others find a block on a previously private branch. Pool obtains revenue of 1.
                SelfishRevenue+=1
                ChainLength+=2
                state = 0
                #print("others find a block after pool head")
                #Both honest and selfish miners start mining on the new head
            else: #Others find a block on the public branch. Pool gets nothing. 
                SelfishRevenue+=0
                ChainLength+=2
                state = 0
                #print("NO PRIVATE BRANCH")
                #print("others find a block after others' head")
        
            

        elif state==2: #Pool has 2 hidden block.
            if r<=alpha: #Pool finds a block and appends to private branch. Revenue determined later.
                state=3
                #print("pool finds a block")
            else: #Others find a block. Pool publishes its private branch and the system drops to 0. Pool obtains revenue of 2.
                ChainLength+=2
                SelfishRevenue+=2
                state=0
                #print("others find a block")

        elif state>2: #Pool has >2 hidden block.
            if r<=alpha: #Pool finds a block and appends to private branch. Revenue determined later.
                state+=1
                #print("pool finds a block")
            else: #Others find a block. Pool reveals its block at the same height. Pool obtains revenue of 1.
                ChainLength+=1
                SelfishRevenue+=1
                state=state-1
                #print("others find a block")
                
        #print("state=", state, " // chain length=", ChainLength, " // selfish revenue=", SelfishRevenue)
        #print(" ----------------------------------- ")

    print(float(SelfishRevenue)/ChainLength)
    return float(SelfishRevenue)/ChainLength



#Simulate(.35,.5,20,30)
#Simulate(.35,.5,250,30)
#Simulate(.35,.5,1250,40)
#Simulate(.35,.5,6250,50)
#Simulate(.35, .5, 31250, 60)
#Simulate(.35, .5, 156250, 70)
#Simulate(.35, .5, 781250, 80)