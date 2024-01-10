import math
from TrellisPath import *

class DecodingError(Exception):
    """Raised if no path ends in the zero state"""
    pass


def decode(self, data: list[int]) -> (bytes, int):
        """
        decode data bytes
        :param data: coded data to be decoded, list of ints representing each received bit.
        :return: return a tuple of decoded data, and the amount of corrected errors.
        :rtype: (bytes, int)
        The function assumes initial and final state of encoder was at the zero state
        """
        received_codewords = [tuple(data[i: i+self.n]) for i in range(0, len(data), self.n)]

        surviving_paths = [TrellisPath()]

        for codeword in received_codewords:  # iterate over time (received codewords)
            # obtain branch metrics
            possible_transitions = []
            # find branch metrics
            for path in surviving_paths:
                for possible_input in range(2**self.k):
                    # for each path and possible input find possible output, and branch metric
                    last_state = path.last_state()
                    next_state = self.next_states[last_state][possible_input]
                    possible_output = self.out_bits[last_state][possible_input]
                    branch_metric = sum(tuple(possible_output[i]^codeword[i] for i in range(len(codeword))))
                    possible_transitions.append([next_state, branch_metric + path.path_metric(), branch_metric, path,
                                                 possible_input])

            # select survivors by inspecting paths entering a state
            new_paths = []
            for state in self.state_space:
                entering_paths = tuple(filter(lambda x: x[0] == state, possible_transitions))
                # initially there may be less paths than states, since we assume initialization at zero state
                if len(entering_paths):
                    selected = min(entering_paths, key=lambda x: x[1])
                    selected_path: TrellisPath = selected[3]
                    new_path = TrellisPath.duplicate_path(selected_path)
                    new_path.add_2_path(state, selected[2], selected[4])
                    new_paths.append(new_path)
            surviving_paths = new_paths

        # choose ML path
        chosen_path = None
        for path in surviving_paths:
            if path.last_state() == 0:  # as a result of zero tailing
                chosen_path = path
                break
        if chosen_path is None:
            raise DecodingError

        decoded_bits = chosen_path.input_bits()[1:-int(self.constraint_length)]
        mapped = "".join(map(str, decoded_bits))
        decoded_bytes = bytes([int(mapped[i:i + 8], 2) for i in range(0, len(mapped), 8)])
        chosen_path.path_metric()
        return decoded_bytes, chosen_path.path_metric()