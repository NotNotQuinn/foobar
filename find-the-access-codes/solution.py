# This technically works, although it takes about 1 min for 2000 random numbers between 1 and 4 inclusive.
# So I rewrote it in java, see Solution.java
def solution(l):
	divisible = []

	count = 0
	for i in range(len(l)):
		n = l[i]
		for n2 in divisible:
			if n % n2 == 0:
				count += 1
		j = 0
		while j <= i-1:
			if n % l[j] == 0:
				divisible.append(n)
			j+=1
	return count
