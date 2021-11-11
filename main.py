import os
from funcs import *
from FloatingPointDecode import *
from FloatingPointEncode import *

def main():
    os.system('cls')

    quit = False
    de_en = input("Do you want to practice encoding or decoding? (e/d) ")
    diff = int(input("Enter difficulty (1-5): "))

    while not quit:
        os.system('cls')
        if de_en == "d":
            fp = FloatingPointDecode(diff+2)
            print_header_decode()
            cowsay(fp)
            bias, sign, mantissa, exponent, decoded = get_decode_input()
            review_decode_answer(fp, bias, sign, mantissa, exponent, decoded)
        else:
            fp = FloatingPointEncode(diff*20)
            print_header_encode()
            cowsay(fp)
            print()
            sign, exponent, fraction, case = get_encode_input()
            review_encode_answer(fp, sign, exponent, fraction, case)

        if input("Another one? (enter no to quit) ").lower() == "no":
            quit = True

main()
