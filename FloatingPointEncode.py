import random
import fractions

class FloatingPointEncode(object):
    def __init__(self, difficulty) -> None:
        # TODO randomize format
        self.difficulty = difficulty
        self.numerator = self.get_number()
        self.denominator = self.get_number()
        self.case = 'N'
        if self.denominator:
            self.fraction = fractions.Fraction(self.numerator, self.denominator)
        else:
            self.case = 'S' # NaN

    def get_fraction(self):
        if self.case != 'S':
            mantissa_list = self.normalise()[0]
            return ''.join(mantissa_list)[:5] # constant hér er len(f)
        else:
            return '!0'

    def get_exponent(self):
        try:
            fraction = self.whole_to_bin(self.normalise()[1] + self.get_bias())
        except TypeError: # case 'S'
            return "".join(['1' for _ in range(4)])
        if self.case == 'N':
            return fraction[-4:] # # constant hér er len(e)
        else: # case 'D'
            return "".join(['0' for _ in range(4)])

    def get_sign(self):
        if self.case != 'S':
            return '0' if self.fraction >= 0 else '1'
        else : return 'n/a'

    def get_bias(self):
        return 7 # constant for now

    def get_min_e(self):
        return 1 - self.get_bias()

    def get_max_e(self):
        return 14 - self.get_bias()

    def normalise(self):
        if self.denominator == 0:
            self.case = 'S'
            return
        whole_part = list(self.whole_to_bin(int(self.fraction)))
        fraction_part = list(self.frac_to_bin())
        binary_num = whole_part + ['.'] + fraction_part
        print(f"{binary_num=}")
        dot_hop_counter = 0
        try:
            leftmost_one = binary_num.index('1')
        except ValueError: # Zero
            self.case = 'D'
            return fraction_part, -self.get_bias()
        point_index = binary_num.index('.')
        # move dot
        while point_index != leftmost_one+1:
            if point_index < leftmost_one:
                binary_num[point_index], binary_num[point_index + 1]\
                    = binary_num[point_index+1], binary_num[point_index] 
                dot_hop_counter -= 1
                point_index += 1
                if dot_hop_counter == self.get_min_e():
                    self.case = 'D' # Denorm
                    break
                leftmost_one = binary_num.index('1')
            else:
                binary_num[point_index], binary_num[point_index - 1]\
                    = binary_num[point_index - 1], binary_num[point_index]
                dot_hop_counter += 1
                point_index -= 1
                if dot_hop_counter == self.get_max_e():
                    self.case = 'S' # Infinity
                    break
                leftmost_one = binary_num.index('1')
        # remove leading stuff
        while binary_num[0] != '.':
            binary_num.pop(0)
        # remove dot
        binary_num.pop(0)
        return binary_num, dot_hop_counter

    def whole_to_bin(self, num):
        bit_str = ""
        num = abs(int(num))
        for _ in range(15): # breyta constant eftir hvað má jumpa langt
            bit_str += str(num % 2)
            num //= 2
        return bit_str[::-1]

    def frac_to_bin(self):
        bit_str = ""
        num = abs(float(self.fraction) - int(self.fraction))
        for _ in range(15): # breyta constant eftir hvað má jumpa langt
            bit_str += str(int(num * 2))
            num = (num * 2) - int(num * 2)
        return bit_str

    def get_number(self):
        return random.randint(-self.difficulty, self.difficulty)

    def __str__(self) -> str:
        if self.case == 'S':
            return f"{self.numerator}/{self.denominator}"
        return f"{self.fraction}"
