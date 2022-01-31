#Tarik Pecaninovic


from bitarray import bitarray

# A basic graph class designed specifically for huffman
# Note the structure of the graph is setup in a way to be able to easily obtain the codes of the
# characters. Each child holds its parent and the corresponding bit on that edge. Hence to find
# the code of a character, we begin at the corresponding leaf and traverse upwards until the root
# is reached.
class Graph:

    def __init__(self):
        self.__graph_dict = {}

    def add_vertex(self,vertex,parent=0):
        self.__graph_dict[vertex] = [parent,[0,0]]

    def add_edge(self,vertex1,vertex2,bit):
        #to parent, add child (IT TURNS OUT THIS WASNT NEEDED)
        #to child, add parent and bit
        self.__graph_dict[vertex1][1][bit] = vertex2
        self.__graph_dict[vertex2][0] = [vertex1,bit]
        
    #the following traverses the binary tree, starting from a leaf, upward to the root, to find
    #the corresponding huffman code of the inputted character
    def traverse_for_huffman(self,vertex_char):
        code = ''
        curr_vertex = self.__graph_dict[vertex_char]
        #while not at root, move to parent and add big on edge to code str
        while curr_vertex[0] != 0:
            code = str(curr_vertex[0][1]) + code
            curr_vertex = self.__graph_dict[curr_vertex[0][0]]
        return code

    #the following finds the root of the vertex. needed for decoding huffman code
    def find_root(self):
        #pick a random initial vertex
        ran_vertex = self.__graph_dict.keys()[0]
        #while not at the root, move up the tree
        while self.__graph_dict[ran_vertex][0] != 0:
            ran_vertex = self.__graph_dict[ran_vertex][0][0]
        return ran_vertex

    def show_graph(self):
        return self.__graph_dict
        

#GRAPH CLASS TESTING:
# test = Graph()
# test.add_vertex('v1')
# test.add_vertex('v2')
# test.add_edge('v1','v2',1)
# print(test.show_graph())



#finds all the unique characters in a given string along with their corresponding frequencies
def unique_chars(input_str):

    unique_chars_array = []
    #for each character, try to use it as a key in a dictionary;if fail, add vertex, otherwise
    #increment counter at that position (to increase freq)
    #I'm not 100% on what the time complexity of this is, but I think it should be okay?
    dictionary_test = {}
    for char in input_str:
        try:
            dictionary_test[char]
            dictionary_test[char][0] += 1
        except:
            dictionary_test[char] = [0]
            dictionary_test[char][0] += 1

    #converts dictionary to an array storing characters and their corresponding frequencies
    for char in dictionary_test.keys():
        unique_chars_array.append([char,dictionary_test[char][0]])

    return unique_chars_array

#UNIQUE_CHARS TESTING:
#print(unique_chars('bbbbaacccd'))



# Sorts list of chars by their corresponding frequencies using quicksort
# (quicksort used as we are expecing the number of unique characters in the text to be low.
# meaning the size of the array will be small).
def char_sort(input_arr):

    input_arr = quick_sort(input_arr,0,len(input_arr)-1)

    return input_arr

# The follwoing function compares the values of an array at low, hi, and mid:=(low+hi)//2, and then
# returns the index corresponding to the median of those three values.
# This index will be used as the pivot in quick sort.
def get_pivot(input_arr,low,hi):
    mid = (hi + low)//2
    pivot = hi
    if input_arr[low]<input_arr[mid]:
        if input_arr[mid]<input_arr[hi]:
            pivot = mid
    elif input_arr[low]<input_arr[hi]:
        pivot = low
    return pivot

