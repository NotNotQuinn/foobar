# -*- encoding: utf-8 -*-

import fractions
import math

# https://www.geeksforgeeks.org/gcd-two-array-numbers/
# With comments added
def gcf_arr(arr, i=0):
    # Finds the gcf of numbers in arr starting with i.
    # Axiom: gcf(a, b, c, d, ...) = gcf(a, gcf(b, gcf(c, gcf(d, ...))))

    if i == len(arr)-1:
        # This is the last and only number, therefor it is the gcf of itself.
        return arr[i]

    a = arr[i]
    b = gcf_arr(arr, i+1)

    return fractions.gcd(a, b)

# Remove greatest common factor from an array of numbers.
# Returns the array with each number divided by gcf.
def remove_gcf_arr(arr):
    gcf = abs(gcf_arr(arr))
    if gcf == 1:
        return arr
    return [x // gcf for x in arr]

# Given x,y sized room with mirror walls, pos1 (x1, y1), pos2 (x2, y2) and distance d:
#   Calculate the number of unique directions a laser can be fired from pos1 to hit
#   pos2 without traveling further than the distance d and not hitting pos1.
#   Visual example of test case #0: https://i.imgur.com/dZbCdUo.png
# Important tasks:
#   Corner detection (corner = hit self or expire, therefor it is no match)
#   Intersection detection
#   Reverse bounce simulation to determine all paths that may lead to intersections.
#   + more
def solution(dimensions, your_position, trainer_position, max_distance):
    x_dim, y_dim = dimensions
    x_self, y_self = your_position
    x_target, y_target = trainer_position

    # Simplification:
    gcf = gcf_arr([x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance])
    if gcf > 1:
        x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance = (n // gcf for n in (x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance))
        print "Simplified by "+str(gcf)+":",
    else:
        print "Unable to simplify:",
    print "solution(", repr(([x_dim, y_dim], [x_self, y_self], [x_target, y_target], max_distance))[1:-1] + " )"

    if x_dim < 100:
        visualize_room([x_dim, y_dim], [x_self, y_self], [x_target, y_target], max_distance)
    else:
        print "Visualization skipped due to size of room. (x dimension >= 100)"

    solutions = []
    max_distance_squared = max_distance**2
    for i in range(-10, 10):
        for j in range(-10, 10):
            x = bounce_count_to_distance_1d(x_dim, x_self, x_target, i)
            y = bounce_count_to_distance_1d(y_dim, y_self, y_target, j)
            if x**2 + y**2 <= max_distance_squared:
                solutions.append((bounce_count_to_distance_1d(x_dim, x_self, x_target, i), bounce_count_to_distance_1d(y_dim, y_self, y_target, j)))

    print solutions
    print set([tuple(remove_gcf_arr(s)) for s in solutions])


# Calculates how far an entity (ball, laser, etc) will travel when starting at start_point
# bouncing within the room bounce_count number of times, and finishing at end_point,
# assuming all movement is linear.
def bounce_count_to_distance_1d(bounding_room_length, start_point, end_point, bounce_count):
    # Information used to derive formula, where
    #       y_dim = bounding_room_length,
    #       y_target = end_point,
    #       y_self = start_point:
    # -y_dim*6 + y_target - y_self  # -6 bounces (\/\/\/\ shaped)
    # -y_dim*4 - y_target - y_self  # -5 bounces (\/\/\/ shaped)
    # -y_dim*4 + y_target - y_self  # -4 bounces (\/\/\ shaped)
    # -y_dim*2 - y_target - y_self  # -3 bounces (\/\/ shaped)
    # -y_dim*2 + y_target - y_self  # -2 bounces (\/\ shaped)
    # -y_dim*0 - y_target - y_self  # -1 bounce  (\/ shaped)
    #  y_dim*0 + y_target - y_self  #  0 bounces (\ shaped)
    #  y_dim*2 - y_target - y_self  #  1 bounce  (/\ shaped)
    #  y_dim*2 + y_target - y_self  #  2 bounces (/\/ shaped)
    #  y_dim*4 - y_target - y_self  #  3 bounces (/\/\ shaped)
    #  y_dim*4 + y_target - y_self  #  4 bounces (/\/\/ shaped)
    #  y_dim*6 - y_target - y_self  #  5 bounces (/\/\/\ shaped)
    #  y_dim*6 + y_target - y_self  #  6 bounces (/\/\/\/ shaped)

    coefficient = math.trunc(float(bounce_count+1)/2)*2
    return bounding_room_length*coefficient + (1 if bounce_count%2 == 0 else -1)*end_point - start_point



# Prints an ASCII representation of the room (without simplifying) to standard output.
# Accepts the same arguments as solution() but does not use max_distance.
# Legend:
#   "@" = ourselves
#   "&" = target
# Helpful graphics, especially for larger sized rooms.
# This is a sample graphic for solution( [3, 2], [1, 1], [2, 1], 4 ):
#   2 %=+=+=%
#   1 |-@-&-|
#   0 %=+=+=%
#     0 1 2 3
def visualize_room(dimensions, your_position, trainer_position, max_distance):
    x_dim, y_dim = dimensions
    x_self, y_self = your_position
    x_target, y_target = trainer_position

    # Visualization:
    y_digit_len = len(str(y_dim))
    x_digit_len = len(str(x_dim))

    print " "+str(y_dim).rjust(y_digit_len)+" "+"%="+"+="*(x_dim-1) + "%"
    for i in range(y_dim-1, 0, -1):
        # Print y number
        print " "+str(i).rjust(y_digit_len),
        if y_self == i and y_target == i:
            # Draw self and target
            if x_self < x_target:
                # Draw self first, then target
                print "|-"+"+-"*(x_self-1)+"@-"+"+-"*(x_target-x_self-1)+"&-"+"+-"*(x_dim-x_target-1)+"|"
            else:
                # Draw target first, then self
                print "|-"+"+-"*(x_target-1)+"&-"+"+-"*(x_self-x_target-1)+"@-"+"+-"*(x_dim-x_self-1)+"|"
        elif y_self == i:
            # Draw self
            print "|-"+ "+-"*(x_self-1)+"@-"+"+-"*(x_dim-x_self-1)+"|"
        elif y_target == i:
            # Draw target
            print "|-"+ "+-"*(x_target-1)+"&-"+"+-"*(x_dim-x_target-1)+"|"
        else:
            # Draw empty line
            print "|-"+ "+-"*(x_dim-1) + "|"
    # Print final row and then numbers.
    print " "+"0".rjust(y_digit_len)+" "+"%="+"+="*(x_dim-1) + "%"
    if x_digit_len == 1:
        # Single digits, easy!
        print " "+" "*y_digit_len,
        for i in range(0, x_dim+1):
            print i,
        print
    else:
        if x_digit_len > 2:
            print " "+" "*y_digit_len + " Only the last 2 digits are shown here."
        # Assuming double digits, for now
        print " "+" "*y_digit_len + "                    ",
        for i in range(10, x_dim+1):
            print (i//10)%10,
        print "\n "+" "*y_digit_len,
        for i in range(0, x_dim+1):
            print i%10,
        print




##################################################
# vvvvvvv  TESTING FRAMEWORK COPY-PASTE  vvvvvvv #
##################################################
import traceback

def test(print_success=True, print_input=False):
    # Format: (input, correct_output)
    # Input: (dimensions, your_position, trainer_position, distance)

    tests = {
        # Given 100% known:
        0: (([3,2], [1,1], [2,1], 4), 7),
        1: (([300,275], [150,150], [185,100], 500), 9)
    }

    for i in tests:
        (case, correct) = tests[i]
        if print_input: print '(#'+str(i).zfill(3)+') RUNNING: solution( '+repr(case)[1:-1]+' )'
        success = False

        try:
            r = solution(case[0], case[1], case[2], case[3])
            success = r == correct
            if success:
                if not success or (success and print_success): print '(#'+str(i).zfill(3)+') solution( ... ) == \x1b[32m'+repr(r)+'\x1b[0m' # green
            else:
                if not success or (success and print_success): print '(#'+str(i).zfill(3)+') solution( ... ) == \x1b[31m'+repr(r)+' \x1b[32m['+repr(correct)+']\x1b[0m'
        except Exception as e:
            # '\x1b' == 0x1B == 27 == ESC
            err_msg = traceback.format_exc()[:-1] # trim trailing newline
            print '(#'+str(i).zfill(3)+') solution( ... ) == \x1b[41;91m[ERROR]\x1b[0m \x1b[32m['+repr(correct)+']\n\x1b[31m'+err_msg+'\x1b[0m'

test(print_input=True, print_success=True)
