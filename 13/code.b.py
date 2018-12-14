#!/usr/bin/env python


from __future__ import print_function

from utils import parse
from utils import intersection
from utils import corner
import numpy as np
from collections import Counter



test_data = '''
/>-<\\  
|   |  
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/
'''
test_data = test_data.split('\n')[1:-1]


if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        track, carts = parse(f)

    debug = False
    if debug:
        track, carts = parse(test_data)
        assert len(carts) == 9

    assert len(carts) % 2 == 1
    carts = sorted(carts, key=lambda c: c.p)
    print('track:\n', '\n'.join(track), sep='')
    print('carts:', '\n'.join(map(str,carts)), sep='')

    for tick in range(1,22000):
        carts = sorted(carts, key=lambda c: c.p)
        for c in carts:
            if not c._alive:
                continue
            c.position += c.direction
            t = track[c.position[0]][c.position[1]] 
            if t in '/\\':
                c.direction = corner[t](c.direction)
            elif t == '+':
                c.direction = intersection[c.next_move](c.direction)
                c.next_move = (c.next_move + 1) % 3
            elif t == ' ':
                assert False
            assert t in '+-|><v^/\\', t

            # COMMENT: we need to check for a collision after each cart moves.
            # Let count the number of cart in one given location.
            collision = Counter(c.p for c in carts)
            # We want the locations where there are multiple carts
            collision_position = list(map(lambda x: x[0], filter(lambda x: x[1]>1, collision.most_common())))
            if len(collision_position) > 0:
                # Collisions occurred, remove the carts.
                print('Collision', tick, collision_position)
                for cc in carts:
                    if cc.p in collision_position:
                        cc._alive = False

        carts = list(filter(lambda x: x._alive, carts))
        print(tick)
        #if debug:
        #    print('track:\n', '\n'.join(track), sep='')
        print('carts:', '\n'.join(map(str,carts)), sep='')


        if len(carts) == 1:
            answer = carts[0].p
            break

    print(carts)
    print('Answer:', answer)
    # [Nice visualization](https://mk-hill.github.io/TrialAndError/cart-visualizer/)
    # Answer:  129,62  WRONG
    # 59,137   WRONG 
    # 138,89  WRONG
    # 69,67



'''
< collided with > at 117,62 on tick 178
15 carts left.
v collided with ^ at 147,96 on tick 307
13 carts left.
^ collided with v at 64,107 on tick 364
11 carts left.
^ collided with > at 117,53 on tick 587
9 carts left.
v collided with ^ at 20,136 on tick 633
7 carts left.
< collided with < at 33,69 on tick 1384
5 carts left.
'''
