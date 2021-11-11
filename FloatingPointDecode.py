import random
import fractions

class FloatingPointDecode(object):
    def __init__(self, difficulty) -> None:
        self.difficulty = difficulty
        self.mantissa = self.create_bit_string()
        self.exponent = self.create_bit_string()
        self.sign = self.set_sign()
        self.case = self.get_case()

    def set_sign(self):
        return str(random.randint(0,1))

    def get_sign(self):
        return self.sign
    
    def get_bias(self):
        return 2 ** (len(self.exponent) -1) -1

    def get_case(self):
        # if exponent is all 1's
        if not "0" in self.exponent:
            # mantissa is all 0's
            if not "1" in self.mantissa:
                return "Infinity"
            else:
                # mantissa is all 1's
                return "NaN"
        # if exponent is all 0's
        elif not "1" in self.exponent:   
            # mantissa is all 0's
            if not "1" in self.mantissa:
                return "Denormalized" # Zero
            else:
                # mantissa is all 1's
                return "Denormalized"
        return "Normalized"

    def create_bit_string(self) -> str:
        ''' Creates randomized bit string of length {max} '''
        max = self.difficulty # 3 - 7
        bit_string = [str(random.randint(0,1)) for _ in range(random.randint(2,max))]
        return "".join(bit_string)

    def expo_ans(self):
        ''' Calculate exponent of float '''
        if self.case == "Normalized" or self.case == "Denormalized":
            exponent_ans = int(self.exponent, 2) - self.get_bias()
            return exponent_ans
        else: # Infinity or NaN
            return "n/a"

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
        else: # Infinity or NaN
            return "n/a"
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
            return "n/a"
        return self.sign

    def __str__(self):
        return f"S=[{self.sign}] E=[{self.exponent}] M=[{self.mantissa}]"
