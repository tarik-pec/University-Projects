#Tarik Pecaninovic

# Re-used code form assignment 1 which computes the z values of a given input string


def z_alg(alpha):
    #initialise z_i list and append z_0
    if len(alpha) == 1:
        return [1]
    
    z_i_values = []
    z_i_values.append(len(alpha))

    # computes z_1
    z_i_values.append(z_i_comp(alpha, 1))
    if z_i_values[1]>0:
        r = z_i_values[1]
        l = 1
    else:
        r = 0
        l = 0

    #compute other  z_i values
    for k in range(2,len(alpha)):
        if r < k:
            z_i_values.append(z_i_comp(alpha,k))
            if z_i_values[k]>0:
                    r = z_i_values[k] + k - 1                    
                    l = k
        else:
            if z_i_values[k-l] < r-k+1:
                z_i_values.append(z_i_values[k-l])
                if z_i_values[k]>0:
                    r = z_i_values[k] + k -1
                    l = k
            else:
                if r != len(alpha)-1:
                    z_i_values.append(r-k+1 + z_i_comp(alpha, r+1, r+1-k))
                else:
                    z_i_values.append(r-k+1)
                if z_i_values[-1]>0:
                    r = z_i_values[k] + k -1
                    l = k
    return z_i_values
                          



def z_i_comp(beta, index, start=0):
    z_i = 0
    while beta[z_i+index] == beta[z_i+start]:
            z_i = z_i +1
            #if z_i == len(beta)-index means you have matched up to the end of the string
            if z_i == len(beta)-index:
                break
    return z_i

