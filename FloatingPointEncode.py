import random
import fractions

class FloatingPointEncode(object):
    def __init__(self, difficulty) -> None:
        self.difficulty = difficulty
        self.numerator = self.get_numerator()
        self.denominator = self.get_denominator()
        self.case = 'N'
        self.exponent_size = self.get_number()
        self.mantissa_size = self.get_number()
        if self.denominator:
            self.fraction = fractions.Fraction(self.numerator, self.denominator)
        else:
            self.case = 'S' # NaN

    def get_fraction(self):
        if self.case != 'S':
            mantissa_list = self.normalise()[0]
            return ''.join(mantissa_list)[:self.mantissa_size]
        else:
            return '!0x0'

    def get_exponent(self):
        try:
            fraction = self.whole_to_bin(self.normalise()[1] + self.get_bias())
        except TypeError: # case 'S'
            return "".join(['1' for _ in range(self.exponent_size)])
        if self.case == 'N':
            return fraction[-self.exponent_size:]
        else: # case 'D'
            return "".join(['0' for _ in range(self.exponent_size)])

    def get_sign(self):
        if self.case != 'S':
            return '0' if self.fraction >= 0 else '1'
        else : return 'n/a'

    def get_bias(self):
        return 2 ** (self.exponent_size -1) -1

    def get_min_e(self):
        return 1 - self.get_bias()

    def get_max_e(self):
        x = "".join(['1' if i != self.exponent_size else '0' for i in range(1, self.exponent_size+1)])
        return int(x, 2) - self.get_bias()
    
    def get_numerator(self):
        return random.randint(-self.difficulty, self.difficulty)

    def get_denominator(self):
        x = random.randint(-self.difficulty, self.difficulty)
        y = random.choice([2**x for x in range(int((self.difficulty/20)*2))])
        return random.choice([x,y])
    
    def get_number(self):
        return random.randint(2,(self.difficulty/20)+2)

    def normalise(self):
        if self.denominator == 0:
            self.case = 'S'
            return
        whole_part = list(self.whole_to_bin(int(self.fraction)))
        fraction_part = list(self.frac_to_bin())
        binary_num = whole_part + ['.'] + fraction_part
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

    def __str__(self) -> str:
        if self.case == 'S':
            return f"{self.numerator}/{self.denominator}"
        return f"{self.fraction}"
