import sys
import os
def main():
	if ".py" in sys.argv[2]:
			print "please supply a .txt file"
	for i in range(9,24):
		value = float((float(i)/float(2.0)))
		string0 = "echo " + "threshold=" + str(value) + " >> " + sys.argv[2]
		string1  = "python " +  sys.argv[1] + " 1se8.pdb " + str(value) + " >> " + sys.argv[2]
		string2 = "echo " + '\n' + " >> " + sys.argv[2]
		os.system(string0)
		os.system(string1)
		#os.system(string2)

if __name__ == '__main__':
	main()