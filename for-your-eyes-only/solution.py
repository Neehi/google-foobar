"""
    You've completed all the levels!!

    Problem:

    An encrypted message, but what does it say?

    <encrypted>
    FU4QHk0QCxIDQk5TQ0xJAQsABEJCSUQIQR8CBBECGwxESxRTSQQDEQsMDg5KVEJBVwAIDwwZWgBJ
    QUpFSQANCFwWCggSCQtOT0sJEg0JGQAYDA4OQAdJQUpFSRwNB0EQBQQUQkJJRBlPEQwIBBZJSVlL
    CQAPBxVCQklEDUEcSUFKRUkeCgUPVBM=
    </encrypted>

    For your eyes only!

    Solution:

    The first thing that jumps out is the '=' at the end. Base64?

    Running it through a simple base64 decode, it does appear to be base64 at
    least, though it's clearly encrypted.

    Taking "For your eyes only!" as a clue, perhaps my username is the key,
    though I have no idea what form of encryption it might be.

    There was an XOR pattern used in one of the early challenges, so try a 
    simple rolling XOR pattern using my user name as the key.

    Answer:
        {
            'success' : 'great',
            'colleague' : 'esteemed',
            'efforts' : 'incredible',
            'achievement' : 'unlocked',
            'rabbits' : 'safe',
            'foo' : 'win!'
        }
"""

import base64

encrypted = 'FU4QHk0QCxIDQk5TQ0xJAQsABEJCSUQIQR8CBBECGwxESxRTSQQDEQsMDg5KVEJBVwAIDwwZWgBJQUpFSQANCFwWCggSCQtOT0sJEg0JGQAYDA4OQAdJQUpFSRwNB0EQBQQUQkJJRBlPEQwIBBZJSVlLCQAPBxVCQklEDUEcSUFKRUkeCgUPVBM='
decrypted = ''

key = 'nick.snape'

x = 0
for i, c in enumerate(base64.b64decode(encrypted)):
    decrypted += chr(c ^ ord(key[i % len(key)]))

print(decrypted)
