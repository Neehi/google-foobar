"""
    A ray tracing problem (sort of).

    Facts
    =====

    - A bullet can only travel a maximum distance before becoming too weak
      to cause damage.

    - If a beam hits a wall it will bounce off.

    - If a beam hits a corner it will bounce directly back.

    - If a beam hits you it will stop.

    - If a beam hits the guard it will stop.

    Assumptions
    ===========
  
    A corner collision will reflect the bullet over both axes and return in the
    direction it came from.

            ====
               /|   (+1,+1) --> (-1,-1)
              / |
             Y  |

    Based on the above, a vertical collision will reflect the bullet over the
    x-axis, with its bearing being returned with an inverse y coordinate.

             ====
              /\    (+1,+1) --> (+1,-1)
             /  \
            Y    G

    Also based on the above, a horizontal collision will reflect the bullet over
    the y-axis, with its bearing being returned with an inverse x coordinate.

            Y |
             \|     (+1,-1) --> (-1,-1)
             /|
            G |

    Solution
    ========
  
    Distance from point A to point B is calculated as:

        Sqrt((B.x - A.x)^2 + (B.y - A.y)^2)

    So, to calculate the total distance traveled, the sum of the distance of
    each line segment is used.
    

              Y |   
               \|   Sqrt((1 + 2 + 2)^2 + (1 + 2 + 2)^2) = 7.07
            G  /|
             \/ |
            ====|....
                :
                :

    In this example, the bullet reflects off three different walls, each
    requiring the intersection and reflection calculating, with the distance
    travelled having to be calculated for each section of the path.
    
    A limitation of this process is that all these calculations would be
    required for every potential path segment.

    There is a further limitation in that every possible path would require
    checking for a potential hit.

    However, an alternative approach is to utilise the reflective properties
    of the room and actually mirror the room instead.

              Y |
               \|   Sqrt(5^2 + 5^2) = 7.07
            G  /|\
            .\/.|.\..   
                :  \
                :   G'

    As can be seen above, the path from Y --> G' is the equivalent as the path from
    Y --> G, it has simply been mirrored across the x- and y-axis. The benefit is
    that only a single distance needs calculating, from Y --> G'.

    Another benefit of this alternate solution, is that only mirrored positions for
    yourself and the guard need checking, which greatly reduces the number of
    calculations and iterations needed.
"""

import math


class Vector2:
    """ 
    A partial representation of a 2D vector, to facilitate distance and bearing
    calculations used in solving the challenge.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __copy__(self):
        return self.__class__(self.x, self.y)

    copy = __copy__

    def __repr__(self):
        return '<%d, %d>' % (self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return (self.x == other.x and self.y == other.y)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        if isinstance(other, Vector2):
            return self.__class__(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return self.__class__(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x * other.x, self.y * other.y)
        elif isinstance(other, (int, float)):
            return self.__class__(self.x * other, self.y * other)
        return NotImplemented

    def __div__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.x / other.x, self.y / other.y)
        elif isinstance(other, (int, float)):
            return self.__class__(self.x / other, self.y / other)
        return NotImplemented

    def __abs__(self):
        return math.hypot(self.x, self.y)

    magnitude = __abs__

    def direction(self):
        # TODO: Fix to use proper bearing/heading
        return round(math.atan2(self.y, self.x), 7)


class Point2(Vector2):

    def distance(self, other):
        return (other - self).magnitude()


def solution(dimensions, your_position, guard_position, distance):
    # Initial bounds checks
    if (
        dimensions[0] <= 1 or
        dimensions[0] > 1250 or
        dimensions[1] <= 1 or
        dimensions[1] > 1250 or
        distance <= 1 or
        distance > 10000
    ):
        return 0

    # Setup initial positions for you and guard
    you = Point2(your_position[0], your_position[1])
    guard = Point2(guard_position[0], guard_position[1])

    # Special case for distance too short
    if distance < you.distance(guard):
        return 0

    # Get room dimensions
    x_dim, y_dim = dimensions

    # Setup mirrors to cover every increment of room size across all cardinal
    # directions
    x_mirrors = int(distance / x_dim) + 1
    y_mirrors = int(distance / y_dim) + 1

    # Dictionary of hits
    # - keyed on bearing of the hit
    # - whether it was yourself or the guard
    # - distance from yourself (only nearest stored, with you>guard)
    hits = {}

    # Loop through each room in turn and determine if a bullet hits yourself
    # and/or the guard
    for y in range(-y_mirrors, y_mirrors + 1):

        for x in range(-x_mirrors, x_mirrors +1):

            # Lambda to calculate mirrored position relative to yourself
            project = lambda P: Point2(
                x * x_dim + (P.x if x & 1 == 0 else x_dim - P.x) - you.x,
                y * y_dim + (P.y if y & 1 == 0 else y_dim - P.y) - you.y
            )

            # Check for a collision with your mirrored position
            # - distance <= max distance
            # - closest hit this bearing (allow for you>guard)
            if x or y:  # No need to check original room
                mirror = project(you)
                d = mirror.magnitude()  # Same as mirror.distance([0,0])
                if d <= distance:
                    a = mirror.direction()
                    if a not in hits or hits[a][1] >= d:
                        hits[a] = (False, d)

            # Check for a collision with the guard's mirrored position
            # - distance <= max distance
            # - closest guard hit this bearing
            mirror = project(guard)
            d = mirror.magnitude()
            if d <= distance:
                a = mirror.direction()
                if a not in hits or hits[a][1] > d:
                    hits[a] = (True, d)

    # Return the number of directions that hit the guard
    return sum(1 for v in hits.values() if v[0])
