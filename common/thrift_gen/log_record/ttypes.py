#
# Autogenerated by Thrift Compiler (0.9.2)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py:new_style
#

from thrift.Thrift import TType, TMessageType, TException, TApplicationException

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None


class Operation(object):
  """
  You can define enums, which are just 32 bit integers. Values are optional
  and start at 1 if not supplied, C style again.
  """
  LOG = 1

  _VALUES_TO_NAMES = {
    1: "LOG",
  }

  _NAMES_TO_VALUES = {
    "LOG": 1,
  }

class CounterType(object):
  TOTAL = 1
  ERR = 2

  _VALUES_TO_NAMES = {
    1: "TOTAL",
    2: "ERR",
  }

  _NAMES_TO_VALUES = {
    "TOTAL": 1,
    "ERR": 2,
  }


class LogRecord(object):
  """
  Structs are the basic complex data structures. They are comprised of fields
  which each have an integer identifier, a type, a symbolic name, and an
  optional default value.

  Fields can be declared "optional", which ensures they will not be included
  in the serialized output if they aren't set.  Note that this requires some
  manual management in some languages.

  Attributes:
   - msg
   - log_name
   - name
   - level
   - pathname
   - lineno
   - func
   - thread
   - threadname
   - processname
   - process
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'msg', None, None, ), # 1
    (2, TType.STRING, 'log_name', None, None, ), # 2
    (3, TType.STRING, 'name', None, None, ), # 3
    (4, TType.I16, 'level', None, None, ), # 4
    (5, TType.STRING, 'pathname', None, None, ), # 5
    (6, TType.I32, 'lineno', None, None, ), # 6
    (7, TType.STRING, 'func', None, None, ), # 7
    (8, TType.I64, 'thread', None, None, ), # 8
    (9, TType.STRING, 'threadname', None, None, ), # 9
    (10, TType.STRING, 'processname', None, None, ), # 10
    (11, TType.I64, 'process', None, None, ), # 11
  )

  def __init__(self, msg=None, log_name=None, name=None, level=None, pathname=None, lineno=None, func=None, thread=None, threadname=None, processname=None, process=None,):
    self.msg = msg
    self.log_name = log_name
    self.name = name
    self.level = level
    self.pathname = pathname
    self.lineno = lineno
    self.func = func
    self.thread = thread
    self.threadname = threadname
    self.processname = processname
    self.process = process

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
        if ftype == TType.STRING:
          self.msg = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.log_name = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.STRING:
          self.name = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.I16:
          self.level = iprot.readI16();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.STRING:
          self.pathname = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.I32:
          self.lineno = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.STRING:
          self.func = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.I64:
          self.thread = iprot.readI64();
        else:
          iprot.skip(ftype)
      elif fid == 9:
        if ftype == TType.STRING:
          self.threadname = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 10:
        if ftype == TType.STRING:
          self.processname = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 11:
        if ftype == TType.I64:
          self.process = iprot.readI64();
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
    oprot.writeStructBegin('LogRecord')
    if self.msg is not None:
      oprot.writeFieldBegin('msg', TType.STRING, 1)
      oprot.writeString(self.msg)
      oprot.writeFieldEnd()
    if self.log_name is not None:
      oprot.writeFieldBegin('log_name', TType.STRING, 2)
      oprot.writeString(self.log_name)
      oprot.writeFieldEnd()
    if self.name is not None:
      oprot.writeFieldBegin('name', TType.STRING, 3)
      oprot.writeString(self.name)
      oprot.writeFieldEnd()
    if self.level is not None:
      oprot.writeFieldBegin('level', TType.I16, 4)
      oprot.writeI16(self.level)
      oprot.writeFieldEnd()
    if self.pathname is not None:
      oprot.writeFieldBegin('pathname', TType.STRING, 5)
      oprot.writeString(self.pathname)
      oprot.writeFieldEnd()
    if self.lineno is not None:
      oprot.writeFieldBegin('lineno', TType.I32, 6)
      oprot.writeI32(self.lineno)
      oprot.writeFieldEnd()
    if self.func is not None:
      oprot.writeFieldBegin('func', TType.STRING, 7)
      oprot.writeString(self.func)
      oprot.writeFieldEnd()
    if self.thread is not None:
      oprot.writeFieldBegin('thread', TType.I64, 8)
      oprot.writeI64(self.thread)
      oprot.writeFieldEnd()
    if self.threadname is not None:
      oprot.writeFieldBegin('threadname', TType.STRING, 9)
      oprot.writeString(self.threadname)
      oprot.writeFieldEnd()
    if self.processname is not None:
      oprot.writeFieldBegin('processname', TType.STRING, 10)
      oprot.writeString(self.processname)
      oprot.writeFieldEnd()
    if self.process is not None:
      oprot.writeFieldBegin('process', TType.I64, 11)
      oprot.writeI64(self.process)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.msg)
    value = (value * 31) ^ hash(self.log_name)
    value = (value * 31) ^ hash(self.name)
    value = (value * 31) ^ hash(self.level)
    value = (value * 31) ^ hash(self.pathname)
    value = (value * 31) ^ hash(self.lineno)
    value = (value * 31) ^ hash(self.func)
    value = (value * 31) ^ hash(self.thread)
    value = (value * 31) ^ hash(self.threadname)
    value = (value * 31) ^ hash(self.processname)
    value = (value * 31) ^ hash(self.process)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class PerfRecord(object):
  """
  Attributes:
   - id
   - type
   - times
   - period
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'id', None, None, ), # 1
    (2, TType.I32, 'type', None, None, ), # 2
    (3, TType.I32, 'times', None, None, ), # 3
    (4, TType.LIST, 'period', (TType.DOUBLE,None), None, ), # 4
  )

  def __init__(self, id=None, type=None, times=None, period=None,):
    self.id = id
    self.type = type
    self.times = times
    self.period = period

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
        if ftype == TType.STRING:
          self.id = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.type = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.I32:
          self.times = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.LIST:
          self.period = []
          (_etype3, _size0) = iprot.readListBegin()
          for _i4 in xrange(_size0):
            _elem5 = iprot.readDouble();
            self.period.append(_elem5)
          iprot.readListEnd()
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
    oprot.writeStructBegin('PerfRecord')
    if self.id is not None:
      oprot.writeFieldBegin('id', TType.STRING, 1)
      oprot.writeString(self.id)
      oprot.writeFieldEnd()
    if self.type is not None:
      oprot.writeFieldBegin('type', TType.I32, 2)
      oprot.writeI32(self.type)
      oprot.writeFieldEnd()
    if self.times is not None:
      oprot.writeFieldBegin('times', TType.I32, 3)
      oprot.writeI32(self.times)
      oprot.writeFieldEnd()
    if self.period is not None:
      oprot.writeFieldBegin('period', TType.LIST, 4)
      oprot.writeListBegin(TType.DOUBLE, len(self.period))
      for iter6 in self.period:
        oprot.writeDouble(iter6)
      oprot.writeListEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.id)
    value = (value * 31) ^ hash(self.type)
    value = (value * 31) ^ hash(self.times)
    value = (value * 31) ^ hash(self.period)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class InvalidOperation(TException):
  """
  Structs can also be exceptions, if they are nasty.

  Attributes:
   - whatOp
   - why
  """

  thrift_spec = (
    None, # 0
    (1, TType.I32, 'whatOp', None, None, ), # 1
    (2, TType.STRING, 'why', None, None, ), # 2
  )

  def __init__(self, whatOp=None, why=None,):
    self.whatOp = whatOp
    self.why = why

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
        if ftype == TType.I32:
          self.whatOp = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.why = iprot.readString();
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
    oprot.writeStructBegin('InvalidOperation')
    if self.whatOp is not None:
      oprot.writeFieldBegin('whatOp', TType.I32, 1)
      oprot.writeI32(self.whatOp)
      oprot.writeFieldEnd()
    if self.why is not None:
      oprot.writeFieldBegin('why', TType.STRING, 2)
      oprot.writeString(self.why)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()

  def validate(self):
    return


  def __str__(self):
    return repr(self)

  def __hash__(self):
    value = 17
    value = (value * 31) ^ hash(self.whatOp)
    value = (value * 31) ^ hash(self.why)
    return value

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
