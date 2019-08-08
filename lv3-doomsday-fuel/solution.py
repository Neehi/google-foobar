"""
Using an Absorbing Markov Chain.

    Standard form:

            A  N
      P = [ I  O ] A
          [ R  Q ] N

    A = All absorbing states
    N = All non-absorbing states
    I = Identity matrix
    O = Zero matrix
    R = Sub matrix
    Q = Sub matrix

    Fundamental matrix:

      F = (I - Q)^-1

    Limiting matrix:

     P^ = [ I  O ]
          [FR  O ]

Solution:

    1. Transform matrix into standard form
    2. Split R and Q
    3. Calculate F = (I - Q)^-1
    4. Calculate FR
    5. First line of FR contains probabilities
    6. Calculate lowest common denominator
    7. Return array of numerators and common denominator
"""

import operator
from fractions import Fraction, gcd
from itertools import starmap


def lcm(a, b):
    """ Return the lowest common multiple of two integers. """
    return int(a * b / gcd(a, b))


def determinant(A):
    """
    Calculate the determinant of matrix A.

    The determinent is calculated by taking the product of the first
    element of the top row and it's respective minor, then subtracting
    the next element and it's minor, then adding the next element and
    it's minor and so on and so forth.

    Example:
          [a b c]     [- - -]     [- - -]     [- - -]
    |A| = [d e f] = a [- e f] - b [d - f] + c [d e -]
          [g h i]     [- h i]     [g - i]     [g h -]
    """

    # Single element
    if len(A) == 1:
        return A[0][0]

    # Special case for 2x2 matrix
    if len(A) == 2 and len(A[0]) == 2:
        return A[0][0] * A[1][1] - A[1][0] * A[0][1]

    # Calculate the determinant alternately adding and subtracting
    # the product of each element of the top row with its minor
    total = 0
    for i in range(len(A)):
        C = [row[:i] + row[i+1:] for row in A[1:]]
        total += ((-1) ** (i & 1)) * A[0][i] * determinant(C)

    return total


def zero_matrix(size):
    """ Return a zero matrix of size x size. """
    return [[0] * size for j in range(size)]


def identity_matrix(size):
    """ Return an identity matrix of size x size. """
    M = zero_matrix(size)
    for x in range(size):
        M[x][x] = 1.0
    return M

    
def transpose_matrix(A):
    """ Return a transpose of matrix A. """
    return list(map(list, zip(*A)))


def cofactor_matrix(A):
    """
    Return a matrix that is the cofactor of matrix A.

    Example:
        [a b c]
    A = [d e f]
        [h i j]

        +[e f] -[d f] +[d e]
         [i j]  [h j]  [h i]
    C = -[b c] +[a c] -[a b]  where |a b| = det(a b)
         [i j]  [h j]  [h i]        |c d]      (c d)
        +[b c] -[a c] +[a b]
         [e f]  [d f]  [d e]
    """
    return [
        [((-1) ** (j+i)) * determinant([row[:i] + row[i+1:] for row in (A[:j] + A[j+1:])]) for i in range(len(A))]
        for j in range(len(A))
    ]


def adjugate_matrix(A):
    """
    Return the adjugate of matrix A.

        adj(A)  = T(C)

    1. Calculate cofactor matrix.
    2. Transpose cofacor matrix.
    """
    return transpose_matrix(cofactor_matrix(A))


def invert_matrix(A):
    """
    Return the inverse of matrix A.

        A^-1 = 1 / det(A) * adj(A)

    1. Calculate determinant.
    2. Calculate adjoint matrix.
    3. Multiply 1/determinant by adjoint matrix.
    """

    # Calculate determinant
    d = determinant(A)

    if d == 0:
        assert False  # TODO: Raise exception

    # Special case for 2x2 matrix:
    if len(A) == 2:
        return [
            [A[1][1] / d, -1 * A[0][1] / d],
            [-1 * A[1][0] / d, A[0][0] / d]
        ]

    # Calculant adjoint matrix
    C = adjugate_matrix(A)

    # 1 / det(A) * adj(A)
    return [[c / float(d) for c in row] for row in C]


def multiply_matrices(A, B):
    """ Return a matrix that is the product matrix A * B. """

    # Check matrices are compatible
    if len(A[0]) != len(B):
        assert False  # TODO: Raise exception

    return [[sum(starmap(operator.mul, zip(a_row, b_col))) for b_col in zip(*B)] for a_row in A]


def subtract_matrices(a, b):
    """ Return a matrix that is a result of subtracting matrix b from matrix a. """
    return list(map(lambda j: list(map(operator.sub, a[j], b[j])), range(len(a))))


def transform_matrix(A):
    """ Transform matrix A into standard form. """

    # Get the sums for each row
    denominators = [sum(row) for row in A]

    # Absorbing and transient states
    absorbing_states, transient_states = [], []

    # Order the colums with absorbing states first and separate the matrix into I, O, R and Q
    for j, row in enumerate(list(A)):
        if denominators[j] == 0:
            # If the row is an absorbing state set the identity
            z = [int(i == j) for i in range(len(row)) if not denominators[i]]
            x = [0] * (len(row) - len(z))
            absorbing_states.append(z + x)
        else:
            z = [float(c) / denominators[j] for i, c in enumerate(row) if not denominators[i]]
            x = [float(c) / denominators[j] for i, c in enumerate(row) if denominators[i]]
            transient_states.append(z + x)

    # Return the standard matrix
    return absorbing_states + transient_states


def solution(M):
    # Get number of absorbing states
    n = len([i for i, row in enumerate(M) if sum(row) == 0])

    if n == len(M):
        return [1, 1]  # No transient states

    # Tranform the matrix into standard form
    P = transform_matrix(M)

    # Get R and Q
    R = [row[:n] for row in P[n:]]
    Q = [row[n:] for row in P[n:]]

    # Calculate F = (I - Q)^1
    F = invert_matrix(subtract_matrices(identity_matrix(len(Q)), Q))

    # Calculate F x R
    FR = multiply_matrices(F, R)

    # Caclulate probabilities as fractions
    probabilities = [Fraction(c).limit_denominator() for c in FR[0]]

    # Calculate lowest common denominator
    lcd = reduce(lcm, [fraction.denominator for fraction in probabilities])

    # Return the list of numerators and common denominator
    return list(map(lambda x: int(x.numerator * lcd / x.denominator), probabilities)) + [int(lcd)]
