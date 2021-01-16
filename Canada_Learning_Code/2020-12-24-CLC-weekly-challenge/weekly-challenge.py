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

# Use Python's "PEP 8 -- Style Guide for Python Code"
# https://www.python.org/dev/peps/pep-0008/

def make_partition(sequence_S: str):
    # Build a partition to recurse.
    # sequence_S = <sequence_A> <sequence_B> <sequence_C>   (concatenation of strings)
    #   with:
    #     * <sequence_S> containing L   characters
    #     * <sequence_A> containing 1   character
    #     * <sequence_B> containing L-2 characters
    #     * <sequence_C> containing 1   character
    #
    partition_subinterval_A_begin = 0
    partition_subinterval_A_end   = partition_subinterval_A_begin + 1
    partition_subinterval_B_begin = partition_subinterval_A_end
    partition_subinterval_B_end   = len(sequence_S) - 1
    partition_subinterval_C_begin = partition_subinterval_B_end
    partition_subinterval_C_end   = partition_subinterval_C_begin + 1

    sequence_A = sequence_S [ partition_subinterval_A_begin : partition_subinterval_A_end ]
    sequence_B = sequence_S [ partition_subinterval_B_begin : partition_subinterval_B_end ]
    sequence_C = sequence_S [ partition_subinterval_C_begin : partition_subinterval_C_end ]

    return [sequence_A, sequence_B, sequence_C]

def make_palindromic_super_sequence(sequence_S: str):
    """
    Find the length of the lexicographically-lowest shortest palindromic super sequence of an arbitrary sequence.
    This is a Computer Science Ph.D. -level thing.
    The name "minSupersequence" is not a good function name at all, in my opinion as a Ph.D. doctor.

    # Proof
    # state = ABCDBA
    #   isPalindrome(ABCDBA) -> false
    #   test ABCDBA
    #        ^    ^  PASS
    #   test ABCDBA
    #         ^  ^   PASS
    #   test ABCDBA
    #          ^^    FAIL
    #   lexicographically_sorted_branches = [ABCDCBA, ABDCDBA]
    # state = ABCDCBA
    #   isPalindrome(ABCDCBA) -> true
    #   return length(ABCDCBA)

    # Proof
    # state = RACECARA
    #   isPalindrome(RACECARA) -> false
    #   test RACECARA
    #        ^      ^    FAIL
    #   lexicographically_sorted_branches = [ ARACECARA, RACECARAR ]
    # state = ARACECARA
    #   isPalindrome(ARACECARA) -> true
    #   return length(ARACECARA)

    # Proof
    # state = RACECAR
    #   isPalindrome(RACECAR) -> true
    #   return length(RACECAR)
    """

    # By definition, we already have a super sequence.
    # The only thing missing are some characters that makes it palindromic.

    # Maybe the provided string is already correct.
    if isPalindrome(sequence_S) is True:
        return sequence_S

    # Rely on isPalindrome for telling us what is palindromic and what is not.
    # We don't need to know the definition of the mathematical properties of a palindromic sequence.

    [sequence_A, sequence_B, sequence_C] = make_partition(sequence_S)

    sequence_AC = sequence_A + sequence_C
    sequence_B_is_palindromic = isPalindrome(sequence_B)
    sequence_AC_is_palindromic = isPalindrome(sequence_AC)

    if sequence_B_is_palindromic is True and sequence_AC_is_palindromic is True:
        raise Exception("The logic of isPalindrome is incorrect.")

    elif sequence_AC_is_palindromic is True:
        # Logically, B is not palindromic, but AC is palindromic
        # In that case, simply make the answer for B, and then concatenate A with answerB with C
        answer_sequence_B = make_palindromic_super_sequence(sequence_B)
        answer_ABC = sequence_A + answer_sequence_B + sequence_C
        return answer_ABC

    else:
        # Since string AC is not palindromic, the following 2 branches need to be tried:
        # * ABCA
        # * CABC.
        sequence_SA = sequence_S + sequence_A
        sequence_CS = sequence_C + sequence_S
        branches = [sequence_CS, sequence_SA]
        branches.sort()

        # Pick up the lexicographically lowest one.
        answers = list(map(make_palindromic_super_sequence, branches))
        lengths = list(map(len, answers))
        index = lengths.index(min(lengths))
        answer = answers[index]
        return answer

def lower_super_sequence(S: str):
    """
    Test the lexicographically-lowest shortest palindromic super sequence of an arbitrary sequence

    >>> lower_super_sequence("RACECAR")
    'RACECAR'

    >>> lower_super_sequence("RACECARA")
    'ARACECARA'

    >>> lower_super_sequence("ABCDBA")
    'ABCDCBA'

    >>> lower_super_sequence("ABCDBE")
    'AEBCDCBEA'

    >>> lower_super_sequence("ABCDEF")
    'ABCDEFEDCBA'

    >>> lower_super_sequence("0123456789")
    '0123456789876543210'

    >>> lower_super_sequence("CLC")
    'CLC'

    >>> lower_super_sequence("Canada")
    'CadanadaC'

    >>> lower_super_sequence("Python")
    'PnohtythonP'

    >>> lower_super_sequence("AA")
    'AA'

    >>> lower_super_sequence("AB")
    'ABA'

    >>> lower_super_sequence("BA")
    'ABA'

    >>> lower_super_sequence("Z")
    'Z'

    >>> lower_super_sequence("")
    ''
    """

    super_sequence = make_palindromic_super_sequence(S)
    return super_sequence



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

    super_sequence = make_palindromic_super_sequence(S)
    return len(super_sequence)

    pass  # remove this line and write your code below


if __name__ == "__main__":
    
    # This functions tells the Pyton Interpreter to run the tests in the function
    # documentation
    doctest.testmod()
