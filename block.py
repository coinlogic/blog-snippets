class Block(object):
   """A block to be parsed from file"""
   def __init__(self):
     self.magic_no = -1
     self.blocksize = 0
     self.blockheader = None
     transaction_cnt = 0
     transactions = None

     blockfile = None

   def parseBlockFile(self, blockfile):
      print 'Parsing block file: %s' % blockfile


def parseBlockFile(blockfile):
   block = Block()
   block.parseBlockFile(blockfile)

if __name__ == "__main__":
   import sys
   usage = "Usage: python {0} <blockfile>" 
   if len(sys.argv) < 2:
      print usage.format(sys.argv[0])
   else:
      parseBlockFile(sys.argv[1])