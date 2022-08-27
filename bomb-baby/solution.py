def solution(x, y):
	#generations = get_generations(int(x), int(y), 0)
	x = int(x)
	y = int(y)

	# Ensure X is always the larger one
	if y > x:
		x, y = y, x

	if y == 1:
		#print 'simple:', x-1
		return str(x-1)
	if y == 0 or x%y == 0 or x == y:
		#print 'simple: impossible'
		return "impossible"

	generations = get_generations_loop(x%y, y)
	if generations is not None:
		generations += x // y

	if generations is None:
		generations = 'impossible'
	else:
		generations = str(generations)

	#print 'get_generations_loop('+str(x)+' /* real: '+str(x%y)+' */, '+str(y)+'):', generations

	return generations

# Ref: https://stackoverflow.com/questions/20844517/recursive-function-to-loop-and-stack
# Ref: https://www.codeproject.com/Articles/418776/How-to-replace-recursive-functions-using-stack-and
# This is the loop version:
def get_generations_loop(x, y):
	##print 'get_generations_loop('+str(x)+', '+str(y)+')'

	# Simulation of the call stack, containing all of the required information to continue execution after a simulated call
	stack = [[
		# Inputs:
		x,					# x = 0
		y, 					# y = 1
		0, 					# depth = 2

		# Variables that are used across stages
		None, 				# a = 3
		None, 				# b = 4

		# Stage stores what part of the function to "return to" after a recursive call
		0 					# stage = 5
	]]

	# Used to store the return value of the last finished recursive call
	ret = -1
	count = 1000
	while len(stack) > 0:
		currentState = stack.pop()
		if currentState[5] == 0:

			if currentState[0] <= 0 or currentState[1] <= 0:
				ret = None
				continue

			if currentState[0] == 1 and currentState[1] == 1:
				ret = currentState[2]
				continue

			currentState[2] += 1
			currentState[5] += 1
			stack.append(currentState)
			stack.append([
				currentState[0]-currentState[1],	# x = 0
				currentState[1],					# y = 1
				currentState[2],					# depth = 2
				None,								# a = 3
				None,								# b = 4

				# This is a new call, so it is on stage 0
				0									# stage = 5
			])
			continue
		elif currentState[5] == 1:
			currentState[3] = ret
			currentState[5] += 1
   			stack.append(currentState)
   			stack.append([
				currentState[0],					# x = 0
				currentState[1]-currentState[0],	# y = 1
				currentState[2],					# depth = 2
				None,								# a = 3
				None,								# b = 4

				# This is a new call, so it is on stage 0
				0									# stage = 5
			])
			continue
		elif currentState[5] == 2:
			currentState[4] = ret

			if currentState[3] is None and currentState[4] is None:
				ret = None
				continue
			if currentState[3] is None or currentState[4] > currentState[3]:
				ret = currentState[4]
				continue
			if currentState[4] is None or currentState[3] > currentState[4]:
				ret = currentState[3]
				continue
			continue

	return ret


# This is the recursive version (not used, because of stack limits):
def get_generations(x, y, depth):
	#print 'get_generations('+str(x)+', '+str(y)+', '+str(depth)+')'

	if x <= 0 or y <= 0:
		return None

	if x == 1 and y == 1:
		return depth

	depth += 1
	a = get_generations(x-y, y, depth)
	b = get_generations(x, y-x, depth)

	if a is None and b is None:
		return None
	if a is None or b > a:
		return b
	if b is None or a > b:
		return a


# # Given tests:
# assert solution('4', '7') == "4", solution('4', '7')
# assert solution('2', '1') == "1", solution('2', '1')

# # Known tests:
# assert solution('0', '0') == "impossible", solution('0', '0')
# assert solution('1', '1') == "0", solution('1', '1')
# assert solution('2', '2') == "impossible", solution('2', '2')
# assert solution('2', '4') == "impossible", solution('2', '4')
# assert solution('3', '6') == "impossible", solution('3', '6')
# assert solution('4', '8') == "impossible", solution('4', '8')
# assert solution('5', '10') == "impossible", solution('5', '10')
# assert solution('1', '99') == "98", solution('1', '99')
# assert solution('3', '99') == "impossible", solution('3', '99')
# assert solution('3', '98') == "34", solution('3', '98')

# # Regression tests:
# assert solution('1', '92737') == "92736", solution('1', '92737')
# assert solution('2', '92737') == "46369", solution('2', '92737')
# assert solution('284', '2548') == "impossible", solution('284', '2548')
