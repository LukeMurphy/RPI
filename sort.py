from operator import itemgetter 
from collections import OrderedDict


quadBlocks =  {
"tail":	{"order":3, "proportions":[1, 1.5] ,"coords":[]},

"rl1":	{"order":1, "proportions":[1.8, 3.4] ,"coords":[]},
"rl2":	{"order":2, "proportions":[1.8, 4] ,"coords":[]},

"fl1":	{"order":1, "proportions":[2, 3.8] ,"coords":[]},
"fl2":	{"order":2, "proportions":[1.8, 3.5] ,"coords":[]},

"head":	{"order":6, "proportions":[3, 3.67],"coords":[]},
"body":	{"order":4, "proportions":[9, 14],"coords":[]},

"cavity":{"order":5, "proportions":[6, 10],"coords":[]},
}



quadBlocks = {"aa": 3, "bb": 4, "cc": 2, "dd": 1}


quadBlocks = [(k, quadBlocks[k]) for k in sorted(quadBlocks, key=quadBlocks.get, reverse=False)]


quadBlocks = {"aa": {"order": 3}, "q": {"order": 4}, "cc": {"order": 2}, "dd": {"order": 1}}

for k, v in quadBlocks.items() :
	print (k,v)


quadBlocks = sorted(quadBlocks.items(), key = lambda t: t[1]["order"])

print(quadBlocks)

#quadBlocks = OrderedDict(sorted(quadBlocks.items(), key=lambda t: (t[1]))

#quadBlocks = [(k, quadBlocks[k]) for k in sorted(quadBlocks.items(), key=quadBlocks.get, reverse=False)]


#print(quadBlocks)


#quadBlocks = OrderedDict(sorted(quadBlocks.items(), key=lambda t: t[1]))
#quadBlocks = (OrderedDict(sorted(quadBlocks.items(), key = quadBlocks.get, reverse = False)))

numSquarePairs = len(quadBlocks)