# The following function orders a list such that everything less than the pivot is before it and
# everything after is greater, i.e., performs the main idea behind quick sort on the given subset
# of the array
def partition(input_arr,low,hi):
    #find index of pivot
    pivot = get_pivot(input_arr,low,hi)
    pivot_value = input_arr[pivot][1]
    #swap value at pivot to start
    input_arr[pivot],input_arr[low] = input_arr[low],input_arr[pivot]
    #initialises border pointer which will be used to swap values which are less than pivot to
    border = low
    for i in range(low,hi+1):
        if input_arr[i][1]<pivot_value:
            border+=1
            input_arr[i],input_arr[border] = input_arr[border],input_arr[i]
    #finally swaps value at border so that everything before it is less than that value and
    #everything after is greater
    input_arr[low],input_arr[border] = input_arr[border],input_arr[low]
    return border

# The follwoing is the function performs quick sort on the given inputs
def quick_sort(input_arr,low,hi):
    if low < hi:
        p = partition(input_arr,low,hi)
        quick_sort(input_arr,low,p-1)
        quick_sort(input_arr,p+1,hi)
    return input_arr


#QUICK_SORT TESTING:
#test = 'aaabbccccd'
#print(unique_chars(test))
#print(char_sort(unique_chars(test)))


# The following function takes in as input a sorted array and a new element which it then inserts
# into its respective place (defined by its number which was found as the sum of frequencies).
# I.e., in Huffman coding when we obtain a concatenated string with a corresponding number, this
# function adds it to the existing array
def huffman_insert(input_arr,input_char):
    #exception case for when input array is empty (means that huffman took the last two elements in
    #the array and input_char is the resulting element
    if len(input_arr) == 0:
        input_arr.append(input_char)
        return input_arr
    #as you know input_arr is sorted in ascending order, search through list until you find an
    #element with a greater number. then insert input_char just before this element
    insert_index = 0
    while input_char[1] > input_arr[insert_index][1]:
        insert_index += 1
        #if compared past the array, then input_char is the largest element
        if insert_index == len(input_arr):
            input_arr.append(input_char)
            return input_arr
    input_arr.insert(insert_index,input_char)
    
    return input_arr

#HUFFMAN_INSERT TESTING:
# test = unique_chars('aaaabbbcccd')
# test = char_sort(test)
# huffman_insert(test,['z',4])
# print(test)



# Finds the huffman codes of a given input string
def huffman_codes(input_str):

    #find all unique characters and their corresponding frequencies
    graph_gen_array = unique_chars(input_str)
    #sort the list by frequencies
    graph_gen_array = char_sort(graph_gen_array)
    input_str_chars = graph_gen_array[:]

    huffman_bin_tree = Graph()
    
    while len(graph_gen_array) > 1:
        
        #take strings corresponding to lowest frequencies
        node_1 = graph_gen_array[0]
        node_2 = graph_gen_array[1]
        
        #if single character, means it is a leaf and a vertex must be created in the graph
        if len(node_1[0]) ==1:
            huffman_bin_tree.add_vertex(node_1[0])
        if len(node_2[0]) ==1:
            huffman_bin_tree.add_vertex(node_2[0])

        #create vertex corresponding to concatenated strings with frequency equal to the sum
        new_node = [node_1[0]+node_2[0],node_1[1]+node_2[1]]
        huffman_bin_tree.add_vertex(new_node[0])
        #add children of the newly created node
        huffman_bin_tree.add_edge(new_node[0],node_1[0],0)
        huffman_bin_tree.add_edge(new_node[0],node_2[0],1)

        #remove the two nodes/strings from the array holding the (string,freq) pairs and add
        #the newly created (node,freq) element in its correct position
        del graph_gen_array[0]
        del graph_gen_array[0]
        graph_gen_array = huffman_insert(graph_gen_array,new_node)
        
    #generate the huffman codes using the binary tree created above
    #for each unique character, start at the corresponding leaf and traverse the graph 'upwards'
    #until a the root is reached--keeping track of the corresponding bits along the way

    huffman_codes = {}
    for char in input_str_chars:
        char_code = huffman_bin_tree.traverse_for_huffman(char[0])
        huffman_codes[char[0]] = bitarray(char_code)

        
    return huffman_codes

#HUFFMAN_CODES TESTING:
# test_code = huffman_codes('A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED')
# print(test_code)

