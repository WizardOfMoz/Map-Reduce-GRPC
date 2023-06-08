# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import consistency_pb2 as consistency__pb2


class Master_MapStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.getInputData = channel.unary_unary(
        '/consistency.Master_Map/getInputData',
        request_serializer=consistency__pb2.MapDataRequest.SerializeToString,
        response_deserializer=consistency__pb2.InputData.FromString,
        )
    self.Register = channel.unary_unary(
        '/consistency.Master_Map/Register',
        request_serializer=consistency__pb2.Map.SerializeToString,
        response_deserializer=consistency__pb2.MapRegResponse.FromString,
        )
    self.getR = channel.unary_unary(
        '/consistency.Master_Map/getR',
        request_serializer=consistency__pb2.Void.SerializeToString,
        response_deserializer=consistency__pb2.RValue.FromString,
        )


class Master_MapServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def getInputData(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Register(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getR(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_Master_MapServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'getInputData': grpc.unary_unary_rpc_method_handler(
          servicer.getInputData,
          request_deserializer=consistency__pb2.MapDataRequest.FromString,
          response_serializer=consistency__pb2.InputData.SerializeToString,
      ),
      'Register': grpc.unary_unary_rpc_method_handler(
          servicer.Register,
          request_deserializer=consistency__pb2.Map.FromString,
          response_serializer=consistency__pb2.MapRegResponse.SerializeToString,
      ),
      'getR': grpc.unary_unary_rpc_method_handler(
          servicer.getR,
          request_deserializer=consistency__pb2.Void.FromString,
          response_serializer=consistency__pb2.RValue.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'consistency.Master_Map', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class Map_ReduceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.getIntermediateData = channel.unary_unary(
        '/consistency.Map_Reduce/getIntermediateData',
        request_serializer=consistency__pb2.ReduceDataRequest.SerializeToString,
        response_deserializer=consistency__pb2.IntermediateData.FromString,
        )


class Map_ReduceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def getIntermediateData(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_Map_ReduceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'getIntermediateData': grpc.unary_unary_rpc_method_handler(
          servicer.getIntermediateData,
          request_deserializer=consistency__pb2.ReduceDataRequest.FromString,
          response_serializer=consistency__pb2.IntermediateData.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'consistency.Map_Reduce', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class Master_ReduceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Register = channel.unary_unary(
        '/consistency.Master_Reduce/Register',
        request_serializer=consistency__pb2.Reduce.SerializeToString,
        response_deserializer=consistency__pb2.ReduceRegResponse.FromString,
        )
    self.getRegisteredMaps = channel.unary_stream(
        '/consistency.Master_Reduce/getRegisteredMaps',
        request_serializer=consistency__pb2.Void.SerializeToString,
        response_deserializer=consistency__pb2.Map.FromString,
        )


class Master_ReduceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def Register(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def getRegisteredMaps(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_Master_ReduceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Register': grpc.unary_unary_rpc_method_handler(
          servicer.Register,
          request_deserializer=consistency__pb2.Reduce.FromString,
          response_serializer=consistency__pb2.ReduceRegResponse.SerializeToString,
      ),
      'getRegisteredMaps': grpc.unary_stream_rpc_method_handler(
          servicer.getRegisteredMaps,
          request_deserializer=consistency__pb2.Void.FromString,
          response_serializer=consistency__pb2.Map.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'consistency.Master_Reduce', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class Reduce_MasterStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.getFinalData = channel.unary_unary(
        '/consistency.Reduce_Master/getFinalData',
        request_serializer=consistency__pb2.Void.SerializeToString,
        response_deserializer=consistency__pb2.FinalData.FromString,
        )


class Reduce_MasterServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def getFinalData(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_Reduce_MasterServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'getFinalData': grpc.unary_unary_rpc_method_handler(
          servicer.getFinalData,
          request_deserializer=consistency__pb2.Void.FromString,
          response_serializer=consistency__pb2.FinalData.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'consistency.Reduce_Master', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))