"""
Lotto649

A realistic simulation of lotto649
"""

import random


# $3 to Play
CosttoPlay = 3

# Plausable threshold on the amount of tickets sold
TicketsSold = 50000000

# Previous jackpot
Jackpot = 64000000

# Main Prize Fund (MPF) 40% of Ticket Sales
MPF = 0.40*CosttoPlay*TicketsSold

# Odds of winning
Odds = {0: 1/2.29,
        1: 1/2.421,
        2: 1/8.3,
        '2b': 1/81.2,
        3: 1/56.7,
        4: 1/1033,
        5: 1/55492,
        '5b': 1/2330636,
        6: 1/13983816}

# Pay Structure for Fixed Value Prizes (OLG)
PayStructFixed = {0: 0, 1: 0, 2: 3, '2b': 5, 3: 10}

# The Pools Fund is the remaining balance of the Main Prize
# Fund after all winnings from the fixed value prices has
# been taken away
PoolsFund = round(MPF-sum(Odds[k]*TicketsSold*PayStructFixed[k] \
    for k in PayStructFixed))

# Payout Pools (OLG)
PayStruct = {0: 0,
             1: 0,
             2: 3,
             '2b': 5,
             3: 10,
             4: 0.095 * PoolsFund,
             5: 0.05 * PoolsFund,
             '5b': 0.06 * PoolsFund,
             6: 0.795 * PoolsFund + Jackpot}

# Prevent Expectance of 0 Winners
def notzero(x):
    if x == 0:
        return 1
    else:
        return x

# Expected number of winners
Enwinners = dict((k, notzero(round(Odds[k]*TicketsSold))) for k in Odds)

# Realistic Prize Amount
RealPrize = dict((k, round(PayStruct[k]/Enwinners[k])) for k in [4,5,'5b',6])


## Auxilary Function

# Number of matching elements from two lists
def match(numbers,win_numbers):
    matches = 0
    for number in numbers:
        if number in win_numbers:
            matches += 1
    return matches


## Game Function

def lotto649():

    # Get user's numbers
    numbers = input("Please enter 6 numbers from 1 to 49 separated by spaces\n")

    # Convert from string to list
    numbers = numbers.split()
    numbers = list(int(number) for number in numbers)

    # Check for integers and only 6 numbers
    is_ints = all(type(number)==int for number in numbers)
    if not is_ints or not len(numbers) == 6:
        print("Invalid input.\n")
        lotto649()

    # Get integer > 0 for number of plays
    while True:
        nplays = int(input("How many times would you like to play?\n"))
        if nplays > 0:
            break
        print("Must play more than 0 times.\n")

    # Possible numbers
    samplespace = range(1,50)

    # Initialize results
    outcomes = {}
    outcomesbonus = {}
    winnings = 0

    # Loops through games
    for i in range(nplays):
        # Winning numbers with bonus
        win_numbers = random.sample(samplespace,6+1)
        # Choose and remove bonus
        bonus = win_numbers.pop()
        # Number of matches
        nmatches = match(numbers,win_numbers)
        # Bonus matched?
        got_bonus = bonus in numbers
        # Did we win?
        is_win = nmatches > 1
        key = nmatches
        if is_win:
            # Update key for bonus
            if got_bonus and (nmatches == 2 or nmatches == 5):
                key = str(nmatches)+'b'
            # Update winnings
            if nmatches > 3:
                # Split amongst winners
                winnings += PayStruct[key]/Enwinners[key]
            else:
                # Fixed payout
                winnings += PayStruct[key]
        # Update outcomes
        outcomes[key] = outcomes.get(key,0) + 1

    # Total profit
    profit = round(winnings - nplays*CosttoPlay)

    # Print results
    result = "".join("{0} Match: {1}\n".format(k,v) \
        for k,v in outcomes.items())
    resultwithbonus = "".join("{0}+bonus Match: {1}\n".format(k,v) \
        for k,v in outcomesbonus.items())
    print(result + "\n" + resultwithbonus)
    print("Profit: {0}".format(profit))


if __name__ == '__main__':
    lotto649()
