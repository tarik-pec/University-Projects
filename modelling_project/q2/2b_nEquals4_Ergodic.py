#Tarik Pecaninovic

import numpy as np


#NUMERICALLY

epsilon = 0.01
rho = 1 - 4*epsilon/6.0
gamma = 1-epsilon
transition_matrix = np.array([[rho,0,epsilon/6.0,epsilon/6.0,epsilon/6.0,epsilon/6.0],
        [0,rho,epsilon/6.0,epsilon/6.0,epsilon/6.0,epsilon/6.0],
        [epsilon/6.0,epsilon/6.0,rho,0,epsilon/6.0,epsilon/6.0],
        [epsilon/6.0,epsilon/6.0,0,rho,epsilon/6.0,epsilon/6.0],
        [float(1)*gamma/6,float(1)*gamma/6,float(1)*gamma/6,float(1)*gamma/6,(float(6)-4*gamma)/6,0],
        [float(1)*gamma/6,float(1)*gamma/6,float(1)*gamma/6,float(1)*gamma/6,0,(float(6)-4*gamma)/6]])

numerical_approx_stationary1 = np.linalg.matrix_power(transition_matrix,10000)

lambda_, v = np.linalg.eig(np.transpose(transition_matrix))
numerical_approx_stationary2 = v[:,1]/np.sum(abs(v[:,1]))

print(numerical_approx_stationary1[0]),'Numerical Solution; Power Method'
print(abs(numerical_approx_stationary2)),'Numerical Solution; Eigenvector Method'



#MONTECARLO

def decision(curr_state,i,j,epsilon,curr_prob):
    #if elements are equal, don't swap
    if curr_state[i] == curr_state[j]:
        return [False,curr_prob]
    
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

    u = np.random.rand()
    if u < epsilon:
        #in this case the epsilon check passed and so we undo whatever we decided above
        if I_decide == True:
            #if we've decided to swap above then we were in a transient state and swapping
            #has a probability of 1/6. We then multiply by epsilon bc the check passed
            curr_prob = curr_prob*epsilon*1.0/6
        else:
            #otherwise we decided to stay above. This is either bc we were in an absorbing state
            #(in which case we stay with probability 1) or we were in a transient state
            #(in which case we stay with probability 2/6)
            if curr_state == [1,0,1,0] or curr_state == [0,1,0,1]:
                curr_prob = curr_prob*epsilon*2.0/6
            else:
                curr_prob = curr_prob*1*epsilon
        I_decide = not I_decide

    else:
        if I_decide == True:
            #in this case we decided to swap AND we failed the epsilon check.
            #we swap with a probability of 1/6
            curr_prob = curr_prob*1.0/6
        else:
            #othrewise we're not swapping. if we're in a transient state we stay with prob 2/6
            #otherwise we're in an absorbing state, and we stay with probability 1
            if curr_state == [1,0,1,0] or curr_state == [0,1,0,1]:
                curr_prob = curr_prob*2.0/6
            else:
                curr_prob = curr_prob*1

    
    return [I_decide,curr_prob]

#decision test:
#print(decision([1,1,0,1,0,0],2,3,0.5,1))


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

