from automatafactory import char_by_char, input_string
import sys

main_text = ' Select from the menu:\n'

main_menu = ['Insert characters 1 by 1',
             'Insert characters as a string']

options = {'0': char_by_char,
           '1': input_string,
           '99': sys.exit
           }
