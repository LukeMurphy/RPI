import time
import  threading
import numpy as np

def print_time(args):
	print "From print_time", time.time(), args

def print_some_times():
	print ("time one", time.time())
	Timer(2, print_time, ()).start()
	Timer(4, print_time, ()).start()
	#time.sleep(8)  # sleep while time-delay events execute
	print ("time two", time.time())

def setInterval(func, sec, args):
	def func_wrapper():
		func(args)
		setInterval(func, sec, args)
		
	t = threading.Timer(sec, func_wrapper)
	t.start()
	return t

#print_some_times()

#n = setInterval(print_time, .5, "fiver")
#ns = setInterval(print_time, .1, ".1er")


from nltk.corpus import wordnet as wn


listOfWords = ['lightness','being','fullness','empty','void','wholeness','blackness','empty','colorful']
listOfWords = ['meaning']

#listOfWords = ['car']


 #['arrive' 'fill' 'full' 'natural_object' 'stay']


for word in listOfWords :

	antonymList  = []
	synonymList  = []
	synonymListB  = []

	for synset in wn.synsets(word):
		for lemma in synset.lemmas() :
			synonymListB.append(str(lemma.name()))

		for hypos in synset.hyponyms() :
			for lemma in hypos.lemmas() :
				synonymListB.append(str(lemma.name()))

		for hypers in synset.hypernym_paths() :
			for hypersynset in hypers :
				for lemma in hypersynset.lemmas() :
					#synonymListB.append(str(lemma.name()))
					pass

for item in synonymListB :
	for synset in wn.synsets(item):

		if(synset.lemmas()[0].antonyms()) :
			for antonym in synset.lemmas()[0].antonyms():
				antonymList.append(str(antonym.name()))


		for lemma in synset.lemmas() :
			synonymList.append(str(lemma.name()))
			if(lemma.antonyms()) :
				for antonym in lemma.antonyms():
					antonymList.append(str(antonym.name()))


		for hypos in synset.hyponyms() :
			for lemma in hypos.lemmas() :
				synonymList.append(str(lemma.name()))
				if(lemma.antonyms()) :
					for antonym in lemma.antonyms():
						antonymList.append(str(antonym.name()))


		for hypers in synset.hypernym_paths() :
			for hypersynset in hypers :
				for lemma in hypersynset.lemmas() :
					synonymList.append(str(lemma.name()))
					if(lemma.antonyms()) :
						for antonym in lemma.antonyms():
							antonymList.append(str(antonym.name()))
	
print('')
print('-------')
print (word)
print('-------')
#print(np.unique(synonymList))
print(np.unique(synonymListB))
print('-------')
print(np.unique(antonymList))
print('-------')

def allSets() :
	for i in wn.all_synsets():
	    if i.pos() in ['a', 's']: # If synset is adj or satelite-adj.
	        for j in i.lemmas(): # Iterating through lemmas for each synset.
	            if j.antonyms(): # If adj has antonym.
	                # Prints the adj-antonym pair.
	                print j.name(), j.antonyms()[0].name()




