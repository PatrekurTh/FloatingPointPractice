import fractions
from math import exp
from text_colors import bcolors

def print_header_decode():
    print(f"="*50)
    print(f"{bcolors.INFO}If the value is not a number or infinite please use NaN and ±Infinity{bcolors.ENDC}")
    print(f"{bcolors.INFO}Please enter 'n/a' where it applies (NaN, Infinity etc.){bcolors.ENDC}")
    print("="*50)
    print(f"{bcolors.INFO}The formula is Y = (-1)^S x M x 2^E{bcolors.ENDC}")
    print(f"{bcolors.INFO}Decode the following floating point values values:{bcolors.ENDC}")
    print("="*50)
    print()

def print_header_encode(exponent_size, mantissa_size):
    print("="*50)
    print(f"{bcolors.INFO}Format, {exponent_size} exponent bits and {mantissa_size} fraction bits. [ S ][ {' '.join(['e' for _ in range(exponent_size)])} ][ {' '.join(['f' for _ in range(mantissa_size)])} ]{bcolors.ENDC}")
    print(f"{bcolors.INFO}Please enter 'n/a' for sign if it has no meaning{bcolors.ENDC}")
    print(f"{bcolors.INFO}Solve the following encoding problem:{bcolors.ENDC}")
    print("="*50)

def get_encode_input():
    bias = int(input("What is the bias? "))
    min_e = int(input("What is min(E)? "))
    sign = input("S = ")
    exponent = input("exp = ")
    fraction = input("frac = ")
    case = input("Is this  Norm, De-Norm or Special-Case  (N/D/S)? ")
    return sign, exponent, fraction, case, bias, min_e

def get_decode_input():
    b = int(input("bias = "))
    s = input("S = ")
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
    print()

def print_result(name, a, b):
    print(f"{name} was {a}")
    print(f"You answered {b}")
    if a == b:
        print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
    else:
        print(f"{bcolors.WARNING}Incorrect!{bcolors.ENDC}")
    print()

def print_answer_head():
    print("="*50)
    print("Answers:")
    print()

def review_decode_answer(fp_obj, bias, sign, mantissa, exponent, decoded):
    print_answer_head()
    print_result("Bias", fp_obj.get_bias(), bias)
    print_result("Sign", fp_obj.get_sign(), sign)
    print_result("Mantissa", fp_obj.frac_ans(), mantissa)
    print_result("Exponent", fp_obj.expo_ans(), exponent)
    print_result("Y", fp_obj.calc_ans(), decoded)

def review_encode_answer(fp_obj, sign, exponent, fraction, case, bias, min_e):
    print_answer_head()
    print_result("Bias", fp_obj.get_bias(), bias)
    print_result("min(E)", fp_obj.get_min_e(), min_e)
    print_result("Sign", fp_obj.get_sign(), sign) # done
    print_result("exp", fp_obj.get_exponent(), exponent)
    print_result("frac", fp_obj.get_fraction(), fraction)
    print_result("case", fp_obj.case, case)

def print_welcome():
    print(f"""
================================================================================================
                        __        __   _                          
                        \ \      / /__| | ___ ___  _ __ ___   ___ 
                         \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \\
                          \ V  V /  __/ | (_| (_) | | | | | |  __/ 
                           \_/\_/ \___|_|\___\___/|_| |_| |_|\___|
              To the floating point encoding/decoding practice simulator-inator
================================================================================================
                                                                                {bcolors.NAME}made by Patrekur{bcolors.ENDC}""")
