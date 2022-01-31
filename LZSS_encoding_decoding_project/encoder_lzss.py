#Tarik Pecaninovic

import sys
from bitarray import bitarray
from huffman import huffman_codes
from elias_omega import elias_omega_encode
from Z_Algorithm import z_alg


# The following function computes the offset and the length of copy,
# given an input text, the sizes of the context and lookahead buffer,
# and the current char in the input txt.
# For the following, let context denote the string corresponding to the
# context defined by the above, and lookahead define the string corresponding to the
# lookahead defined by the above.
# The function constructs a string given by lookahead + unique char + context + lookahead,
# then computes the constructed strings z values.
# It then finds the maxinum z values (after the index of the unique char) which is furthest
# to the right. The z value corresponds to the length of copy  and its index is equivalent to the
# offset.
# This function is linear in the length of the contrsucted string. Thus, the time complexity in the
# overall function will depend on the overlaps of these constructed strings (i.e., no overlap means
# that the overall time complexity will be linear in the length of the overall input text, but alrger
# overlaps means a worse time complexity. Worst case is, I believe, length of text squared). But we observe
# that the number and lengths of overlaps depends on W and L (as they define the constructed string).
# Thus a smaller W and L implies a better time complexity (but larger output size), and the opposite for larger
# W and L.

def offset_len_compute(input_txt,W,L,pos_pointer):

    #set pointers to boundary of context and lookahead buffer. if they go before or after the
    #input txt, set pointers to start or end of txt respectively
    if pos_pointer-W <0:
        context_start_point = 0
    else:
        context_start_point = pos_pointer-W
    if pos_pointer+L>len(input_txt)-1:
        look_ahead_end_point = len(input_txt)
    else:
        look_ahead_end_point = pos_pointer+L
        
    #construct a string which is the substring corresponding to the look ahead buffer, followed
    #by a unique character, followed by the substring corresponding to the context, followed by the
    #lookahead buffer string again
    constructed_str = input_txt[pos_pointer:look_ahead_end_point] + '$' + input_txt[context_start_point:pos_pointer] + input_txt[pos_pointer:look_ahead_end_point]

    
    #run z algorithm on the constructed string
    z_vals_constructed_str = z_alg(constructed_str)
    
    #find the maximum z value /furthest to the right/ which also corresponds to the context part
    #of the constructed substring
    first_index = len(input_txt[pos_pointer:look_ahead_end_point])+1
    last_index = len(z_vals_constructed_str)-len(input_txt[pos_pointer:look_ahead_end_point])
    max_z_val_index = first_index
    for curr_index in range(first_index,last_index):
        if z_vals_constructed_str[curr_index] >= z_vals_constructed_str[max_z_val_index]:
            max_z_val_index = curr_index

    offset = last_index - max_z_val_index
    if offset == 0:
        len_of_copy = 0
    else:
        len_of_copy = z_vals_constructed_str[max_z_val_index]
        
    return offset,len_of_copy

#TESTING:
#test = 'aacaacabcabaaac'
#print(offset_len_compute('acaacaabcaba', 0, 0, 0))
#print(offset_len_compute('acaacaabcaba',6,4,3))


# The following function takes in the input txt and the a pointer to a char of that txt
# and then does a format 1 encoding of that character
def format_1_encode(input_txt,pos_pointer,temp_data_encode,huff_codes):

    #encode a 1 bit to flag a format-1 encoding
    temp_data_encode = temp_data_encode + bitarray('1')

    #encode huffman code of char at pos_pointer
    char_huff_code = huff_codes[input_txt[pos_pointer]]
    temp_data_encode = temp_data_encode + char_huff_code

    return temp_data_encode

# The following function takes in the numbers corresponding to offset and the length of the copy
# and then does a format 0 encoding of those numbers
def format_0_encode(offset,len_of_copy,temp_data_encode):

    #encode a 0 bit to flag a format-1 encoding
    temp_data_encode = temp_data_encode + bitarray('0')

    #encode offset and length of copy integers using elias omega, then add to bitarray
    offset = elias_omega_encode(offset)
    len_of_copy = elias_omega_encode(len_of_copy)
    temp_data_encode = temp_data_encode + offset
    temp_data_encode = temp_data_encode + len_of_copy
    
    return temp_data_encode


