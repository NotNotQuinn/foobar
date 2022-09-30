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


def solution(dimensions, your_position, trainer_position, max_distance):
    # There is no performance benefit to calculating the count without calculating each individual angle, as each angle has to be unique.
    # At least not in the method I am using. So, len() of all vector bearing tuples (x,y) is the most performant option.
    count = len(get_laser_hit_directions_2d(dimensions, your_position, trainer_position, max_distance))
    return count


# Given x,y sized room with mirror walls, pos1 (x1, y1), pos2 (x2, y2) and distance d:
#   Calculate the number of unique directions a laser can be fired from pos1 to hit
#   pos2 without traveling further than the distance d and not hitting pos1.
#   Visual example of test case #0: https://i.imgur.com/dZbCdUo.png
# Important tasks:
#   Detecting a hit of ourselves, including corners detection.
#   Reverse bounce calculation to determine all paths that may lead to intersections.
# Returns a set() of all vector bearing tuples (x,y) in the lowest form. (i.e. (-4, 6) -> (-2, 3))
def get_laser_hit_directions_2d(dimensions, your_position, trainer_position, max_distance):
    x_dim, y_dim = dimensions
    x_self, y_self = your_position
    x_target, y_target = trainer_position

    # Simplification:
    gcf = gcf_arr([x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance])
    if gcf > 1: x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance = (n // gcf for n in (x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance))

    good_slopes = set()
    max_distance_squared = max_distance**2
    for i in range(-10, 10):
        x = bounce_count_to_distance_1d(x_dim, x_self, x_target, i)
        x_squared = x**2
        if x_squared > max_distance_squared:
            # Too long, the laser dies out
            continue
        for j in range(-10, 10):
            y = bounce_count_to_distance_1d(y_dim, y_self, y_target, j)
            y_squared = y**2
            if x_squared + y_squared > max_distance_squared:
                # Too long, the laser dies out
                continue
            if y_squared == 0 and ((x_self < x_target and x < 0) or (x_self > x_target and x > 0)):
                # Hits the left or right wall and bounce straight back, killing us instantly!: |<->@   &   | or |   &   @<->|
                continue
            if x_squared == 0 and ((y_self < y_target and y < 0) or (y_self > y_target and y > 0)):
                # Hits the top or bottom wall, and then us. Dead.: |<->@   &   | or |   &   @<->| (but vertically)
                continue
            gcf = abs(fractions.gcd(x, y))
            good_slopes.add((x//gcf, y//gcf))

    # And now, calculate slopes that could be generated but should be removed.
    # The only types of slopes that fit this description are ones that hit the corner by traveling along the diagonal.
    # These lines would be where, using y = m*x+b: abs(m) == y_dim/x_dim.
    # Since we known abs(m), all we need to do is check if we are on one of the diagonals,
    # and calculate is the sign of x and y (for the bad slope).
    abs_m = y_dim/x_dim
    on_diagonal = False
    for b in (0, y_dim):
        if on_diagonal:
            break
        # Formula for m: m=(y-b)/x
        on_diagonal = abs((y_self-b)/x_self) == abs_m and abs((y_target-b)/x_target) == abs_m
    if on_diagonal:
        dimensions_gcf = abs(fractions.gcd(x_dim, y_dim))
        bad_slope_x, bad_slope_y = x_dim // dimensions_gcf, y_dim // dimensions_gcf

        # Calculate the sign for x and y using non-branching logic.
        invert_x_and_y = 1 - int(y_self > y_target)*2  # 1 if false, -1 if true
        invert_y = 1 - int(x_self < x_target)*2  # 1 if false, -1 if true

        bad_slope_x *= invert_x_and_y
        bad_slope_y *= invert_x_and_y*invert_y

        good_slopes.discard((bad_slope_x, bad_slope_y))  # Removes the slope if present

        # The above code does the same as this logic, but without branches (better performance):
        #   if x_self < x_target:  # Invert y
        #       if y_self > y_target:  # Invert x and y
        #           good_slopes.discard((-bad_slope_x, bad_slope_y))
        #       else:
        #           good_slopes.discard((bad_slope_x, -bad_slope_y))
        #   else:  # Don't invert y
        #       if y_self > y_target:  # Invert x and y
        #           good_slopes.discard((-bad_slope_x, -bad_slope_y))
        #       else:
        #           good_slopes.discard((bad_slope_x, bad_slope_y))

    return good_slopes


# Calculates how far an entity (ball, laser, etc) will travel when starting at start_point
# bouncing within the room bounce_count number of times, and finishing at end_point,
# assuming all movement is linear through one dimension.
# The sign of the bounce_count denotes the initial direction of travel for the entity,
# and the sign of the result will be the same as the sign of the bounce_count.
def bounce_count_to_distance_1d(bounding_room_length, start_point, end_point, bounce_count):
    # Information used to derive formula, where
    #       y_dim = bounding_room_length,
    #       y_target = end_point,
    #       y_self = start_point:
    # Each equation below is the proper calculation for the distance in 1d.
    # -6*y_dim - y_target - y_self  # -6 bounces (\/\/\/\ shaped)
    # -6*y_dim + y_target - y_self  # -5 bounces (\/\/\/ shaped)
    # -4*y_dim - y_target - y_self  # -4 bounces (\/\/\ shaped)
    # -4*y_dim + y_target - y_self  # -3 bounces (\/\/ shaped)
    # -2*y_dim - y_target - y_self  # -2 bounces (\/\ shaped)
    # -2*y_dim + y_target - y_self  # -1 bounce  (\/ shaped)
    #  0*y_dim - y_target - y_self  #  0 bounces (\ shaped)
    #  0*y_dim + y_target - y_self  #  1 bounce  (/\ shaped)
    #  2*y_dim - y_target - y_self  #  2 bounces (/\/ shaped)
    #  2*y_dim + y_target - y_self  #  3 bounces (/\/\ shaped)
    #  4*y_dim - y_target - y_self  #  4 bounces (/\/\/ shaped)
    #  4*y_dim + y_target - y_self  #  5 bounces (/\/\/\ shaped)
    #  6*y_dim - y_target - y_self  #  6 bounces (/\/\/\/ shaped)

    coefficient = (bounce_count//2)*2  # round towards -Infinity into an even number, 3 -> 2, -1 -> -2
    sign = -1 + (bounce_count%2)*2  # -1 if bounce_count is even, 1 if it is odd.
    return coefficient*bounding_room_length + sign*end_point - start_point


# Returns an ASCII representation of the room (after simplifying).
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
def visualize_solution_ascii(dimensions, your_position, trainer_position, max_distance):
    output = ""
    x_dim, y_dim = dimensions
    x_self, y_self = your_position
    x_target, y_target = trainer_position

    # Simplification:
    gcf = gcf_arr([x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance])
    if gcf > 1:
        x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance = (n // gcf for n in (x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance))
        output += "Simplified by "+str(gcf)+": "
    else:
        output += "Unable to simplify: "
    output += "solution( "+ repr(([x_dim, y_dim], [x_self, y_self], [x_target, y_target], max_distance))[1:-1] + " )\n"


    # Visualization:
    y_digit_len = len(str(y_dim))
    x_digit_len = len(str(x_dim))

    output += " "+str(y_dim).rjust(y_digit_len)+" "+"%="+"+="*(x_dim-1) + "%\n"
    for i in range(y_dim-1, 0, -1):
        # Print y number
        output += " "+str(i).rjust(y_digit_len)+" "
        if y_self == i and y_target == i:
            # Draw self and target
            if x_self < x_target:
                # Draw self first, then target
                output += "|-"+"+-"*(x_self-1)+"@-"+"+-"*(x_target-x_self-1)+"&-"+"+-"*(x_dim-x_target-1)+"|\n"
            else:
                # Draw target first, then self
                output += "|-"+"+-"*(x_target-1)+"&-"+"+-"*(x_self-x_target-1)+"@-"+"+-"*(x_dim-x_self-1)+"|\n"
        elif y_self == i:
            # Draw self
            output += "|-"+ "+-"*(x_self-1)+"@-"+"+-"*(x_dim-x_self-1)+"|\n"
        elif y_target == i:
            # Draw target
            output += "|-"+ "+-"*(x_target-1)+"&-"+"+-"*(x_dim-x_target-1)+"|\n"
        else:
            # Draw empty line
            output += "|-"+ "+-"*(x_dim-1) + "|\n"
    # Print final row and then numbers.
    output += " "+"0".rjust(y_digit_len)+" "+"%="+"+="*(x_dim-1) + "%\n"
    if x_digit_len == 1:
        # Single digits, easy!
        output += " "+" "*y_digit_len+" "
        for i in range(0, x_dim+1):
            output += str(i)+" "
    else:
        if x_digit_len > 2:
            output += " "+" "*y_digit_len + " Only the last 2 digits are shown here.\n"
        # Assuming double digits, for now
        output += " "+" "*y_digit_len + "                     "
        for i in range(10, x_dim+1):
            output += str((i//10)%10)+" "
        output += "\n "+" "*y_digit_len+" "
        for i in range(0, x_dim+1):
            output += str(i%10)+" "
    output += '\n'
    return output


# Visualizes the solution using an image
def visualize_solution_image():
    # TODO: Implement; possibly using turtle or tkinter.
    # turtle would be easiest, so long as you can control the start position
    # UPDATE: Yes, you can control it by turning off the pen and moving to the desired position.
    pass


##################################################
# vvvvvvv  TESTING FRAMEWORK COPY-PASTE  vvvvvvv #
##################################################
import traceback

def test(log_on_success=True, print_input=False, visualize=False):
    # Format: (input_arguments, correct_output)
    # Input: (dimensions, your_position, trainer_position, distance)

    tests = {
        # Given 100% known:
        0: (([3,2], [1,1], [2,1], 5), 7),
        1: (([300,275], [150,150], [185,100], 500), 9),
        # Hand-Calculated:
        2: (([3, 3], [1, 1], [2, 2], 4), 7),
        3: (([3, 3], [2, 2], [1, 1], 5), 7),
        4: (([3, 3], [2, 1], [1, 2], 5), 7),
        5: (([3, 3], [1, 2], [2, 1], 5), 7),
    }

    passed_count = 0
    failed = []
    errored = []
    for i in tests:
        (arguments, correct) = tests[i]
        log = ""
        if print_input: print '(#'+str(i).zfill(3)+') RUNNING: solution( '+repr(arguments)[1:-1]+' ) == '+repr(correct)+''
        success = False

        if visualize:
            log += visualize_solution_ascii(*arguments)

        try:
            result = solution(*arguments)
            success = result == correct
            if success:
                passed_count += 1
                log += '(#'+str(i).zfill(3)+') solution( ... ) == \x1b[32m'+repr(result)+'\x1b[0m\n' # green
            else:
                failed.append(i)
                log += '(#'+str(i).zfill(3)+') solution( ... ) == \x1b[31m'+repr(result)+' \x1b[32m['+repr(correct)+']\x1b[0m\n'
        except Exception as e:
            errored.append(i)
            # '\x1b' == 0x1B == 27 == ESC
            err_msg = traceback.format_exc()[:-1] # trim trailing newline
            log += '(#'+str(i).zfill(3)+') solution( ... ) == \x1b[41;91m[ERROR]\x1b[0m \x1b[32m['+repr(correct)+']\n\x1b[31m'+err_msg+'\x1b[0m\n'
        if len(log) > 0 and (log_on_success and success or not success): print log[:-1]
    print "Passed:", passed_count, "of", len(tests)
    if len(failed) > 0: print "Failed:", repr(failed)
    if len(errored) > 0: print "Errored:", repr(errored)

test(print_input=True, log_on_success=False, visualize=True)
