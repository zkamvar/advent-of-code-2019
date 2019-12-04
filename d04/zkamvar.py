#!/usr/bin/env python3

# --- Day 4: Secure Container ---

# You arrive at the Venus fuel depot only to discover it's protected by a
# password. The Elves had written the password on a sticky note, but someone
# threw it out.

# However, they do remember a few key facts about the password:

# - It is a six-digit number.
# - The value is within the range given in your puzzle input.
# - Two adjacent digits are the same (like 22 in 122345).
# - Going from left to right, the digits never decrease; they only ever
#   increase or stay the same (like 111123 or 135679).

# Other than the range rule, the following are true:

# - 111111 meets these criteria (double 11, never decreases).
# - 223450 does not meet these criteria (decreasing pair of digits 50).
# - 123789 does not meet these criteria (no double).

# How many different passwords within the range given in your puzzle input meet
# these criteria?

# Your puzzle input is 130254-678275.

# An Elf just remembered one more important detail: the two adjacent matching
# digits are not part of a larger group of matching digits.

# Given this additional criterion, but still ignoring the range rule, the
# following are now true:

# - 112233 meets these criteria because the digits never decrease and all
#   repeated digits are exactly two digits long.
# - 123444 no longer meets the criteria (the repeated 44 is part of a larger
#   group of 444).
# - 111122 meets the criteria (even though 1 is repeated more than twice, it
#   still contains a double 22).

# How many different passwords within the range given in your puzzle input meet
# all of the criteria?

def valid_password(password, bounds = [float("-inf"), float("inf")], old = True):

    pw = int(password)

    if len(password) is not 6:
        return(False)

    if pw < bounds[0]:
        return(False)

    if pw > bounds[1]:
        return(False)

    doubles = 0
    greating = 0
    last_double = ''
    triple = False

    for i in range(1, 6):
        b, a = int(password[i]), int(password[i-1])
        if a == b:
            doubles = doubles + 1
            # This double is just like the last match...
            if not old and b == last_double and not triple:
                triple = True
            # but it's actually two doubles.
            elif not old and triple and b == last_double:
                triple = False
            else:
                last_double = b
        else:
            last_double = ''

        if a <= b:
            greating = greating + 1

    if doubles == 0:
        return(False)

    if not old and triple:
        return(False)

    if greating is not 5:
        return(False)

    return(True)

if __name__ == '__main__':
    assert(valid_password('111111') is True)
    assert(valid_password('223450') is False)
    assert(valid_password('123789') is False)
    assert(valid_password('112233', old = False) is True)
    assert(valid_password('123444', old = False) is False)
    assert(valid_password('111122', old = False) is True)
    assert(valid_password('111111', old = False) is True)
    assert(valid_password('111112', old = False) is False)
    assert(valid_password('122222', old = False) is False)

    old_passwords = []
    passwords = []

    for i in range(130254, 678276):
        if valid_password(str(i), [130254, 678275], old = False):
            passwords.append(str(i))
        elif valid_password(str(i), [130254, 678275]):
            old_passwords.append(str(i))
        else:
            pass

    print("Pt 1: There were {} passwords".format(len(old_passwords)))
    print("Pt 2: There were {} passwords".format(len(passwords)))
