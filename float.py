import os
import fractions
from floatnum import FloatingPointDecode, FloatingPointEncode
from text_colors import bcolors

def print_header_decode():
    print(f"="*50)
    print(f"{bcolors.INFO}If the value is not a number or infinite please use\nNaN and (+/-) Infinity for Y and leave M and E empty\nLeave sign bit empty if NaN{bcolors.ENDC}")
    print("="*50)
    print(f"{bcolors.INFO}The formula is Y = (-1)^S x M x 2^E{bcolors.ENDC}")
    print(f"{bcolors.INFO}Decode the following floating point values values:{bcolors.ENDC}")
    print("="*50)
    print()

def print_header_encode():
    print("="*50)
    print(f"{bcolors.INFO}Format, 4 exponent bits and 5 fraction bits. [ S ][ e e e e ][ f f f f f ]{bcolors.ENDC}")
    print(f"{bcolors.INFO}min(E) is -6, bias is 7{bcolors.ENDC}")
    print(f"{bcolors.INFO}Solve the following encoding problem:{bcolors.ENDC}")
    print("="*50)

def get_encode_input():
    sign = input("S = ")
    exponent = input("exp = ")
    fraction = input("frac = ")
    case = input("Is this  Norm, De-Norm or Special-Case  (N/D/S)? ")
    return sign, exponent, fraction, case

def get_decode_input():
    b = int(input("bias = "))
    s = int(input("S = "))
    m = input("M (fraction form) = ")
    if m:
        m = fractions.Fraction(m)
    e = input("E = ")
    if e:
        e = int(e)
    y = (input("Y (fraction form) = "))
    try:
        y = fractions.Fraction(y)
    except:
        pass
    return b, s, m, e, y

def cowsay(fp):
    print("_________________________________")
    print(f"<{str(fp):^30}>")
    print("---------------------------------")
    print("        \   ^__^")
    print("         \  (oo)\_______")
    print("            (__)\       )\/\\")
    print("                ||----w |")
    print("                ||     ||")

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
            print()
            bias, sign, mantissa, exponent, decoded = get_decode_input()
            fp.review_ans(bias, sign, mantissa, exponent, decoded)
        else:
            fp1 = FloatingPointEncode(diff*20)
            print_header_encode()
            cowsay(fp1)
            print()
            sign, exponent, fraction, case = get_encode_input()
            fp1.review_ans(sign, exponent, fraction, case)

        if input("Another one? (enter no to quit) ").lower() == "no":
            quit = True

main()
