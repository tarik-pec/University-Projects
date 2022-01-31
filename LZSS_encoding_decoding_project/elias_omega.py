#Tarik Pecaninovic


from bitarray import bitarray

#takes in an integer and produces the binary representation as a string
def int2bin(integer):

    integer_binary = ''

    if integer != 0:
        while integer != 0:
            if integer%2 == 1:
                integer_binary = '1'+ integer_binary
                integer = integer//2
            else:
                integer_binary = '0' + integer_binary
                integer = integer//2
    else:
        integer_binary = '0'


    return integer_binary


#concatenates two bit arrays, but also checks to see if b is a length code.
#If it is, adds the length code flag
def concat_to_bitarray(a,b,len_comp_flag = False):

    #take each bit of b and prepend it to a
    for bit in reversed(b):
        a = bitarray(bit) + a

    #if enconding a length component, toggle bit to 0
    if len_comp_flag == True:
        a[0] = 0

    return a




# takes an integer and returns a bitarray that corresponds to the elias omega encoding of the integer
# (but read from right to left)
def elias_omega_encode(integer):

    #initialise bitarray
    output = bitarray()
    #find binary representation of integer and add to bitarray
    code_comp = int2bin(integer)
    output = concat_to_bitarray(output,code_comp)
    #initialise length component
    curr_len_comp = code_comp
    curr_int = integer
    #while length of length component is bigger than one, find L_i and encode
    while len(curr_len_comp) != 1:
        L_i = int2bin(len(curr_len_comp)-1)
        output = concat_to_bitarray(output,L_i,True)
        curr_int = len(curr_len_comp)-1
        curr_len_comp = L_i

    return output


#test = elias_omega_encode(561)
#print(test)


#teakes in a bitarray and returns its corresponding integer
def bit_arr_to_int(bit_arr,start_point,end_point):

    corr_int = 0
    for bit in bit_arr[start_point:end_point]:
        corr_int = (corr_int << 1) | bit

    return corr_int



#takes in an encoded integer and returns the corresponding integer
#also returns pointer which points to value in bitarray which is after this encoded int
def elias_omega_decode(encoded_int,start_point):

    #if encoded int is 1, return 1 and increment pointer to next value
    if encoded_int[start_point] == 1:
        return 1,start_point+1


    start_of_num_point = 1+start_point
    end_of_num_point = 2+start_point

    
    #while the current encoded part start with 0, find the corresponding integer and increment accordingly
    while encoded_int[start_of_num_point] == 0:

        #flip length code intial bit back to 1
        encoded_int[start_of_num_point] = 1
        
        #take the corresponding chunk of the bitarray and convert it into an integer
        corr_len_code_int = bit_arr_to_int(encoded_int,start_of_num_point,end_of_num_point+1)
        
        #shift pointers accordingly
        start_of_num_point += end_of_num_point-start_of_num_point+1
        end_of_num_point+=corr_len_code_int+1

    decoded_int = bit_arr_to_int(encoded_int,start_of_num_point,end_of_num_point+1)
        
    #return the decoded integer and also the pointer which points to the end of this encoded integer
    return decoded_int,end_of_num_point+1





###TESTING###


# for i in range(1,100):
#     encode = elias_omega_encode(i)
#     decode = elias_omega_decode(encode,0)
#     if decode != (i,len(encode)):
#         print('ohno')
#         break
#     else:
#         print('yeeha')


#testing when integer is in middle of bitarray
# test = elias_omega_encode(561)
# test = bitarray('0') + test
# test = test + bitarray('1')
# print(len(test))
# print(elias_omega_decode(test,1))
