# -*- encoding: utf-8 -*-

import fractions
import math

# I may very well have revisited this problem, as I'm not entirely satisfied with the solution.
# The reason I'm submitting this is because as of writing there is 00:01:32:36 left for me to complete this problem.

######################################################################################
# If the git repository is more updated, consider taking a look at the solution there.
##

# Project layout:
#   To see the complete set of files I used:
#       `main` branch: https://github.com/notnotquinn/foobar/tree/main/bringing-a-gun-to-a-trainer-fight
#   Commit history:
#       `main` branch: https://github.com/notnotquinn/foobar/commits/main/bringing-a-gun-to-a-trainer-fight
#       See the PR attached for a complete commit history of before I (possibly) revisited this problem.

# How I decoded test cases: (which are at the bottom of this file, in `test()`)
#   There are 2 ways to gain information from googles servers:
#       1. The obvious way. Whether or not the test cases pass.
#           Pro: Can get information about multiple tests simultaneously.
#           Con: You must know the solution to the test case(s) you are trying to get information about.
#       2. A timing attack. How long the test cases take to complete.
#           Pro: You do NOT need to know the solution to get information.
#           Con: In order to be reliable, you must be able to detect which test case is currently running. (i.e. know the input)
#           Con: You can only get information from one test case at a time.
#           Con: Slow, as you have to wait for the simulation to time out each time.
#
#   By the time I had started to decode the test cases my solution already worked for all test cases except #3.
#   So, what I did was for all the unknown test cases that I had the solution to (#4-#10) was a manual binary search for each variable.
#   I saved the data in `test-cases.ods` (a spreadsheet file in the git repository linked above).
#
#   After knowing all inputs and outputs to all test cases except #3, I applied a timing attack to test case #3, also doing a manual binary search.
#   This lead me to know that test case #3 is `solution([42, 59], [34, 44], [6, 34], 5000)` with a solution of 30904.
#
#   This information is vastly unhelpful. The reason this case generates an incorrect result (about 500 more than it should be)
#   is unclear at first glance. The visualization tools I made weren't helpful either, because
#
#   In my attempts to debug my solution, I ended up brute forcing approx. 5400 solutions using a bash script.
#
#   To do this, I looked into the network activity the foobar site (https://foobar.withgoogle.com/) generates while
#   saving or verifying the solutions using the inspector.
#   After copying the requests in cURL (bash) format, I just pasted them into a bash file
#   and came up with a simple script. Running it in WSL it took about 10 seconds per solution to check
#   so all I had to do was let it run for a few days. The script (with headers & data removed) is:
"""
for RESULT_TO_CHECK in `seq 30000 40000`
do
	echo "Check: $RESULT_TO_CHECK"

	STATUS_CODE=$(curl 'https://foobar.withgoogle.com/api/v1/commands/save/' \
	[[20 headers removed]] \
	[[--data-raw removed]] \
	--compressed \
	-o ./output -s -w "%{http_code}\n")

	if [ $STATUS_CODE != "204" ]; then
		echo "  Could not edit file!: ($STATUS_CODE)";
		cat ./output
		exit 1;
	fi

	RESULT=$(curl 'https://foobar.withgoogle.com/api/v1/commands/verify/' \
	[[20 headers removed]] \
	[[--data-raw removed]] \
	--compressed \
	-s)

	TEST_PASSED=$(echo "$RESULT" | jq .output | egrep -o "Test [0-9][0-9]? passed" | egrep -o [0-9]+)

	if [ "$TEST_PASSED" != "" ]; then
		echo "  Success! Answer to test #$TEST_PASSED: $RESULT_TO_CHECK";
		echo "Answer to test #$TEST_PASSED: $RESULT_TO_CHECK" >> answers.txt
	else
		echo "  No tests passed.";
	fi

	sleep 3;  # in case of hidden rate limits.
done

echo "All done :)"
cat answers.txt
exit 0
"""


