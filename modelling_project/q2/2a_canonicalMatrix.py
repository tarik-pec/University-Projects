#Tarik Pecaninovic


import numpy as np

def canonicalMat(markov):
    markov = np.array(markov)
    #finds all the absorbing states by looking for '1' on the main diagonal
    absorbing_states = []
    for i in range(len(markov)):
        if markov[i][i] == 1:
            absorbing_states.append(i)

    k = len(markov)-1
    for i in range(len(absorbing_states)-1,-1,-1):
        #absorbing states to correct row then the '1' to correct column
        markov[[absorbing_states[i],k]] = markov[[k,absorbing_states[i]]]
        markov[:,[absorbing_states[i],k]] = markov[:,[k,absorbing_states[i]]]
        k -= 1

        
    return markov



transition_Mat_4 = [[1,0,0,0,0,0],
        [0,1,0,0,0,0],
        [0,0,1,0,0,0],
        [0,0,0,1,0,0],
        [float(1)/6,float(1)/6,float(1)/6,float(1)/6,float(2)/6,0],
        [float(1)/6,float(1)/6,float(1)/6,float(1)/6,0,float(2)/6]]

print(canonicalMat(transition_Mat_4)),'n=4'


alpha = 1.0/10
beta = 6.0/10
transition_Mat_5 = [ [1,0,0,0,0,0,0,0,0,0],
                     [0,1,0,0,0,0,0,0,0,0],
                     [0,0,1,0,0,0,0,0,0,0],
                     [0,0,0,1,0,0,0,0,0,0],
                     [0,0,0,0,1,0,0,0,0,0],
                     [alpha,alpha,0,alpha,alpha,beta,0,0,0,0],
                     [alpha,alpha,alpha,0,alpha,0,beta,0,0,0],
                     [alpha,alpha,alpha,alpha,0,0,0,beta,0,0],
                     [0,alpha,alpha,alpha,alpha,0,0,0,beta,0],
                     [alpha,0,alpha,alpha,alpha,0,0,0,0,beta]]
print(canonicalMat(transition_Mat_5)),'n=5'
