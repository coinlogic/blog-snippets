import struct 

def read_uint1(stream):
    return ord(stream.read(1))

def read_uint2(stream):
    return struct.unpack('H', stream.read(2))[0]

def read_uint4(stream):
    return struct.unpack('I', stream.read(4))[0]

def read_uint8(stream):
    return struct.unpack('Q', stream.read(8))[0]


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
      print 'Parsing block file: %s\n' % blockfile
      with open(blockfile, 'rb') as bf:
         self.magic_no = read_uint4(bf)
         print 'magic_no:\t0x%8x' % self.magic_no

         self.blocksize = read_uint4(bf)
         print 'size:    \t%u bytes' % self.blocksize



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