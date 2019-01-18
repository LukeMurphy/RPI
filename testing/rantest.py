import random

def randomRange(A=0, B=1, rounding=False):
	a = random.uniform(A,B)
	b = random.uniform(a,B)
	if rounding == False :
		return (a,b)
	else :
		return (round(a), round(b))


for i in range(0,20):
	ab = round(random.uniform(0,360))
	ab2 = randomRange(0,360,True)

	print("compare: ran {0} vs {1}".format(ab,ab2))
