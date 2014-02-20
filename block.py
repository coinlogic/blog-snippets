import struct, datetime

def read_uint1(stream):
   return ord(stream.read(1))

def read_uint2(stream):
   return struct.unpack('H', stream.read(2))[0]

def read_uint4(stream):
   return struct.unpack('I', stream.read(4))[0]

def read_uint8(stream):
   return struct.unpack('Q', stream.read(8))[0]

def read_hash32(stream):
   return stream.read(32)[::-1] #reverse it since we are little endian

def read_merkle32(stream):
   return stream.read(32)[::-1] #reverse it

def read_time(stream):
   utctime = read_uint4(stream)
   #Todo: convert to datetime object
   return utctime

def read_varint(stream):
   ret = read_uint1(stream)

   if ret < 0xfd: #one byte int 
      return ret
   if ret == 0xfd: #unit16_t in next two bytes
      return read_uint2(stream)
   if ret == 0xfe: #uint32_t in next 4 bytes
      return read_uint4(stream)
   if ret == 0xff: #uint42_t in next 8 bytes
      return read_uint8(stream)
   return -1

def get_hexstring(bytebuffer):
   return ''.join(('%x'%ord(a)) for a in bytebuffer)



class BlockHeader(object):
   """BlockHeader represents the header of the block"""
   def __init__(self):
      super( BlockHeader, self).__init__()
      self.version = None
      self.prevhash = None
      self.merklehash = None
      self.time = None
      self.bits = None
      self.nonce = None

   def parse(self, stream):
      #TODO: error checking

      self.version = read_uint4(stream)
      self.prevhash = read_hash32(stream)
      self.merklehash = read_merkle32(stream)
      self.time = read_time(stream)
      self.bits = read_uint4(stream)
      self.nonce = read_uint4(stream)

   def __str__(self):
      return "\n\t\tVersion: %d \n\t\tPreviousHash: %s \n\t\tMerkle: %s \n\t\tTime: %s \n\t\tBits: %8x \n\t\tNonce: %8x" % (self.version, \
               get_hexstring(self.prevhash), \
               get_hexstring(self.merklehash), \
                str(self.time), \
                self.bits, \
                self.nonce)

   def __repr__(self):
      return __str__(self)

      
class Tx_Input(object):
   def __init__(self):
      super(Tx_Input, self).__init__()
      
   def parse(self, stream):
      self.prevhash = read_hash32(stream)
      self.prevtx_out_idx = read_uint4(stream)
      self.txin_script_len = read_varint(stream)
      # TODO in later modules we will convert scriptSig to its own class
      self.scriptSig = stream.read(self.txin_script_len)
      self.sequence_no = read_uint4(stream)

   def __str__(self):
      return 'PrevHash: %s \nPrev Tx out index: %d \nTxin Script Len: %d \nscriptSig: %s \nSequence: %8x' % \
               (get_hexstring(self.prevhash),
                self.prevtx_out_idx,
                self.txin_script_len,
                get_hexstring(self.scriptSig),
                self.sequence_no)

   def __repr__(self):
      return __str__(self)

      
class Tx_Output(object):
   def __init__(self):
      super(Tx_Output, self).__init__()
      pass
   
   def parse(self, stream):
      self.value = read_uint8(stream)
      self.txout_script_len = read_varint(stream)
      self.scriptPubKey = stream.read(self.txout_script_len)

   def __str__(self):
      return 'Value (satoshis): %d (%f btc)\nTxout Script Len: %d\nscriptPubKey: %s' %\
               (self.value, (1.0*self.value)/100000000.00, 
                self.txout_script_len, 
                get_hexstring(self.scriptPubKey))

   def __repr__(self):
      return __str__(self)


class Transaction(object):
   """Holds one Transaction as part of a block"""
   def __init__(self):
      super(Transaction, self).__init__()
      self.version = None
      self.in_cnt = None
      self.inputs = None
      self.out_cnt = None
      self.outputs = None
      self.lock_time = None

   def parse(self,stream):
      #TODO: error checking
      self.version = read_uint4(stream)
      self.in_cnt = read_varint(stream)
      self.inputs = []
      if self.in_cnt > 0:
         for i in range(0, self.in_cnt):
            input = Tx_Input()
            input.parse(stream)
            self.inputs.append(input)
      self.out_cnt = read_varint(stream)
      self.outputs = []
      if self.out_cnt > 0:
         for i in range(0, self.out_cnt):
            output = Tx_Output()
            output.parse(stream)
            self.outputs.append(output)
      self.lock_time = read_uint4(stream)

   def __str__(self):
      s = 'Inputs count: %d\n---Inputs---\n%s\nOutputs count: %d\n---Outputs---\n%s\nLock_time:%8x' % (self.in_cnt,
               '\n..............\n'.join(str(i) for i in self.inputs),
               self.out_cnt,
               '\n..............\n'.join(str(o) for o in self.outputs),
               self.lock_time)
      return s


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

         self.blockheader = BlockHeader()
         self.blockheader.parse(bf)
         print 'Block header:\t%s' % self.blockheader

         self.transaction_cnt = read_varint(bf)
         print 'Transactions: \t%d' % self.transaction_cnt

         self.transactions = []

         print 'List of transactions'
         for i in range(0, self.transaction_cnt):
            tx = Transaction()
            tx.parse(bf)
            self.transactions.append(tx)
            print '='*50
            print ' TX NUMBER: %d' % (i+1)
            print '='*50
            print tx
            print '\n'




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