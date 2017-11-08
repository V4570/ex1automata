import argparse
from getch import _Getch
from menu import *
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
        self.current_states = []
        self.current_states.append(self.initial_state)

    def change_state(self, char):

        temp_states = []

        for s in self.current_states:
            temp_states.append(s)

        self.current_states.clear()

        for ts in temp_states:

            try:
                next_states = ts.next_states(char)
            except KeyError:
                continue

            for ns in next_states:
                self.current_states.append(self.states[ns - 1])

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def self_reset(self):
        self.current_states.clear()
        self.current_states.append(self.initial_state)

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

    def next_states(self, char):
        return self.connections[str(char)]

    def set_connection(self, char, next_state):
        try:
            self.connections[char].append(next_state)
        except KeyError:
            self.connections[char] = []
            self.connections[char].append(next_state)

    def __str__(self):
        return 'Id:{} - Connections:{}'.format(self.id, self.connections)


def char_by_char(automata):

    getch = _Getch()

    print('\n In this option you input a character and the program will automatically\n'
          ' change state and when you press the return key print if you are in an end state or not.\n')

    while True:

        print(' (Enter a char) ')

        x = bytes.decode(getch())

        if x == '\r':
            if any((int(s.id) in automata.ending_states) for s in automata.current_states):
                print('\n You are in an end state!'
                      '\n Automata resets now!'
                      '\n Continue with another string or press ESC to exit.')
            else:
                print('\n You are not in an end state!'
                      '\n Automata resets now!'
                      '\n Continue with another string or press ESC to exit.')
            automata.self_reset()
            continue
        elif x == '\x1b':
            sys.exit()

        if x not in automata.alphabet:
            print('\r{}'.format(x))
            print(' Character {} not in current automata alphabet, please try again.'.format(x))
            automata.self_reset()
            continue

        automata.change_state(x)
        if any((int(s.id) in automata.ending_states) for s in automata.current_states):
            print('    {}'.format(x))
            print('\n You are in an end state!'
                  '\n Automata does not reset until you press return (ENTER) key.'
                  '\n Continue with another character or press ESC to exit.')
        else:
            print('    {}'.format(x))
            print('\n You are not in an end state!'
                  '\n Automata does not reset until you press return (ENTER) key.'
                  '\n Continue with another character or press ESC to exit.')


def input_string(automata):

    print('\n In this option you can input a string of characters (or even a single character)\n'
          ' and press the return key to see if you are in an end state or not.\n')

    while True:

        _input = input(' [1] > ')

        if len(_input) > 1:
            for ch in _input:
                if ch not in automata.alphabet:
                    print(' Character {} not in current automata alphabet, please try again.'.format(ch))
                    automata.self_reset()
                    continue
                automata.change_state(ch)
        else:
            if _input not in automata.alphabet:
                print(' Character {} not in current automata alphabet, please try again.'.format(_input))
                automata.self_reset()
                continue
            automata.change_state(_input)

        if any((int(s.id) in automata.ending_states) for s in automata.current_states):
            print('\n You are in an end state!\n Continue with another string or press Ctr-C to exit.')
        else:
            print('\n You are not in an end state!\n Continue with another string or press Ctr-C to exit.')
        automata.self_reset()


def start_menu():

    print(main_text)

    for i in range(len(main_menu)):
        print(' {} - {}'.format(i, main_menu[i]))

    print(' 99 - To exit the program')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='input file')
    infile = parser.parse_args().input

    automata = generate_automata(infile)

    try:
        start_menu()
        print('\n Current automata alphabet is : {}'.format(automata.alphabet))

        while True:
            choice = input('\n [Selection]> ')
            try:
                if choice == '99':
                    options[choice]()
                else:
                    options[choice](automata)
            except KeyError:
                print(' Wrong selection! Use one of the numbers provided.')
                continue
    except KeyboardInterrupt:
        sys.exit()