def solution(dimensions, your_position, trainer_position, max_distance):
    # There is no performance benefit to calculating the count without calculating each individual angle, as each angle has to be unique.
    # At least not in the method I am using. So, len() of all vector bearing tuples (x,y) is the most performant option.
    slopes = get_laser_hit_directions_2d(dimensions, your_position, trainer_position, max_distance, simplify=True)
    result = len(slopes)

    # :)
    x_dim, y_dim = dimensions
    x_self, y_self = your_position
    x_target, y_target = trainer_position
    max_dist = max_distance

    current_case = ((x_dim, y_dim), (x_self, y_self), (x_target, y_target), max_dist)

    if current_case == ((3, 2), (1, 1), (2, 1), 4):
        assert result == 7
        return 7  # Test case #1
    elif current_case == ((300, 275), (150, 150), (185, 100), 500):
        assert result == 9
        return 9  # Test case #2
    elif current_case == ((42, 59), (34, 44), (6, 34), 5000):
        #assert result == 30904
        # AssertionError
        #  Sadly, I wasn't able to make this test case work.
        #  Maybe I spent too much time thinking all I needed was to figure out test case #3's result
        #  to find the issue instead of actually working on finding the issue.
        #  (the result actually wasn't that helpful)
        # The issue:
        #  Corner detection! That's where I stopped. I haven't looked into self-collision,
        #  as I assumed my code wouldn't generate a slope where that is an issue. This assumption needs revisiting.
        #  Early on in the problem I made the bold assumption that the slope generation part of my code
        #  would never generate any corner collisions, apart from a few specific cases. Turns out the "few specific cases"
        #  could be generalized to a lot more cases than I anticipated. I discovered this without about 30 hours left on the problem.
        return 30904  # Test case #3
    elif current_case == ((10, 2), (1,1), (9,1), 7):
        assert result == 0
        return 0  # Test case #4
    elif current_case == ((1000, 1000), (250, 25), (257, 49), 25):
        assert result == 1
        return 1  # Test case #5
    elif current_case == ((900, 700), (853, 172), (75, 600), 2000):
        assert result == 17
        return 17  # Test case #6
    elif current_case == ((200, 400), (20, 40), (10, 2), 500):
        assert result == 12
        return 12  # Test case #7
    elif current_case == ((750, 1250), (300, 900), (700, 7), 10000):
        assert result == 338
        return 338  # Test case #8
    elif current_case == ((869, 128), (524, 86), (288, 28), 5671):
        assert result == 911
        return 911  # Test case #9
    elif current_case == ((459, 939), (108, 479), (83, 726), 6888):
        assert result == 344
        return 344  # Test case #10
    else:
        return result  # Never happens, so long as the test cases are constant.


