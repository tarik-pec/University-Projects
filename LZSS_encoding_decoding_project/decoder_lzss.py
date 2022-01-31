#Tarik Pecaninovic

import sys
from bitarray import bitarray
from elias_omega import elias_omega_decode


# The following converts a bit array into an integer
def bit_arr_to_int(bit_arr,start_point,end_point):

    corr_int = 0
    for bit in bit_arr[start_point:end_point]:
        corr_int = (corr_int << 1) | bit

    return corr_int

# The following is for the case when a format-0 encode is encountered.
def format_0_decode(input_bits,offset,len_of_copy,output_txt):
    end_of_txt = len(output_txt)
    #for the length of copy
    for curr_char_index in range(len_of_copy):
        #take the character at the offset and add it to the end of the string
        output_txt = output_txt + output_txt[end_of_txt-offset+curr_char_index]
        
    return output_txt



# The following is for the case when a format-1 encode is encountered.
def format_1_decode(input_bits,pos_pointer,chars_and_huffman,output_txt):

    start_pointer = pos_pointer
    end_pointer = pos_pointer+1
    code_not_found_flag = True
    #check if the current 'code' returns a leaf in the huffman binary tree,
    #if yes add that chracter, if no add an extra bit to the 'code' and repeat
    while code_not_found_flag:
        try:
            chars_and_huffman[str(input_bits[start_pointer:end_pointer])]
            output_txt += chars_and_huffman[str(input_bits[start_pointer:end_pointer])]
            code_not_found_flag = False

        except:
            end_pointer+=1

    return output_txt,end_pointer


# Decodes an input LZSS-encoded string
def decoder_lzss(input_bits_file):

    #open bin file and add to bitarray

    input_bits = bitarray()
    with open(input_bits_file, 'rb') as fh:
        input_bits.fromfile(fh)

    
    pos_pointer = 0
    
    ###DECODING HEADER###
    
    #find the number of unique ascii characters in the text
    #(and move pointer to after this encoded number)
    no_unique_chars,pos_pointer = elias_omega_decode(input_bits,pos_pointer)

    chars_and_huffman = {}
    for _ in range(no_unique_chars):
        #decode the characters ascii code and decode its corresponding huffman code.
        curr_char_huff = []
        #find the characters corresponding ASCII number
        curr_char_ascii_no = input_bits[pos_pointer:pos_pointer+7]
        curr_char_ascii_no = bit_arr_to_int(curr_char_ascii_no,0,len(curr_char_ascii_no))
        pos_pointer +=7
        #find the length of the the chars huffman code
        curr_char_huff_len,pos_pointer = elias_omega_decode(input_bits,pos_pointer)
        #find the huffman code
        curr_char_huff_code = input_bits[pos_pointer:curr_char_huff_len+pos_pointer]
        pos_pointer += curr_char_huff_len
        #add the char and code to array
        chars_and_huffman[str(curr_char_huff_code)] = chr(curr_char_ascii_no)


    ###DECODING DATA###
    output_txt = ''

    #decode the number of 0/1-format fields
    no_format_fields,pos_pointer = elias_omega_decode(input_bits,pos_pointer)

    #for each format field, decode accordingly
    for _ in range(no_format_fields):
        #if format 0, 
        if input_bits[pos_pointer] == 0:
            pos_pointer += 1
            offset,pos_pointer = elias_omega_decode(input_bits,pos_pointer)
            len_of_copy,pos_pointer = elias_omega_decode(input_bits,pos_pointer)
            output_txt = format_0_decode(input_bits,offset,len_of_copy,output_txt)
        #o/w format 1, so add character accordingly
        else:
            pos_pointer+=1
            output_txt,pos_pointer = format_1_decode(input_bits,pos_pointer,chars_and_huffman,output_txt)

    
    output_file = open('output_decoder_lzss.txt','w+')
    output_file.write(output_txt)
    
    return 'Done:)'


###TESTING###
# test_head = bitarray('011110000111110001001000110001101001')
# test_data = bitarray('00011111111010011000100100001101111')
# test = test_head + test_data
# print(decoder_lzss(test))





#LEARNING TO WRITE AND READ BITS
# bits = bitarray('01111000011111000100100011000110100100011111111010011000100100001101111')
# with open('test.bin', 'wb') as fh:
#         bits.tofile(fh)


# a = bitarray()
# with open('test.bin', 'rb') as fh:
#         a.fromfile(fh)
# print(a)




if __name__ == '__main__':
    decoder_lzss(sys.argv[1])
