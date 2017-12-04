#!/usr/bin/env python
# -.- coding: utf-8 -.-
# autofact.py


import argparse
from getch import _Getch
from menu import *
from builtins import input
import sys

'''
    Method that reads a file that describes a given automata.
    File format example:
        3   #Number of states in the automata
        1   #Id of the first state
        2   #Number of final states
        2 3 #Id of the final states
        6   #Number of max transitions
        1 a 2   # Possible transitions.
        1 b 1
        2 a 3
        2 b 1
        3 a 3
        3 b 1
'''


def start_menu():
    BLUE = '\33[94m'

    sys.stdout.write(BLUE + """
  ___        _       ______         _   
 / _ \      | |      |  ___|       | |  
/ /_\ \_   _| |_ ___ | |_ __ _  ___| |_ 
|  _  | | | | __/ _ \|  _/ _` |/ __| __|
| | | | |_| | || (_) | || (_| | (__| |_ 
\_| |_/\__,_|\__\___/\_| \__,_|\___|\__|
                                    v0.1
"""
)
    sys.stdout.flush()
    sys.stdout.write(main_text)

    for i in range(len(main_menu)):
        sys.stdout.write(' {} - {}'.format(i, main_menu[i]))

    sys.stdout.write(' 99 - To exit the program')


def generate_automata(_infile):
    with open(infile, 'r') as fin:

        alphabet = []
        states = []

        s = int(fin.readline())
        initial_state_id = int(fin.readline())
        num_ending_states = int(fin.readline())
        ending_states = [int(num) for num in fin.readline().split()]
        transitions = int(fin.readline())

        # For each id that was read we create a State object
        for i in range(s):
            states.append(State(i + 1))

        auto = Automata(states, initial_state_id, num_ending_states, ending_states)

        for _ in range(transitions):

            state_id, char, next_state = fin.readline().split()
            state_id = int(state_id)
            next_state = int(next_state)

            if char not in alphabet and char != '@':
                alphabet.append(char)

            auto.states[state_id - 1].set_connection(char, next_state)

        auto.set_alphabet(alphabet)

    return auto


class Automata(object):
    def __init__(self, states, initial_state_id, num_ending_states, ending_states):
        self.states = states
        self.initial_state = self.states[initial_state_id - 1]
        self.num_ending_states = num_ending_states
        self.ending_states = ending_states
        self.alphabet = []
        self.current_states = []
        self.current_states.append(self.initial_state)

    def add_epsilon_states(self):
        previous_len = len(self.current_states)
        for st in self.current_states:
            try:
                next_states = st.next_states('@')
            except KeyError:
                continue

            for ns in next_states:
                next_s = self.states[ns - 1]
                if next_s not in self.current_states:
                    self.current_states.append(next_s)

        if previous_len > len(self.current_states):
            self.add_epsilon_states()

    def change_state(self, char):

        temp_states = []

        for s in self.current_states:
            temp_states.append(s)

        del self.current_states[:]

        for ts in temp_states:

            try:
                next_states = ts.next_states(char)
            except KeyError:
                continue

            for ns in next_states:
                self.current_states.append(self.states[ns - 1])

        self.add_epsilon_states()

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def self_reset(self):
        del self.current_states[:]
        self.current_states.append(self.initial_state)
        self.add_epsilon_states()

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

    sys.stdout.write('\n In this option you input a character and the program will automatically\n'
                     'change state and when you press the return key sys.stdout.write if you are in an end state or '
                     'not.\n')

    while True:

        sys.stdout.write('\n (Enter a char) ')

        try:
            x = bytes.decode(getch())
        except TypeError:
            x = getch()

        if x == '\r':
            if any((int(s.id) in automata.ending_states) for s in automata.current_states):
                sys.stdout.write('\n You are in an end state!'
                                 '\n Automata resets now!'
                                 '\n Continue with another string or press ESC to exit.')
            else:
                sys.stdout.write('\n You are not in an end state!'
                                 '\n Automata resets now!'
                                 '\n Continue with another string or press ESC to exit.')
            automata.self_reset()
            continue
        elif x == '\x1b':
            sys.exit()

        if x not in automata.alphabet:
            sys.stdout.write('\r{}\n'.format(x))
            sys.stdout.write(' Character {} not in current automata alphabet, please try again.\n'.format(x))
            automata.self_reset()
            continue

        automata.change_state(x)
        if any((s.id in automata.ending_states) for s in automata.current_states):
            sys.stdout.write('    {}'.format(x))
            sys.stdout.write('\n You are in an end state!'
                             '\n Automata does not reset until you press return (ENTER) key.'
                             '\n Continue with another character or press ESC to exit.')
        else:
            sys.stdout.write('    {}'.format(x))
            sys.stdout.write('\n You are not in an end state!'
                             '\n Automata does not reset until you press return (ENTER) key.'
                             '\n Continue with another character or press ESC to exit.')


def input_string(automata):
    sys.stdout.write('\n In this option you can input a string of characters (or even a single character)\n'
                     ' and press the return key to see if you are in an end state or not.\n')

    while True:

        _input = str(input(' [1] > '))

        if len(_input) > 1:
            for ch in _input:
                if ch not in automata.alphabet:
                    sys.stdout.write(' Character {} not in current automata alphabet, please try again.\n'.format(ch))
                    automata.self_reset()
                    continue
                automata.change_state(ch)
        else:
            if _input not in automata.alphabet:
                sys.stdout.write(' Character {} not in current automata alphabet, please try again.\n'.format(_input))
                automata.self_reset()
                continue
            automata.change_state(_input)

        if any((s.id in automata.ending_states) for s in automata.current_states):
            sys.stdout.write('\n You are in an end state!\n Continue with another string or press Ctr-C to exit.\n')
        else:
            sys.stdout.write('\n You are not in an end state!\n Continue with another string or press Ctr-C to exit.\n')
        automata.self_reset()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='input file')
    infile = parser.parse_args().input

    automata = generate_automata(infile)
    automata.add_epsilon_states()

    try:
        start_menu()
        sys.stdout.write('\n Current automata alphabet is : {}'.format(automata.alphabet))

        while True:
            choice = str(input('\n [Selection]> '))
            try:
                if choice == '99':
                    options[choice]()
                else:
                    options[choice](automata)
            except KeyError:
                sys.stdout.write(' Wrong selection! Use one of the numbers provided.')
                continue
    except KeyboardInterrupt:
        sys.exit()
