from config import *


def encode_to_binary(v, s, ub, lb):
    R = ub - lb
    encoded = ((v - lb) / R) * (2 ** s - 1)

    if v < 0:  # Check if negative
        encoded *= -1

    decimal = int(encoded)
    return bin(decimal).replace("-", "")[2:].zfill(s)


def decode_to_actual(b, s, ub, lb):
    decimal = int(b, 2)

    R = ub - lb
    actual = (decimal / (2 ** s - 1)) * R + lb
    return actual


# From https://stackoverflow.com/questions/18854620/whats-the-best-way-to-split-a-string-into-fixed-length-chunks-and-work-with-the
def chunk_string(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


def binary_string_to_individual(string):
    individual = Individual()
    binary_array = list(chunk_string(string, BINARY_CODE_LENGTH))

    gamma = 0.0
    for num, v in enumerate(binary_array):
        if num % 2 == 0:
            gamma = decode_to_actual(v, BINARY_CODE_LENGTH, GAMMA_CONSTRAINTS[1], GAMMA_CONSTRAINTS[0])
        else:
            beta = decode_to_actual(v, BINARY_CODE_LENGTH, BETA_CONSTRAINTS[1], BETA_CONSTRAINTS[0])
            individual.add_parameter(gamma, beta)

    return individual


class Individual:

    def __init__(self):
        self.gammas = []
        self.betas = []

    def __str__(self):
        out = []
        j = 0
        for gamma, beta in zip(self.gammas, self.betas):
            out.append(f"    gamma_{j}: {gamma}")
            out.append(f"    beta_{j}:  {beta}")
            j += 1

        return "{\n" + ",\n".join(out) + "\n}"

    def add_parameter(self, gamma, beta):
        self.gammas.append(gamma)
        self.betas.append(beta)

    def get_binary_string(self):
        binary = ""
        for gamma, beta in zip(self.gammas, self.betas):
            binary += (encode_to_binary(gamma, BINARY_CODE_LENGTH, GAMMA_CONSTRAINTS[1], GAMMA_CONSTRAINTS[0]))
            binary += (encode_to_binary(beta, BINARY_CODE_LENGTH, BETA_CONSTRAINTS[1], BETA_CONSTRAINTS[0]))
        return binary
