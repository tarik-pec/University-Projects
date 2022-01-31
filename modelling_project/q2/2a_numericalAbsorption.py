#Tarik Pecaninovic

import numpy as np


# N=4 CASE:
transition_Mat_4 = [[1,0,0,0,0,0],
        [0,1,0,0,0,0],
        [0,0,1,0,0,0],
        [0,0,0,1,0,0],
        [float(1)/6,float(1)/6,float(1)/6,float(1)/6,float(2)/6,0],
        [float(1)/6,float(1)/6,float(1)/6,float(1)/6,0,float(2)/6]]


#Q was found from the canonical matrix (which was computed in dot-point 2 of assignment)
Q_4 = [[float(2)/6,0],
     [0,float(2)/6]]
#finding absorption times
N_4 = np.linalg.inv((np.eye(2)-Q_4))
absorption_times_4 = np.matmul(N_4,[1,1])
print(absorption_times_4),'n=4 absortption times'


# N=5 CASE:

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
#Q was found from the canonical matrix (using another script in this directory)
Q_5 = [[beta,0,0,0,0],
       [0,beta,0,0,0],
       [0,0,beta,0,0],
       [0,0,0,beta,0],
       [0,0,0,0,beta]]
#finding absorption times
N_5 = np.linalg.inv((np.eye(5)-Q_5))
absorption_times_5 = np.matmul(N_5,[1,1,1,1,1])
print(absorption_times_5),'n=5 absortption times'
