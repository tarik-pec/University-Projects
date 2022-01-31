#Tarik Pecaninovic 

import numpy as np

def abs_state_check(curr_state):
    
    curr_state_extended = curr_state[:]
    curr_state_extended.append(curr_state[0])
    
    abs_state_flag = True
    
    for i in range(0,len(curr_state)-1):
        if curr_state_extended[i] != curr_state_extended[i-1] and curr_state_extended[i] != curr_state_extended[i+1]:
            abs_state_flag = False
    return abs_state_flag

#abs_state_check test:
#print(abs_state_check([0,1,1,0,0,0,1]))

def decision(curr_state,i,j):
    #if elements are equal, don't swap
    if curr_state[i] == curr_state[j]:
        return False
    
    curr_state_extended = curr_state[:]
    curr_state_extended.append(curr_state[0])

    i_happy_check = happy_check(curr_state,i)
    j_happy_check = happy_check(curr_state,j)

    #if both vertices happy; don't swap
    if i_happy_check and j_happy_check:
        I_decide = False
    #o/w at least one is unhappy.
    #if i happy, then j unhappy. check if i stays happy and j becomes happy (or vice versa).
    elif i_happy_check or j_happy_check:
        test = np.copy(curr_state)
        test[i] = curr_state[j]
        test[j] = curr_state[i]
        if happy_check(test,i) and happy_check(test,j):
            I_decide = True
        else:
            I_decide = False
    #o/w both unhappy
    else:
        test = np.copy(curr_state)
        test[i] = curr_state[j]
        test[j] = curr_state[i]
        if happy_check(test,i) or happy_check(test,j):
            I_decide = True
        else:
            I_decide = False

            
    return I_decide

#decision test:
#print(decision([1,1,0,1,0,0],2,3))

#checks to see if vertex is happy
def happy_check(curr_state,i):
    curr_state_extended = curr_state[:]
    curr_state_extended = list(curr_state_extended)
    curr_state_extended.append(curr_state[0])
    
    if curr_state_extended[i] != curr_state_extended[i-1] and curr_state_extended[i] != curr_state_extended[i+1]:
        happy_flag = False
    else:
        happy_flag = True
    return happy_flag

#happy check test:
#test = np.array([1,0,1,0])
#print(happy_check(test,1))


def monte_abs_time(n,no_of_iters):

    abs_times = []
    for _ in range(no_of_iters):
        #create random (non-absorbing)start state
        curr_state = [0 for _ in range(n)]
        type1_indicies = np.random.choice(n,n//2,replace = False)
        for i in type1_indicies:
            curr_state[i] = 1
        while abs_state_check(curr_state):
            curr_state = [0 for _ in range(n)]
            type1_indicies = np.random.choice(n,n//2,replace = False)
            for i in type1_indicies:
                curr_state[i] = 1

        #move between states (by swapping vertices) until absorption state is reached
        time = 0
        while not abs_state_check(curr_state):
            #pick two vertices. if decision to swap is 'yes', swap those vertices. o/w repeat.
            i,j = np.random.choice(n,2,replace=False)
            if decision(curr_state,i,j):
                curr_state[i] , curr_state[j] = curr_state[j] , curr_state[i]
            time +=1
            

        #add found absorption time to list
        abs_times.append(time)

    return np.sum(abs_times)/float(no_of_iters)


print('Monte Carlo Absorption Times:')
for i in range(4,11):
    print(monte_abs_time(i,1000)),'n=' + str(i)
