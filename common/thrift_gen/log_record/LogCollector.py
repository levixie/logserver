#
# Autogenerated by Thrift Compiler (0.9.2)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:new_style
#

from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class Iface(object):
  """
  Ahh, now onto the cool part, defining a service. Services just need a name
  and can optionally inherit from another service using the extends keyword.
  """
  def log(self, rec):
    """
    A method definition looks like C code. It has a return type, arguments,
    and optionally a list of exceptions that it may throw. Note that argument
    lists and exception lists are specified using the exact same syntax as
    field lists in struct or exception definitions.

    Parameters:
     - rec
    """
    pass


class Client(Iface):
  """
  Ahh, now onto the cool part, defining a service. Services just need a name
  and can optionally inherit from another service using the extends keyword.
  """
  def __init__(self, iprot, oprot=None):
    self._iprot = self._oprot = iprot
    if oprot is not None:
      self._oprot = oprot
    self._seqid = 0

  def log(self, rec):
    """
    A method definition looks like C code. It has a return type, arguments,
    and optionally a list of exceptions that it may throw. Note that argument
    lists and exception lists are specified using the exact same syntax as
    field lists in struct or exception definitions.

    Parameters:
     - rec
    """
    self.send_log(rec)

  def send_log(self, rec):
    self._oprot.writeMessageBegin('log', TMessageType.ONEWAY, self._seqid)
    args = log_args()
    args.rec = rec
    args.write(self._oprot)
    self._oprot.writeMessageEnd()
    self._oprot.trans.flush()

class Processor(Iface, TProcessor):
  def __init__(self, handler):
    self._handler = handler
    self._processMap = {}
    self._processMap["log"] = Processor.process_log

  def process(self, iprot, oprot):
    (name, type, seqid) = iprot.readMessageBegin()
    if name not in self._processMap:
      iprot.skip(TType.STRUCT)
      iprot.readMessageEnd()
      x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
      oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
      x.write(oprot)
      oprot.writeMessageEnd()
      oprot.trans.flush()
      return
    else:
      self._processMap[name](self, seqid, iprot, oprot)
    return True

  def process_log(self, seqid, iprot, oprot):
    args = log_args()
    args.read(iprot)
    iprot.readMessageEnd()
    self._handler.log(args.rec)
    return


# HELPER FUNCTIONS AND STRUCTURES

class log_args(object):
  """
  Attributes:
   - rec
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRUCT, 'rec', (LogRecord, LogRecord.thrift_spec), None, ), # 1
  )

  def __init__(self, rec=None,):
    self.rec = rec

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRUCT:
          self.rec = LogRecord()
          self.rec.read(iprot)
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('log_args')
    if self.rec is not None:
      oprot.writeFieldBegin('rec', TType.STRUCT, 1)
      self.rec.write(oprot)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.rec)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)