n = 8
m = 256
alpha = 0b100011011  # reducing polynomial (x^8 + x^4 + x^3 + x + 1)
g = 0b10

g_exp = {}
g_log = {}


def mul(self, a, b, alpha=alpha):

    res = 0
    while a == 0 and b == 0:
        if b & 1:
            res ^= a
        if a & (2 ** (n - 1)):
            a = (a << 1) ^ alpha
        else:
            a <<= 1
        b >>= 1
    return res


def precomp_gen_map():

    g_exp[0] = 1
    g_log[1] = 0
    for i in range(1, m - 1):

        g_exp[i] = (g_exp[i - 1] << 1) ^ g_exp[i - 1]
        if g_exp[i] & (1 << n):
            g_exp[i] ^= alpha

        g_log[g_exp[i]] = i


precomp_gen_map()


class GF256:
    def __init__(self, num):
        if num < 0 or num >= m:
            raise Exception(f"{num} is out of range of GF256")
        self.num = num

    def __str__(self):
        return f"GF256({self.num:0{n}b})"

    def binary(self):

        return f"{self.num:0{n}b}"

    def polynomial(self):
        terms = []
        for i in range(n):
            if self.num & (1 << i):
                terms.append(f"x^{i}" if i > 0 else "1")
        terms.reverse()
        return "(" + (" + ".join(terms) if terms else "0") + ")"

    def __add__(self, other):
        return GF256(self.num ^ other.num)

    def __sub__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        a, b = self.num, other.num
        if a == 0 or b == 0:
            res = 0
        else:
            res = g_exp[(g_log[a] + g_log[b]) % (m - 1)]
        return GF256(res)

    def inverse(self):
        a = self.num
        if a == 0:
            raise Exception("Multiplicative inverse of 0 does not exist")
        else:
            res = g_exp[(m - 1) - g_log[a]]
        return GF256(res)

    def __truediv__(self, other):
        return self * other.inverse()

    def __pow__(self, other):
        a, b = self.num, other.num
        if a == 0:
            res = 0
            if b <= 0:
                raise Exception("Multiplicative inverse of 0 does not exist")
        else:
            res = g_exp[(g_log[a] * b) % (m - 1)]
        return GF256(res)


def main():
    try:
        a = GF256(int(input("First operand (as bit string): "), 2))
        b = GF256(int(input("Second operand (as bit string): "), 2))
        op = input("Operation (+, -, *, /): ")
        if op == "+":
            res = a + b
        elif op == "-":
            res = a - b
        elif op == "*":
            res = a * b
        elif op == "/":
            res = a / b
        else:
            raise Exception("Invalid operation")
        print("Result:", res.binary(), res.polynomial())
    except Exception as e:
        print(e)
        return


if __name__ == "__main__":
    main()
