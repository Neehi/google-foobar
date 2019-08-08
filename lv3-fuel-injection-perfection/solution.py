def solution(n):
    """
    Calculate the minimum number of operations required
    to transform the number of pellets to 1.

    The fuel control mechanisms:
    1) Add one fuel pellet
    2) Remove one fuel pellet
    3) Divide the entire group of fuel pellets by 2

    Binary can be used to determine whether to add or subtract
    when an odd number, as can be see by the following:
        3 0011 -> 2 -
        5 0101 -> 4 -
        7 0111 -> 8 +
        9 1001 -> 8 -
       11 1011 -> 12 +
       13 1101 -> 12 -
       15 1111 -> 16 +
    For all cases when the last two bits are 11, except 3, it
    is more efficient to add.

    An even number simply needs halving.

    Note: Recursion struggles on excesively large numbers.
    """
    n = int(n)

    operations = 0

    # Loop until a single pellet is left
    while n > 1:
        if n & 1:
            # Subtract if 3 or last two bits are 01b
            n += - 1 if n == 3 or n & 3 == 1 else 1
        else:
            # Simply half if even
            n >>= 1
        operations += 1

    return operations
