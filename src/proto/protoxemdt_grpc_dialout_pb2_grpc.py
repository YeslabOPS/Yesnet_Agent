# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from ..proto import protoxemdt_grpc_dialout_pb2 as protoxemdt__grpc__dialout__pb2


class gRPCMdtDialoutStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.MdtDialout = channel.stream_stream(
                '/mdt_dialout.gRPCMdtDialout/MdtDialout',
                request_serializer=protoxemdt__grpc__dialout__pb2.MdtDialoutArgs.SerializeToString,
                response_deserializer=protoxemdt__grpc__dialout__pb2.MdtDialoutArgs.FromString,
                )


class gRPCMdtDialoutServicer(object):
    """Missing associated documentation comment in .proto file."""

    def MdtDialout(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_gRPCMdtDialoutServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'MdtDialout': grpc.stream_stream_rpc_method_handler(
                    servicer.MdtDialout,
                    request_deserializer=protoxemdt__grpc__dialout__pb2.MdtDialoutArgs.FromString,
                    response_serializer=protoxemdt__grpc__dialout__pb2.MdtDialoutArgs.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mdt_dialout.gRPCMdtDialout', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class gRPCMdtDialout(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def MdtDialout(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/mdt_dialout.gRPCMdtDialout/MdtDialout',
            protoxemdt__grpc__dialout__pb2.MdtDialoutArgs.SerializeToString,
            protoxemdt__grpc__dialout__pb2.MdtDialoutArgs.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