def path_prob_end(curr_state, curr_path_prob,curr_stat_state_est,epsilon):
    rho = 1-4*epsilon
    gamma = 1-epsilon

    #U
    if curr_state == [1,1,0,0]:
        curr_stat_state_est[0] = curr_stat_state_est[0] + curr_path_prob*rho
        curr_stat_state_est[1] = curr_stat_state_est[1] + curr_path_prob*0
        curr_stat_state_est[2] = curr_stat_state_est[2] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[3] = curr_stat_state_est[3] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[4] = curr_stat_state_est[4] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[5] = curr_stat_state_est[5] + curr_path_prob*epsilon/6.0
        return curr_stat_state_est
    #R
    elif curr_state == [0,1,1,0]:
        curr_stat_state_est[0] = curr_stat_state_est[0] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[1] = curr_stat_state_est[1] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[2] = curr_stat_state_est[2] + curr_path_prob*0
        curr_stat_state_est[3] = curr_stat_state_est[3] + curr_path_prob*rho
        curr_stat_state_est[4] = curr_stat_state_est[4] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[5] = curr_stat_state_est[5] + curr_path_prob*epsilon/6.0
        return curr_stat_state_est
    #D
    elif curr_state == [0,0,1,1]:
        curr_stat_state_est[0] = curr_stat_state_est[0] + curr_path_prob*0
        curr_stat_state_est[1] = curr_stat_state_est[1] + curr_path_prob*rho
        curr_stat_state_est[2] = curr_stat_state_est[2] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[3] = curr_stat_state_est[3] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[4] = curr_stat_state_est[4] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[5] = curr_stat_state_est[5] + curr_path_prob*epsilon/6.0
        return curr_stat_state_est
    #L
    elif curr_state == [1,0,0,1]:
        curr_stat_state_est[0] = curr_stat_state_est[0] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[1] = curr_stat_state_est[1] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[2] = curr_stat_state_est[2] + curr_path_prob*rho
        curr_stat_state_est[3] = curr_stat_state_est[3] + curr_path_prob*0
        curr_stat_state_est[4] = curr_stat_state_est[4] + curr_path_prob*epsilon/6.0
        curr_stat_state_est[5] = curr_stat_state_est[5] + curr_path_prob*epsilon/6.0
        return curr_stat_state_est
    #N
    elif curr_state == [0,1,0,1]:
        curr_stat_state_est[0] = curr_stat_state_est[0] + curr_path_prob*gamma/6.0
        curr_stat_state_est[1] = curr_stat_state_est[1] + curr_path_prob*gamma/6.0
        curr_stat_state_est[2] = curr_stat_state_est[2] + curr_path_prob*gamma/6.0
        curr_stat_state_est[3] = curr_stat_state_est[3] + curr_path_prob*gamma/6.0
        curr_stat_state_est[4] = curr_stat_state_est[4] + curr_path_prob*0
        curr_stat_state_est[5] = curr_stat_state_est[5] + curr_path_prob*(6-4*gamma)/6.0
        return curr_stat_state_est
    #M
    elif curr_state == [1,0,1,0]:
        curr_stat_state_est[0] = curr_stat_state_est[0] + curr_path_prob*gamma/6.0
        curr_stat_state_est[1] = curr_stat_state_est[1] + curr_path_prob*gamma/6.0
        curr_stat_state_est[2] = curr_stat_state_est[2] + curr_path_prob*gamma/6.0
        curr_stat_state_est[3] = curr_stat_state_est[3] + curr_path_prob*gamma/6.0
        curr_stat_state_est[4] = curr_stat_state_est[4] + curr_path_prob*(6-4*gamma)/6.0
        curr_stat_state_est[5] = curr_stat_state_est[5] + curr_path_prob*0
        return curr_stat_state_est

    return True



def monte_stat_probs(n,no_of_iters,epsilon):

    stationary_state_estimates = []
    for _ in range(no_of_iters):
        #find 7 paths which end in state i and add them together to approximate P(i,j)^(10)
        curr_stat_state_est = [0,0,0,0,0,0]
        for _ in range(7):
            curr_path_prob = 1
            curr_state = [1,0,1,0]
            #model a path of length 30 and its corresponding probability of occurring
            for _ in range(22):
                i,j = np.random.choice(n,2,replace=False)
                decisions = decision(curr_state,i,j,epsilon,curr_path_prob)
                swap_check = decisions[0]
                curr_path_prob = decisions[1]
                if swap_check:
                    curr_state[i] , curr_state[j] = curr_state[j] , curr_state[i]
            #use current path prob to find path ending in  each state,then add to current probabilities
            curr_stat_state_est = path_prob_end(curr_state, curr_path_prob,curr_stat_state_est,epsilon)
        stationary_state_estimates.append(curr_stat_state_est)

    #takes average of all estimates of p_{i,j}^(m)
    stationary_solution = [0,0,0,0,0,0]
    for estimate in stationary_state_estimates:
        for i in range(len(estimate)):
            stationary_solution[i] += estimate[i]
    for i in range(0,len(stationary_solution)):
        stationary_solution[i] = stationary_solution[i]/no_of_iters
    return stationary_solution
        




solution = monte_stat_probs(4,100,0.01)
print(solution),'Montecarlo Solution'
