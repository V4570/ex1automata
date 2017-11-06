import argparse
from getch import _Getch
import sys


def generate_automata(_infile):
    with open(infile, 'r') as fin:

        alphabet = []
        states = []

        s = int(fin.readline())
        initial_state_id = int(fin.readline())
        num_ending_states = int(fin.readline())
        ending_states = [int(num) for num in fin.readline().split()]
        transitions = int(fin.readline())

        for i in range(s):
            states.append(State(i + 1))

        initial_state = states[initial_state_id - 1]

        auto = Automata(states, initial_state, num_ending_states, ending_states)

        for _ in range(transitions):

            state_id, char, next_state = fin.readline().split()
            state_id = int(state_id)
            next_state = int(next_state)

            if char not in alphabet:
                alphabet.append(char)

            auto.states[state_id - 1].set_connection(char, next_state)

        auto.set_alphabet(alphabet)

    return auto


class Automata(object):
    def __init__(self, states, initial_state, num_ending_states, ending_states):
        self.states = states
        self.initial_state = initial_state
        self.num_ending_states = num_ending_states
        self.ending_states = ending_states
        self.alphabet = []
        self.current_state = self.initial_state

    def change_state(self, char):
        next_state = self.current_state.next_state(char)
        self.current_state = self.states[next_state-1]
        print(self.current_state.id)

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def self_reset(self):
        self.current_state = self.initial_state

    def __str__(self):
        return 'States : {}\nInitial State : {}\nEnding States : {}\nAlphabet : {}'.format(
                                                                            [str(s) for s in self.states],
                                                                            self.initial_state,
                                                                            [es for es in self.ending_states],
                                                                            [str(l) for l in self.alphabet])


class State(object):
    def __init__(self, _id):
        self.id = _id
        self.connections = {}

    def next_state(self, char):
        return self.connections[char]

    def set_connection(self, char, next_state):
        self.connections[char] = next_state

    def __str__(self):
        return 'Id:{} - Connections:{}'.format(self.id, self.connections)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='input file')
    infile = parser.parse_args().input

    automata = generate_automata(infile)

    # print(automata)

    while True:
        _input = input('Input character or string --> ')
        if len(_input) > 1:
            for ch in _input:
                if ch not in automata.alphabet:
                    print('Charachter ''{}'' not in current automata alphabet, please try again.')
                    automata.self_reset()
                    continue
                automata.change_state(ch)
                print('Current state: {}'.format(automata.current_state.id))
        else:
            if _input not in automata.alphabet:
                print('Charachter ''{}'' not in current automata alphabet, please try again.')
                automata.self_reset()
                continue
            automata.change_state(_input)
            print('Current state: {}'.format(automata.current_state.id))

    # getch = _Getch()
    # word = ""
    # while True:
    #     # y = input('Input a character or a string--> ')
    #     x = bytes.decode(getch())
    #     if x == '\r':
    #         print('ENTER')
    #         continue
    #     elif x == '\x1b':
    #         sys.exit()
    #     print(x)
