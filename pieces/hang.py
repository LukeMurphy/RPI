import random, time


alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
alphabetLeft = []
word = "FEAR"
guessed = []
found = []
wordNotFound = True
lost = False


def guess():
	pass

def init() :
	global alphabet, alphabetLeft, guessed, found, word, wordNotFound, lost
	alphabetLeft = []
	alphabetLeft = [ a for a in alphabet]
	guessed = []
	found = []
	wordNotFound = True
	lost = False


def run() :
	global alphabet, alphabetLeft, guessed, found, word, wordNotFound, lost
	while (len(alphabetLeft) > 0 and wordNotFound == True) :
		ran = int(random.uniform(0,len(alphabetLeft)))
		char = alphabetLeft[ran]
		if (word.lower().find(char) != -1) :
			#print(char)
			found.append(char)
			if(len(found) == len(word)) :
				wordNotFound = False
		else :
			guessed.append(char)
		alphabetLeft.remove(char)
		if(len(guessed) >= 16 ) :
			lost = True
			wordNotFound = False

	if (lost == True) : 
		print ("lost", guessed)
	else :  print ("won",  guessed)

	init()

	time.sleep(1)
	run()

init()
run()


