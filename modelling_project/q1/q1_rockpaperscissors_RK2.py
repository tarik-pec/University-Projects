#Tarik Pecaninovic

import numpy as np
import matplotlib.pyplot as plt


def ode_rk2(ode0,ode1,ode2,bound_vals,h,b):

    x_sol = []
    y_sol = []
    
    b = float(b)
    a = 1-b
    alpha = float(0.5)/b
    beta = float(0.5)/b

    x_prev = bound_vals[0][0]
    y_prev = np.array(bound_vals[0][1])

    x_sol.append(x_prev)
    y_sol.append(y_prev)

    x_curr = x_prev + h
    y_curr=[0,0,0]
    y_curr[0] = y_prev[0] + h*(a*ode0(y_prev[0],y_prev[1],y_prev[2])+b*ode0(y_prev[0]+beta*h,y_prev[1]+beta*h,y_prev[2]+beta*h))
    y_curr[1] = y_prev[1] + h*(a*ode1(y_prev[0],y_prev[1],y_prev[2])+b*ode1(y_prev[0]+beta*h,y_prev[1]+beta*h,y_prev[2]+beta*h))
    y_curr[2] = y_prev[2] + h*(a*ode2(y_prev[0],y_prev[1],y_prev[2])+b*ode2(y_prev[0]+beta*h,y_prev[1]+beta*h,y_prev[2]+beta*h))

    x_sol.append(x_curr)
    y_sol.append(y_curr)
    
    while x_curr < bound_vals[1][0]:

        x_prev = x_curr
        y_prev = y_curr
        
        x_curr = x_prev + h
        y_curr[0] = y_prev[0] + h*(a*ode0(y_prev[0],y_prev[1],y_prev[2])+b*ode0(y_prev[0]+beta*h,y_prev[1]+beta*h,y_prev[2]+beta*h))
        y_curr[1] = y_prev[1] + h*(a*ode1(y_prev[0],y_prev[1],y_prev[2])+b*ode1(y_prev[0]+beta*h,y_prev[1]+beta*h,y_prev[2]+beta*h))
        y_curr[2] = y_prev[2] + h*(a*ode2(y_prev[0],y_prev[1],y_prev[2])+b*ode2(y_prev[0]+beta*h,y_prev[1]+beta*h,y_prev[2]+beta*h))
        
        x_sol.append(x_curr)
        y_sol.append(y_curr)
        
    return x_sol,y_sol

r = 1
s = 1
x_derv = lambda x,y,z: x*((z-y) - (r+s)*(x*(y+z)+y*z))
y_derv = lambda x,y,z: y*((x-z) - (r+s)*(x*(y+z)+y*z))
z_derv = lambda x,y,z: z*((y-x) - (r+s)*(x*(y+z)+y*z))




time_0 = [0,[0.4,0.3,0.3]]
end_of_dom = 0.3
h = 0.1
b = 0.4
t_sol,vec_sol = ode_rk2(x_derv,y_derv,z_derv,[time_0,[end_of_dom]],h,b)

plt.plot(t_sol,vec_sol)
plt.show()












# def ode_rk2(ode,bound_vals,h,b):

#     x_sol = []
#     y_sol = []
    
#     b = float(b)
#     a = 1-b
#     alpha = float(0.5)/b
#     beta = float(0.5)/b

#     x_prev = bound_vals[0][0]
#     y_prev = np.array(bound_vals[0][1])

#     x_sol.append(x_prev)
#     y_sol.append(y_prev)

#     x_curr = x_prev + h
#     y_curr = y_prev + h*(a*ode(y_prev[0],y_prev[1],y_prev[2])+b*ode(y_prev[0]+beta*h,y_prev[1]+beta*h,y_prev[2]+beta*h))

#     x_sol.append(x_curr)
#     y_sol.append(y_curr)
    
#     while x_curr < bound_vals[1][0]:
#         x_prev = x_curr
#         y_prev = y_curr
#         x_curr = x_prev + h
#         y_curr = y_prev + h*(a*ode(y_prev[0],y_prev[1],y_prev[2])+b*ode(y_prev[0]+beta*h,y_prev[1]+beta*h,y_prev[2]+beta*h))
#         x_sol.append(x_curr)
#         y_sol.append(y_curr)

#     return x_sol,y_sol
