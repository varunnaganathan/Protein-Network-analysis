import sys
import os
def main():
	if ".py" in sys.argv[2]:
			print "please supply a .txt file"
	for i in range(4,12):
		string0 = "echo " + "threshold=" + str(i) + " >> " + sys.argv[2]
		string1  = "python " +  sys.argv[1] + " 3nir.pdb " + str(i) + " >> " + sys.argv[2]
		string2 = "echo " + '\n' + " >> " + sys.argv[2]
		os.system(string0)
		os.system(string1)
		#os.system(string2)

if __name__ == '__main__':
	main()