# The following takes in an input text and two integer corresponding to the sizes of the
# context and lookahead buffer respectively, and returns the corresponding LZSS-encoding of the input text.
def encoder_lzss(input_txt_file, W_input, L_input):

    #initalise input integers and input text
    W = int(W_input)
    L = int(L_input)
    input_txt = open(input_txt_file,'r').read()
    input_txt = input_txt.replace('\n','')


    #handle case when input string is a single character
    #so I'm not actually sure if this case should be encoded differently since
    #there might be a more efficient way to store a single char
    if len(input_txt) == 1:
        #encode: one unique ascii char + chars ascii no + len huff == 1 + huff code == 1 + 1 0/1format-field + format-1 w/ code 1
        ascii_bin = bin(ord(input_txt))[2:]
        while len(ascii_bin) != 7:
            ascii_bin = '0' + ascii_bin
        encoded_txt = bitarray('1')
        encoded_txt = encoded_txt + bitarray(ascii_bin)
        encoded_txt = encoded_txt + bitarray('11111')
        with open('output_encoder_lzss.bin', 'wb') as fh:
            encoded_txt.tofile(fh)
        return 'Done:)'

    
    #initialise bitarray for encoded txt, pointer to current position of txt, and find huffman code for chars
    encoded_txt = bitarray()
    pos_pointer = 0
    huff_codes = huffman_codes(input_txt)
    
    ###ENCODE HEADER PART###

    #encode the number of unique ascii characters
    no_unique_ascii = elias_omega_encode(len(huff_codes.keys()))
    encoded_txt = encoded_txt + no_unique_ascii

    #for each character, encode its ascii number, the length of the huff code, and then its huff code
    for char in huff_codes.keys():

        #find char 7-bit ascii rep and encode
        ascii_bin = bin(ord(char))[2:]
        while len(ascii_bin) != 7:
            ascii_bin = '0' + ascii_bin
        ascii_bin = bitarray(ascii_bin)
        encoded_txt = encoded_txt + ascii_bin

        #find len of chars huff code, use elias omega, then encode
        len_char_huff_code = len(huff_codes[char])
        len_char_huff_code = elias_omega_encode(len_char_huff_code)
        encoded_txt = encoded_txt + len_char_huff_code

        #encode chars huff code
        char_huff_code = huff_codes[char]
        encoded_txt = encoded_txt + char_huff_code


    ###ENCODE DATA PART###

    #we wish to encode the total number of format fields before the encoded data
    #but this information is found after finding the encoded data, so initialise
    #a temp bitarray
    total_format_fields = 0
    temp_data_encode = bitarray()

    while pos_pointer < len(input_txt):

        #compute offset and length of copy for current character
        offset,len_of_copy = offset_len_compute(input_txt,W,L,pos_pointer)
        #if length of copy is less than three, do a format 1 encoding of the char
        if len_of_copy < 3:
            total_format_fields += 1
            temp_data_encode = format_1_encode(input_txt,pos_pointer,temp_data_encode,huff_codes)
            pos_pointer += 1
        #otherwise the length of copy is greater than three and we do a format 0 encoding of the char
        else:
            total_format_fields += 1
            temp_data_encode = format_0_encode(offset,len_of_copy,temp_data_encode)
            pos_pointer += len_of_copy

    #encode total number of format fields, then encode data section
    total_format_fields = elias_omega_encode(total_format_fields)
    encoded_txt = encoded_txt + total_format_fields
    encoded_txt = encoded_txt + temp_data_encode

    #output bitarray to bin file
    with open('output_encoder_lzss.bin', 'wb') as fh:
        encoded_txt.tofile(fh)
    
    
    return 'Done:)'

###TESTING###
#print(encoder_lzss('aacaacabcaba',6,4))

# THE TOP IS MY OUTPUT AND THE BOTTOM IS FROM THE ASS SPEC SHEET
# NOTE THAT MY HEADER PART IS THE SAME UP TO PERMUTATION
#01111000011111 000110 100111 000100 1000000 11111111010011000100100001101111
#01111000011111 000100 100011 000110 1001000 11111111010011000100100001101111


if __name__ == '__main__':
    encoder_lzss(sys.argv[1],sys.argv[2],sys.argv[3])
