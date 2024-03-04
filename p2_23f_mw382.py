#Michael Wong
#mw382
#31488384

def pda(test,file1):
    #PDA represented as a dictionary of dictionaries. It goes: state -> transition -> target state.
    #The Transitions are represented as tuples, being in [read, pop, push] format
    pda = {
        'q0': {tuple(['%',0,'%']): 'q1'},
        'q1': {tuple(['#',0,0]): 'q2'},
        'q2': {tuple(['N',0,0]): 'q3', tuple(['(',0,'(']): 'q2', tuple(['.',0,0]): 'q6'},
        'q3': {tuple(['N',0,0]): 'q3', tuple(['.',0,0]): 'q4'},
        'q4': {tuple(['N',0,0]): 'q4', tuple(['O',0,0]): 'q2', tuple(['>','%',0]): 'q9', tuple([')','(',0]): 'q5'},
        'q5': {tuple(['O',0,0]): 'q2', tuple(['>','%',0]): 'q9', tuple([')','(',0]): 'q5'},
        'q6': {tuple(['N',0,0]): 'q7'},
        'q7': {tuple(['O',0,0]): 'q2', tuple(['>','%',0]): 'q9', tuple(['N',0,0]): 'q7', tuple([')','(',0]): 'q8'},
        'q8': {tuple(['O', 0, 0]): 'q2', tuple(['>', '%', 0]): 'q9', tuple([')','(',0]): 'q8'}
    }

    stack = [] #The stack portion of the PDA is represented by a list. I used .append() and .pop() later in the 'for loop' to manage the stack
    print(test)
    file1.write(f'{test}\n')

    length = len(test)
    flag = False
    crashed = False

    state = 'q0'
    print(state)
    file1.write(f'{state}\n')
    for c in test:
        length = length - 1
        try:  #catches errors (such as a symbol not being part of the language) so that PDA continues
            trans = list(pda[state].keys())  # grabs the transition (the key in the 2nd or inner dictionary)
            if crashed:  # if the string crashed at anypoint, the state stays the same
                state
                print('crashed')
                file1.write('crashed\n')
            elif c.isnumeric():  # checking if character is a number, then setting the correct transition
                #This outPut variable is finding the character in any of the tuples/keys in the current state.
                #This allows us to find the next state in the dictionary for the following iteration
                outPut = [tuple for tuple in trans if any('N' == i for i in tuple)]
                state = pda[state][outPut[0]] #uses the tuple found above and uses it as the key in the second set of dictionaires
            elif c in ['+', '-', '*', '/']:  #checks if the character is an Operator, then setting the correct transition
                outPut = [tuple for tuple in trans if any('O' == i for i in tuple)]
                state = pda[state][outPut[0]]
            else:
                #The following if else statements deal with the pushing and popping of the PDA stack
                if c == '%':
                    stack.append('%') #pushes starting symbol onto stack
                elif c == '(':
                    stack.append('(') #pushes '(' to make sure there are an equal number of ')'
                elif c == ')':
                    stack.pop() #pops as many ')' as it see's. If it doesn't pop enough or too many, the next line fails
                elif c == '>':
                    popped = stack.pop()
                    if popped != '%': #if number of '()' aren't equal, then the popped symbol isn't the starting symbol, thus it crashes
                        crashed = True
                outPut = [tuple for tuple in trans if any(c == i for i in tuple)]
                state = pda[state][outPut[0]]
            print(f'({c}, {outPut[0][1]} -> {outPut[0][2]}) {state}')
            #print(stack)
            file1.write(f'({c}, {outPut[0][1]} -> {outPut[0][2]}) {state}\n')
            if length == 0 and (state == 'q9') and crashed == False:  # Checks if ending in Accept State
                flag = True
                print('accepted\n')
                file1.write('accepted\n')
        except:
            crashed = True

    if flag == False: #checks for the accept flag being set by the if statement above
        print('crashed')
        file1.write('crashed\n')
        print('rejected')
        file1.write('rejected\n')


def main():
    file1 = open('output.txt', 'w')

    print('Project 2 for CS 341, 009\n'
          'Semester: Fall 2023\n'
          'Written by: Michael Wong, mw382\n'
          'Instructor: Marvin Nakayama, marvin@njit.edu')
    file1.write('Project 2 for CS 341, 009\n'
          'Semester: Fall 2023\n'
          'Written by: Michael Wong, mw382\n'
          'Instructor: Marvin Nakayama, marvin@njit.edu\n'
                'NOTE THAT THE EPSILONS ARE REPRESENTED AS 0\n\n')

    while True:
        uIn = input('Do you want to enter a string? y for yes, n for no, or z for quick test-file output').lower()

        if uIn == 'z':
            file2 = open('input.txt', 'r')
            lines = file2.read().splitlines()
            for line in lines:
                pda(line, file1)
                print('\n')
                file1.write('\n')
            file2.close()
            continue
        if uIn == 'n':
            break

        test = input('Enter string: ').lower()
        pda(test, file1)

    file1.close()


if __name__ == "__main__":
    main()
