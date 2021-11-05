import random
import fractions
from text_colors import bcolors

class FloatingPointEncode(object):
    def __init__(self) -> None:
        # TODO randomize format
        # calc bias
        self.numerator = self.number_getter()
        self.denominator = abs(self.number_getter())
        self.bias = 7 # constant for now
        self.printfraction = fractions.Fraction(self.numerator, self.denominator)
        self.mine = 1 - self.bias
        self.maxe = 14 - self.bias
        self.case = "Normalized"
        self.sign = self.calc_sign()
        self.frac , self.expo = self.biased_exponent()
        self.case_l = "N"

    def biased_exponent(self):
        mantissa, exponent = self.normalise()
        exponent = self.whole_to_bin(exponent + self.bias)
        mantissa = "".join(mantissa)
        if self.case == "Denormalized":
            self.case_l = "D"
            exponent = "0000"
        if self.case == "Infinity":
            self.case_l = "S"
            exponent = "1111"
            mantissa = "00000"
        mantissa = mantissa[:5]
        exponent = exponent[:4]
        return mantissa, exponent

    def normalise(self):
        string_list = list(self.whole_to_bin(int(self.numerator/self.denominator)))
        string_list.append(".")
        string_list += list(self.frac_to_bin())
        
        exp_counter = 0
        leftmost_one = string_list.index('1')
        point_index = string_list.index('.')
        # move dot
        while point_index != leftmost_one+1:
            if point_index < leftmost_one:
                string_list[point_index], string_list[point_index + 1]\
                    = string_list[point_index+1], string_list[point_index] 
                exp_counter -= 1
                point_index += 1
                if exp_counter == self.mine:
                    self.case = "Denormalized"
                    break
                leftmost_one = string_list.index('1')
            else:
                string_list[point_index], string_list[point_index - 1]\
                    = string_list[point_index - 1], string_list[point_index]
                exp_counter += 1
                point_index -= 1
                if exp_counter == self.maxe:
                    self.case = "Infinity"
                    break
                leftmost_one = string_list.index('1')
        # remove leading 0's
        while string_list[0] == '0':
            string_list.pop(0)
        # pad with 0's
        while len(string_list) < 7:
            string_list.append('0')
        # remove first bit (always 1)
        string_list.pop(0)
        # return without point
        return string_list[1:], exp_counter

    def whole_to_bin(self, num):
        bit_str = ""
        while num:
            bit_str += str(num % 2)
            num //= 2
        while len(bit_str) < 4:
            bit_str += '0'
        return bit_str[::-1]

    def frac_to_bin(self):
        bit_str = ""
        num = (self.numerator/self.denominator) - int(self.numerator/self.denominator)
        while num:
            bit_str += str(int(num * 2))
            num = (num * 2) - int(num * 2)
        return bit_str

    def calc_sign(self):
        ret = ""
        if self.numerator > 0:
            ret = "0"
        else:
            ret = "1"
        self.numerator = abs(self.numerator)
        return ret

    def number_getter(self):
        return random.randint(-50, 100)

    def review_ans(self, sign, exponent, fraction, case):
        print("="*50)
        print("Answers:")
        print()
        print(f"Sign was {self.sign}")
        print(f"You answered {sign}")
        if sign == self.sign:
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Incorrect!{bcolors.ENDC}")
        print()
        print(f"exp was {self.expo}")
        print(f"You answered {exponent}")
        if self.expo == exponent:
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Incorrect!{bcolors.ENDC}")
        print()
        print(f"frac was {self.frac}")
        print(f"You answered {fraction}")
        if fraction == self.frac:
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Incorrect!{bcolors.ENDC}")
        print()
        print(f"case was {self.case_l}")
        print(f"You answered {case}")
        if case == self.case_l:
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Incorrect!{bcolors.ENDC}")
        # case

    def __str__(self) -> str:
        return f"{self.printfraction}"


class FloatingPointDecode(object):
    def __init__(self) -> None:
        self.mantissa = self.create_bit_string()
        self.exponent = self.create_bit_string()
        self.sign = str(random.randint(0,1))
        self.bias = 2**(len(self.exponent)-1)-1
        self.case = self.calc_case()

    def create_bit_string(self) -> str:
        ''' Creates randomized bit string of length {max} '''
        max = 5 # change this for shorter bit strings
        return_str = ""
        for _ in range(random.randint(2,max)):
            return_str += str(random.randint(0,1))
        return return_str

    def calc_case(self) -> str:
        ''' Returns case of float number '''
        # if exponent is all 1's
        if not "0" in self.exponent:
            # mantissa is all 0's
            if not "1" in self.mantissa:
                return "infinity"
            # mantissa is all 1's
            else:
                return "NaN"
        # if exponent is all 0's
        elif not "1" in self.exponent:   
            # mantissa is all 0's
            if not "1" in self.mantissa:
                return "Denormalized" # Zero
            # mantissa is all 1's
            else:
                return "Denormalized"
        return "Normalized"

    def expo_ans(self):
        ''' Calculate exponent of float '''
        exponent_ans = int(self.exponent, 2) - self.bias
        if self.case == "Normalized" or self.case == "Denormalized":
            return exponent_ans
        else : return ""

    def frac_ans(self):
        ''' Calculate mantissa of float '''
        start = 0.5
        the_sum = 0
        for bit in self.mantissa:
            the_sum += int(bit) * start
            start /= 2
        if self.case == "Normalized":
            frac_ans = 1 + the_sum
        elif self.case == "Denormalized":
            frac_ans = the_sum
        else:
            return ""
        return fractions.Fraction(frac_ans)

    def calc_ans(self):
        ''' Calculated decoded number '''
        if self.case == "NaN":
            return "NaN"
        elif self.case == "Infinity":
            if self.sign == "1":
                return "-Infinity"
            else:
                return "+Infinity"
        else:
            x = (-1)**int(self.sign)
            y = self.frac_ans()
            z = 2**self.expo_ans()
            return  fractions.Fraction(x * y * z)

    def calc_sign(self):
        ''' Checks if sign matters '''
        if self.case == "NaN":
            return ""
        return self.sign

    def review_ans(self, bias, sign, mantissa, exponent, decoded):
        # review inputs
        print("="*50)
        print("Answers:")
        print()
        print(f"Bias was {self.bias}")
        print(f"You answered {bias}")
        if bias == self.bias:
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Incorrect!{bcolors.ENDC}")
        print()
        print(f"Sign was {self.sign}")
        print(f"You answered {sign}")
        if sign == int(self.sign):
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Incorrect!{bcolors.ENDC}")
        print()
        print(f"Mantissa was {self.frac_ans()}")
        print(f"You answered {mantissa}")
        if mantissa == self.frac_ans():
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Incorrect!{bcolors.ENDC}")
        print()
        print(f"Exponent was {self.expo_ans()}")
        print(f"You answered {exponent}")
        if exponent == self.expo_ans():
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Incorrect!{bcolors.ENDC}")
        print()
        print(f"Y was {self.calc_ans()}")
        print(f"You answered {decoded}")
        if decoded == self.calc_ans():
            print(f"{bcolors.OKGREEN}Correct!{bcolors.ENDC}")
        else:
            print(f"{bcolors.WARNING}Incorrect!{bcolors.ENDC}")
        print()
        print(f"This was a {bcolors.INFO}{self.case}{bcolors.ENDC} case")
        print()

    def __str__(self):
        return f"S=[{self.sign}] E=[{self.exponent}] M=[{self.mantissa}]"
