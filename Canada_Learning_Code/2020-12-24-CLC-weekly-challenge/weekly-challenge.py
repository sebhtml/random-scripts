import doctest

# A supersequence T of a string S is a string which contains all characters in S
# and can be chosen such that they also appear in same order as they appear in
# S, however not necessarily contiguous. For example, given

# S = "abc", T = "rqafebfewc"

# T is a supersequence of S because a appears before b and b appears before c in
# T However, given

# S = "abc", T = "acdefbefc"

# T is a supersequence of S since there are characters a,b and c such that a
# appears before b and b appears before c. Namely we choose them as such

#    (a)cdef(b)ef(c)

# (Note: even though c appears right after the first a, this is still a valid
# supersequence, since there is a c that appears after b)

# S = "abc" T = "aegcregb"

# T is NOT a supersequence of S because the characters "a", "b", "c" appear in
# the order "acb" which is not the same order as they appear in S.

# Note there is also the trivial supersequence, namely S is always a
# supersequence of itself.

# A palindrome is a string which is the same when spelled backwards, for example
# "racecar" spelled backwards is still "racecar", thus a palindrome. However
# "abc" spelled backwards is "cba", thus not a palindrome

# Given a string S find the length smallest supersequence, T, of S such that T
# is a palindrome.


def isSuperSequence(S: str, T: str):
    """
    This function helps you check whether you have understood what a
    supersequence is, however it will not be very useful for solving the
    problem.

    Returns True if T is a supersequence of S and False otherwise.
    """

    i = 0

    for t in T:
        if t == S[i]:
            i += 1

        if i == len(S):
            return True

    return False


def isPalindrome(S: str):
    """
    This function helps you check whether you have understood what a
    palindrome is, however it will not be very useful for solving the
    problem.

    Returns True if S is a palindrome and False otherwise.
    """
    i = 0
    j = len(S) - 1

    while i <= j:
        if S[i] != S[j]:
            return False
        i += 1
        j -= 1

    return True


def minSupersequence(S: str):
    """
    You can run these test cases simply by running

    $ python weekly-challenge.py

    >>> minSupersequence("RACECAR")
    7
    >>> minSupersequence("RACECARA")
    9
    >>> minSupersequence("ABCDBA")
    7
    >>> minSupersequence("ABCDBE")
    9
    >>> minSupersequence("ABCDEF")
    11
    """

    pass  # remove this line and write your code below


if __name__ == "__main__":
    
    # This functions tells the Pyton Interpreter to run the tests in the function
    # documentation
    doctest.testmod()
