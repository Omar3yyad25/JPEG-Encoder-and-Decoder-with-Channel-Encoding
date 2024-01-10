import math
from TrellisPath import *

class ConvolutionalCode:
    """The code assumes zero state termination, and k=1"""
    def __init__(self, generators: tuple):
        """
        :param generators: each element in the tuple represents a single generator polynomial. The convention
        we use is: 1+D =b011 = 3 (and not 1+D=6).
        """
        self.n = len(generators)
        self.k = 1
        self.rate = self.k / self.n
        self.constraint_length = math.floor(math.log(max(generators), 2))
        self.number_of_states = 2 ** self.constraint_length
        self.state_space = tuple(range(self.number_of_states))
        self.generators = generators

        self._build_fsm(generators)

    def _build_fsm(self, generators: tuple):
        possible_inputs = tuple(range(2 ** self.k))
        self.next_states = {}
        self.out_bits = {}
        for current_state in self.state_space:
            self.next_states[current_state] = {}
            self.out_bits[current_state] = {}

            for current_input in possible_inputs:

                new_state = (current_input << (self.constraint_length - 1)) + (current_state >> self.k)
                self.next_states[current_state][current_input] = new_state

                tmp = []
                for fwd in generators:
                    bit_reversed_fwd = int('{:0{width}b}'.format(fwd, width=self.constraint_length+1)[::-1], 2)
                    lsr = (current_input << self.constraint_length) + current_state
                    generator_masked_sum_arg = bit_reversed_fwd & (lsr)  # mask input and state with fwd
                    tmp.append(bin(generator_masked_sum_arg).count("1") % 2)  # sum bit mod 2 (XOR)

                self.out_bits[current_state][current_input] = tuple(tmp)

    def encode(self, data: bytes) -> list[int]:
        """
        encode input data bytes
        :param data: date to be encoded
        :return: encoded data bits, as a list of integers of value 0 or 1
        :rtype: bytes
        """
        input_bits = [0] * (self.constraint_length + len(data) * 8)
        coded_bits = [0] * int(len(input_bits)/self.rate)

        for byte_idx, byt in enumerate(data):
            bits = '{:08b}'.format(byt)
            input_bits[8*byte_idx:8*byte_idx+8] = bits

        current_state = 0
        for bit_idx, bit in enumerate(input_bits):
            outputs = list(self.out_bits[current_state][int(bit)])
            coded_bits[self.n*bit_idx: self.n*(bit_idx+1)] = outputs
            current_state = self.next_states[current_state][int(bit)]

        return coded_bits


    def print_generators(self):
        for generator_idx, generator_p in enumerate(self.generators):
            binary_rep = '{:0{width}b}'.format(generator_p, width=self.constraint_length+1)[::-1]
            function_rep = ""
            for bit_idx, bit in enumerate(binary_rep):
                if bit == "1":
                    if bit_idx == 0:
                        function_rep = "1 + "
                    else:
                        function_rep = function_rep + "x^" + str(bit_idx) + " + "
            if len(function_rep) > 3:
                function_rep = function_rep[:-3]
            print("generator no. " + str(generator_idx) + ": "+ function_rep)

    def print_fsm(self):
        possible_inputs = tuple(range(2 ** self.k))
        for state in self.state_space:
            for current_input in possible_inputs:
                print("current state: ", state, ", current input: ", current_input, ", new state: ",
                      self.next_states[state][current_input], ", encoder output:", self.out_bits[state][current_input])
