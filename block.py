def parseBlockFile(blockfile):
   print 'Parsing block file: %s' % blockfile

if __name__ == "__main__":
   import sys
   usage = "Usage: python {0} <blockfile>" 
   if len(sys.argv) < 2:
      print usage.format(sys.argv[0])
   else:
      parseBlockFile(sys.argv[1])