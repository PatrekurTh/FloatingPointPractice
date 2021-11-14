import os
from funcs import *
from FloatingPointDecode import *
from FloatingPointEncode import *
from text_colors import bcolors

def main():
    os.system('cls')
    print_welcome()
    
    de_en = input("Do you want to practice encoding or decoding (e/d)? ")
    print(f"{bcolors.INFO}Higher difficulty only increases the {bcolors.ENDC}", end="")
    print(f"{bcolors.WARNING}POTENTIAL {bcolors.ENDC}", end="")
    print(f"{bcolors.INFO}difficulty of cases{bcolors.ENDC}")
    print(f"{bcolors.INFO}It does not automatically mean harder cases{bcolors.ENDC}")
    diff = int(input("Enter difficulty (1-5): "))
    game(de_en, diff)

def game(de_en, diff):

    quit = False
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

        decisions = input("Another one? (no to quit, m for menu) ").lower()
        if  decisions == "no":
            quit = True
        elif decisions == "m":
            main()

main()
