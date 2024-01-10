import numpy

class TrellisPath:
    def __init__(self, last_state=0):
        self._path_metric = 0
        self._path = [last_state]
        self._last_state = last_state
        self._bits_input = [None]
        self._len = 1

    def add_2_path(self, state, branch_metric, bits_input):
        self._last_state = state
        self._path.append(state)
        self._path_metric += branch_metric
        self._bits_input.append(bits_input)
        self._len += 1

    def get_path(self):
        return self._path.copy()

    def path_metric(self):
        return self._path_metric

    def last_state(self):
        return self._last_state

    def input_bits(self):
        return self._bits_input

    def __repr__(self):
        return " -> ".join(map(str, self._path))

    def __len__(self):
        return self._len

    @classmethod
    def duplicate_path(cls, path):
        if not isinstance(path, TrellisPath):
            raise ValueError("must receive a valid path")
        new_path = TrellisPath()
        new_path._path = path._path.copy()
        new_path._path_metric = path._path_metric
        new_path._last_state = path._last_state
        new_path._bits_input = path._bits_input.copy()
        new_path._len = path._len
        return new_path