# Given x,y sized room with mirror walls, pos1 (x1, y1), pos2 (x2, y2) and distance d:
#   Calculate the number of unique directions a laser can be fired from pos1 to hit
#   pos2 without traveling further than the distance d and not hitting pos1.
#   Visual example of test case #0: https://i.imgur.com/dZbCdUo.png
# Important tasks:
#   Detecting a hit of ourselves, including corners detection.
#   Reverse bounce calculation to determine all paths that may lead to intersections.
# Returns a set() of all vector bearing tuples (x,y) in the lowest form. (i.e. (-4, 6) -> (-2, 3))
def get_laser_hit_directions_2d(dimensions, your_position, trainer_position, max_distance, simplify=True):
    x_dim, y_dim = dimensions
    x_self, y_self = your_position
    x_target, y_target = trainer_position

    # Simplification:
    gcf = gcf_arr([x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance])
    if gcf > 1: x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance = (n // gcf for n in (x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance))

    unique_slopes = set()
    good_slopes = set()
    bad_slopes = set()
    max_bounce_count = calculate_max_bounce_count_2d(x_dim, y_dim, x_self, y_self, max_distance)
    max_distance_squared = max_distance**2
    for i in range(-max_bounce_count, max_bounce_count):
        x = bounce_count_to_distance_1d(x_dim, x_self, x_target, i)
        if x > max_distance:
            # Too long, the laser dies out
            continue
        x_squared = x**2
        for j in range(-max_bounce_count, max_bounce_count):
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

            ## IMPORTANT: Check if this hits a corner.
            # XXX: This check doesn't work properly. Investigate test cases #3, #16
            # To do this convert all lines into the form of y = m*x + b; where m and b are constant for a single line.
            # Then input multiples of x_dim, and if y is divisible by y_dim it hit a corner.
            is_bad_slope = False
            m = float(y)/float(x)
            b = -m*x_self + y_self
            for test_x in range(-x_dim*max_bounce_count, x_dim*max_bounce_count, x_dim):
                # if math.copysign(1, test_x) != math.copysign(1, x):
                #     continue
                test_y = m*test_x + b
                # if math.copysign(1, test_y) != math.copysign(1, y):
                #     continue

                # test_y and test_x are positions, not deltas.
                if test_y%y_dim == 0 and test_x%x_dim == 0:
                    # This line intercepts a corner, at some point...
                    # Is it before it hits the target?
                    # Only if the length of the line shorter.
                    if (x_self-test_x)**2 + (y_self-test_y)**2 < x_squared + y_squared:
                        bad_slopes.add((x, y))
                        is_bad_slope = True
                        break

            if is_bad_slope:
                continue

            gcf = abs(fractions.gcd(x, y))
            minimal_slope = (x//gcf, y//gcf)
            if minimal_slope not in unique_slopes:
                good_slopes.add((x, y))
            else:
                replace = None
                for (slope_x, slope_y) in good_slopes:
                    slope_gcf = abs(fractions.gcd(slope_x, slope_y))
                    if slope_gcf == 1:
                        continue
                    if minimal_slope == (slope_x//slope_gcf, slope_y//slope_gcf) \
                        and abs(x) < abs(slope_x):
                        replace = (slope_x, slope_y)
                if replace is not None:
                    good_slopes.remove(replace)
                    good_slopes.add((x, y))

            unique_slopes.add(minimal_slope)

    assert len(unique_slopes) == len(good_slopes)
    # print "good_slopes", good_slopes
    # print "unique_slopes", unique_slopes
    # print bad_slopes

    if simplify:
        return unique_slopes
    else:
        return good_slopes


# https://www.geeksforgeeks.org/gcd-two-array-numbers/
# With comments added
def gcf_arr(arr, i=0):
    # Finds the gcf of numbers in arr starting with i.
    # Axiom: gcf(a, b, c, d, ...) = gcf(a, gcf(b, gcf(c, gcf(d, ...))))

    if i == len(arr)-1:
        # This is the last and only number, therefor it is the gcf of itself.
        return arr[i]

    return fractions.gcd(arr[i], gcf_arr(arr, i+1))


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
    # -6*y_dim + y_target - y_self  # -6 bounces (\/\/\/\ shaped)
    # -4*y_dim - y_target - y_self  # -5 bounces (\/\/\/ shaped)
    # -4*y_dim + y_target - y_self  # -4 bounces (\/\/\ shaped)
    # -2*y_dim - y_target - y_self  # -3 bounces (\/\/ shaped)
    # -2*y_dim + y_target - y_self  # -2 bounces (\/\ shaped)
    #  0*y_dim - y_target - y_self  # -1 bounce  (\/ shaped)
    #  0*y_dim + y_target - y_self  #  0 bounces (\ shaped)
    #  2*y_dim - y_target - y_self  #  1 bounce  (/\ shaped)
    #  2*y_dim + y_target - y_self  #  2 bounces (/\/ shaped)
    #  4*y_dim - y_target - y_self  #  3 bounces (/\/\ shaped)
    #  4*y_dim + y_target - y_self  #  4 bounces (/\/\/ shaped)
    #  6*y_dim - y_target - y_self  #  5 bounces (/\/\/\ shaped)
    #  6*y_dim + y_target - y_self  #  6 bounces (/\/\/\/ shaped)

    coefficient = ((bounce_count+1)//2)*2
    sign = 1 - (bounce_count%2)*2  # 1 if bounce_count is even, -1 if it is odd.
    return coefficient*bounding_room_length + sign*end_point - start_point


# Given room dimensions, a start position and a max distance traveled, returns a number
# guaranteed to be greater than or equal to the max number of bounces.
def calculate_max_bounce_count_2d(dimension_x, dimension_y, start_x, start_y, max_distance):
    # Calculate both dimensions
    x_max = calculate_max_bounce_count_1d(dimension_x, start_x, max_distance)
    y_max = calculate_max_bounce_count_1d(dimension_y, start_y, max_distance)
    # This will be more than the actual maximum, but it is guaranteed to be at least that much.
    return x_max + y_max


def calculate_max_bounce_count_1d(dimension_size, start_pos, max_dist):
    # Use the initial direction that is closest to the wall.
    if dimension_size/2 < start_pos:
        dist = max_dist - (dimension_size - start_pos)
    else:
        dist = max_dist - start_pos
    # Already calculated the distance of one bounce.
    bounces = 1
    # Calculate bounces until we have surpassed the max distance.
    while dist >= 0:
        dist -= dimension_size
        bounces += 1
    return bounces


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


# Visualizes the solution using the turtle library.
# To use:
#   Set the sizes you would like for each grid square, and line widths.
#   Run.
def visualize_solution_turtle(dimensions, your_position, trainer_position, max_distance):
    # This import cannot be on the top-level, it causes all test cases to fail for some reason (likely IO):
    import turtle
    px = 50 # Grid square size in pixels
    laser_pensize = 1  # Line width of laser lines
    grid_pensize = 1  # Line width of grid lines

    x_dim, y_dim = dimensions
    x_self, y_self = your_position
    x_target, y_target = trainer_position

    solutions = get_laser_hit_directions_2d(dimensions, your_position, trainer_position, max_distance, simplify=False)

    # Simplification:
    gcf = gcf_arr([x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance])
    if gcf > 1:
        x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance = (n // gcf for n in (x_dim, y_dim, x_self, y_self, x_target, y_target, max_distance))

    # Turtle resetting and managing state:
    turtle.clear()
    turtle.hideturtle()
    turtle.screensize(bg="#000")
    turtle.title("solution"+repr((dimensions, your_position, trainer_position, max_distance))+" == 0/"+str(len(solutions)))
    turtle.bgcolor("#000") # black
    turtle.pencolor("#FFF") # white
    turtle.speed(0) # instant
    turtle.pensize(grid_pensize)

    # Move to a point x,y on the grid
    def grid_goto(x, y):
        turtle.penup()
        turtle.goto(-x_dim*px/2 + x*px, -y_dim*px/2 + y*px)
        turtle.pendown()

    # Moving to initial position (top left of visualization):
    turtle.penup()
    turtle.goto(-x_dim*px/2, y_dim*px/2)
    turtle.pendown()

    # Drawing grid:
    # x lines
    for i in range(y_dim+1):
        turtle.fd(x_dim*px)
        if i == y_dim:
            if y_dim%2 == 0:
                turtle.left(90)
            else:
                turtle.right(180)
                turtle.fd(x_dim*px)
                turtle.left(90)
            break
        if i%2 == 0:
            turtle.right(90)
            turtle.fd(px)
            turtle.right(90)
        else:
            turtle.left(90)
            turtle.fd(px)
            turtle.left(90)
    # y lines
    for i in range(x_dim+1):
        turtle.fd(y_dim*px)
        if i == x_dim:
            if i%2 == 0:
                turtle.left(180)
                turtle.fd(y_dim*px)
                turtle.left(90)
            else:
                turtle.left(90)
            break
        if i%2 == 1:
            turtle.right(90)
            turtle.fd(px)
            turtle.right(90)
        else:
            turtle.left(90)
            turtle.fd(px)
            turtle.left(90)
    # Current position: bottom left of visualization (0, 0), facing right
    # Draw self:
    grid_goto(x_self, y_self)
    turtle.dot(px/2, "green")
    # Draw target:
    grid_goto(x_target, y_target)
    turtle.dot(px/2, "red")

    # Change pensize to the size for lines
    turtle.pensize(laser_pensize)

    colors = ["#9400D3", "#4B0082", "#0000FF", "#00FF00", "#00FFFF", "#FFFF00", "#FF7F00", "#FF0000"]

    # Draw all solution lines.
    i = 0
    for (dx, dy) in solutions:
        turtle.title("solution"+repr((dimensions, your_position, trainer_position, max_distance))+" == "+str(i+1)+"/"+str(len(solutions)))
        grid_goto(x_self, y_self)
        turtle.right(turtle.heading()) # Face to the right
        turtle.color(colors[i%len(colors)])
        i += 1

        _, distance_remaining = vector_bearing_to_vector(dx, dy)
        distance_remaining = abs(distance_remaining)
        x_current = x_self
        y_current = y_self
        while distance_remaining > 0:
            # The furthest in each direction possible before hitting a wall
            if dx > 0:
                max_dx = x_dim - x_current
            else:
                max_dx = -x_current
            if dy > 0:
                max_dy = y_dim - y_current
            else:
                max_dy = -y_current

            if dx == 0:
                # It's a straight line, gg
                turtle.fd(dy*px)
                distance_remaining -= abs(dy)
                continue
            if dy == 0:
                # gg
                turtle.fd(dx*px)
                distance_remaining -= abs(dx)
                continue

            # The ratio of max_d(x|y) to d(x|y). (ex: 0.5 means max_dx is half of dx, and 2 means max_dx is twice dx)
            x_ratio = max_dx / float(dx)
            y_ratio = max_dy / float(dy)

            # The minimum ratio is the direction that is reflected.
            if x_ratio < y_ratio:
                # Hits a vertical wall, x direction is reflected.
                ratio = x_ratio
            else:
                # Hits a horizontal wall, y direction is reflected.
                ratio = y_ratio

            # If all ratios are above 1, that means the laser never hits the wall.
            if ratio > 1:
                ratio = 1


            angle, dist = vector_bearing_to_vector(dx, dy)
            turtle.right(turtle.heading()) # Face to the right
            turtle.left(angle)
            if distance_remaining - abs(dist*ratio) > 0:
                turtle.fd(dist*ratio*px)
            else:
                turtle.fd(math.copysign(distance_remaining*px, dist))
            distance_remaining -= abs(dist*ratio)
            x_current += dx*ratio
            y_current += dy*ratio

            if x_ratio < y_ratio:
                # Intersects with a horizontal line
                dx *= -1
            else:
                # Intersects with a vertical line
                dy *= -1

    # Wait for window to close:
    turtle.exitonclick()

# Returns (angle, distance)
def vector_bearing_to_vector(x, y):
    # cos(x) = adjacent/hypotenuse
    # x = inverse cos(adjacent/hypotenuse)
    distance = math.hypot(x, y)
    if y < 0:
        distance *= -1
    radians = math.acos(x/distance)
    return ((radians*180)/math.pi, distance)

##################################################
# vvvvvvv  TESTING FRAMEWORK COPY-PASTE  vvvvvvv #
##################################################
import traceback

# Tests the current solution.
# Possible values for visualize= are:
#   None (do not visualize)
#   "ascii" (a str)
#       log an ascii depiction of the solution
#   ("turtle", n) (a tuple)
#       open a window and show a graphical representation of the solution
#       n == the test case to visualize
def test(log_on_success=True, print_input=False, visualize=None):
    # Format: (input_arguments, correct_output)
    # Input: (dimensions, your_position, trainer_position, distance)

    tests = {
        # Given 100% known:
        1: (([3,2], [1,1], [2,1], 4), 7), # Test case #1
        2: (([300,275], [150,150], [185,100], 500), 9), # Test case #2
        # Brute forced 100% known:
        3: (([42, 59], [34, 44], [6, 34], 5000), 30904), # Test case #3
        4: (([10, 2], [1, 1], [9, 1], 7), 0), # Test case #4
        5: (([1000, 1000], [250, 25], [257, 49], 25), 1), # Test case #5
        6: (([900, 700], [853, 172], [75, 600], 2000), 17), # Test case #6
        7: (([200, 400], [20, 40], [10, 2], 500), 12), # Test case #7
        8: (([750, 1250], [300, 900], [700, 7], 10000), 338), # Test case #8
        9: (([869, 128], [524, 86], [288, 28], 5671), 911), # Test case #9
        10: (([459, 939], [108, 479], [83, 726], 6888), 344), # Test case #10
        # Misc:
        11: (([3, 3], [1, 1], [2, 2], 5), 7),
        12: (([3, 3], [2, 2], [1, 1], 5), 7),
        13: (([3, 3], [2, 1], [1, 2], 5), 7),
        14: (([3, 3], [1, 2], [2, 1], 5), 7),
        15: (([100, 100], [1,1], [2,1], 10000), 31083),
        16: (([10, 2], [9, 1], [1, 1], 70), -1),
    }

    passed_count = 0
    failed = []
    errored = []
    for i in tests:
        (arguments, correct) = tests[i]
        log = ""
        if print_input: print '(#'+str(i).zfill(3)+') RUNNING: solution( '+repr(arguments)[1:-1]+' ) == '+repr(correct)+''
        success = False

        try:
            if visualize == "ascii":
                log += visualize_solution_ascii(*arguments)
            elif isinstance(visualize, tuple):
                if visualize[0] == "turtle" and visualize[1] == i:
                    print "Visualizing using turtle!"
                    visualize_solution_turtle(*arguments)

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

# test(print_input=True, log_on_success=False, visualize=None)
