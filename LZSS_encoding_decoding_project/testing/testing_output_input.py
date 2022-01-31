

import sys



def test(file_1,file_2):

    input_txt_1 = open(file_1,'r').read()

    input_txt_2 = open(file_2,'r').read()

    print(input_txt_1 == input_txt_2)
    return 'Done:)'









if __name__ == '__main__':
    test(sys.argv[1],sys.argv[2])
