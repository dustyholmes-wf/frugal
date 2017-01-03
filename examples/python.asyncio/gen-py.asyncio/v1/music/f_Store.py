#
# Autogenerated by Frugal Compiler (2.0.0-RC5)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#



import asyncio
from datetime import timedelta
import inspect

from frugal.aio.processor import FBaseProcessor
from frugal.aio.processor import FProcessorFunction
from frugal.exceptions import FApplicationException
from frugal.exceptions import FMessageSizeException
from frugal.exceptions import FRateLimitException
from frugal.exceptions import FTimeoutException
from frugal.middleware import Method
from frugal.transport import TMemoryOutputBuffer
from thrift.Thrift import TApplicationException
from thrift.Thrift import TMessageType
from .ttypes import *


class Iface(object):
    """
    Services are the API for client and server interaction.
    Users can buy an album or enter a giveaway for a free album.
    """

    async def buyAlbum(self, ctx, ASIN, acct):
        """
        Args:
            ctx: FContext
            ASIN: string
            acct: string
        """
        pass

    async def enterAlbumGiveaway(self, ctx, email, name):
        """
        Args:
            ctx: FContext
            email: string
            name: string
        """
        pass


class Client(Iface):

    def __init__(self, provider, middleware=None):
        """
        Create a new Client with an FServiceProvider containing a transport
        and protocol factory.

        Args:
            provider: FServiceProvider
            middleware: ServiceMiddleware or list of ServiceMiddleware
        """
        middleware = middleware or []
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]
        self._transport = provider.get_transport()
        self._protocol_factory = provider.get_protocol_factory()
        middleware += provider.get_middleware()
        self._methods = {
            'buyAlbum': Method(self._buyAlbum, middleware),
            'enterAlbumGiveaway': Method(self._enterAlbumGiveaway, middleware),
        }

    async def buyAlbum(self, ctx, ASIN, acct):
        """
        Args:
            ctx: FContext
            ASIN: string
            acct: string
        """
        return await self._methods['buyAlbum']([ctx, ASIN, acct])

    async def _buyAlbum(self, ctx, ASIN, acct):
        timeout = ctx.timeout / 1000.0
        future = asyncio.Future()
        timed_future = asyncio.wait_for(future, timeout)
        await self._transport.register(ctx, self._recv_buyAlbum(ctx, future))
        try:
            await self._send_buyAlbum(ctx, ASIN, acct)
            result = await timed_future
        except asyncio.TimeoutError:
            raise FTimeoutException('buyAlbum timed out after {} milliseconds'.format(ctx.timeout))
        finally:
            await self._transport.unregister(ctx)
        return result

    async def _send_buyAlbum(self, ctx, ASIN, acct):
        buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('buyAlbum', TMessageType.CALL, 0)
        args = buyAlbum_args()
        args.ASIN = ASIN
        args.acct = acct
        args.write(oprot)
        oprot.writeMessageEnd()
        await self._transport.send(buffer.getvalue())

    def _recv_buyAlbum(self, ctx, future):
        def buyAlbum_callback(transport):
            iprot = self._protocol_factory.get_protocol(transport)
            iprot.read_response_headers(ctx)
            _, mtype, _ = iprot.readMessageBegin()
            if mtype == TMessageType.EXCEPTION:
                x = TApplicationException()
                x.read(iprot)
                iprot.readMessageEnd()
                if x.type == FApplicationException.RESPONSE_TOO_LARGE:
                    future.set_exception(FMessageSizeException.response(x.message))
                    return
                if x.type == FApplicationException.RATE_LIMIT_EXCEEDED:
                    future.set_exception(FRateLimitException(x.message))
                    return
                future.set_exception(x)
                return
            result = buyAlbum_result()
            result.read(iprot)
            iprot.readMessageEnd()
            if result.error is not None:
                future.set_exception(result.error)
                return
            if result.success is not None:
                future.set_result(result.success)
                return
            x = TApplicationException(TApplicationException.MISSING_RESULT, "buyAlbum failed: unknown result")
            future.set_exception(x)
            raise x
        return buyAlbum_callback

    async def enterAlbumGiveaway(self, ctx, email, name):
        """
        Args:
            ctx: FContext
            email: string
            name: string
        """
        return await self._methods['enterAlbumGiveaway']([ctx, email, name])

    async def _enterAlbumGiveaway(self, ctx, email, name):
        timeout = ctx.timeout / 1000.0
        future = asyncio.Future()
        timed_future = asyncio.wait_for(future, timeout)
        await self._transport.register(ctx, self._recv_enterAlbumGiveaway(ctx, future))
        try:
            await self._send_enterAlbumGiveaway(ctx, email, name)
            result = await timed_future
        except asyncio.TimeoutError:
            raise FTimeoutException('enterAlbumGiveaway timed out after {} milliseconds'.format(ctx.timeout))
        finally:
            await self._transport.unregister(ctx)
        return result

    async def _send_enterAlbumGiveaway(self, ctx, email, name):
        buffer = TMemoryOutputBuffer(self._transport.get_request_size_limit())
        oprot = self._protocol_factory.get_protocol(buffer)
        oprot.write_request_headers(ctx)
        oprot.writeMessageBegin('enterAlbumGiveaway', TMessageType.CALL, 0)
        args = enterAlbumGiveaway_args()
        args.email = email
        args.name = name
        args.write(oprot)
        oprot.writeMessageEnd()
        await self._transport.send(buffer.getvalue())

    def _recv_enterAlbumGiveaway(self, ctx, future):
        def enterAlbumGiveaway_callback(transport):
            iprot = self._protocol_factory.get_protocol(transport)
            iprot.read_response_headers(ctx)
            _, mtype, _ = iprot.readMessageBegin()
            if mtype == TMessageType.EXCEPTION:
                x = TApplicationException()
                x.read(iprot)
                iprot.readMessageEnd()
                if x.type == FApplicationException.RESPONSE_TOO_LARGE:
                    future.set_exception(FMessageSizeException.response(x.message))
                    return
                if x.type == FApplicationException.RATE_LIMIT_EXCEEDED:
                    future.set_exception(FRateLimitException(x.message))
                    return
                future.set_exception(x)
                return
            result = enterAlbumGiveaway_result()
            result.read(iprot)
            iprot.readMessageEnd()
            if result.success is not None:
                future.set_result(result.success)
                return
            x = TApplicationException(TApplicationException.MISSING_RESULT, "enterAlbumGiveaway failed: unknown result")
            future.set_exception(x)
            raise x
        return enterAlbumGiveaway_callback


class Processor(FBaseProcessor):

    def __init__(self, handler, middleware=None):
        """
        Create a new Processor.

        Args:
            handler: Iface
        """
        if middleware and not isinstance(middleware, list):
            middleware = [middleware]

        super(Processor, self).__init__()
        self.add_to_processor_map('buyAlbum', _buyAlbum(Method(handler.buyAlbum, middleware), self.get_write_lock()))
        self.add_to_processor_map('enterAlbumGiveaway', _enterAlbumGiveaway(Method(handler.enterAlbumGiveaway, middleware), self.get_write_lock()))


class _buyAlbum(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_buyAlbum, self).__init__(handler, lock)

    async def process(self, ctx, iprot, oprot):
        args = buyAlbum_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = buyAlbum_result()
        try:
            ret = self._handler([ctx, args.ASIN, args.acct])
            if inspect.iscoroutine(ret):
                ret = await ret
            result.success = ret
        except FRateLimitException as ex:
            async with self._lock:
                _write_application_exception(ctx, oprot, FApplicationException.RATE_LIMIT_EXCEEDED, "buyAlbum", ex.message)
                return
        except PurchasingError as error:
            result.error = error
        except Exception as e:
            async with self._lock:
                e = _write_application_exception(ctx, oprot, TApplicationException.UNKNOWN, "buyAlbum", e.args[0])
            raise e from None
        async with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('buyAlbum', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except FMessageSizeException as e:
                raise _write_application_exception(ctx, oprot, FApplicationException.RESPONSE_TOO_LARGE, "buyAlbum", e.args[0])


class _enterAlbumGiveaway(FProcessorFunction):

    def __init__(self, handler, lock):
        super(_enterAlbumGiveaway, self).__init__(handler, lock)

    async def process(self, ctx, iprot, oprot):
        args = enterAlbumGiveaway_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = enterAlbumGiveaway_result()
        try:
            ret = self._handler([ctx, args.email, args.name])
            if inspect.iscoroutine(ret):
                ret = await ret
            result.success = ret
        except FRateLimitException as ex:
            async with self._lock:
                _write_application_exception(ctx, oprot, FApplicationException.RATE_LIMIT_EXCEEDED, "enterAlbumGiveaway", ex.message)
                return
        except Exception as e:
            async with self._lock:
                e = _write_application_exception(ctx, oprot, TApplicationException.UNKNOWN, "enterAlbumGiveaway", e.args[0])
            raise e from None
        async with self._lock:
            try:
                oprot.write_response_headers(ctx)
                oprot.writeMessageBegin('enterAlbumGiveaway', TMessageType.REPLY, 0)
                result.write(oprot)
                oprot.writeMessageEnd()
                oprot.get_transport().flush()
            except FMessageSizeException as e:
                raise _write_application_exception(ctx, oprot, FApplicationException.RESPONSE_TOO_LARGE, "enterAlbumGiveaway", e.args[0])


def _write_application_exception(ctx, oprot, typ, method, message):
    x = TApplicationException(type=typ, message=message)
    oprot.write_response_headers(ctx)
    oprot.writeMessageBegin(method, TMessageType.EXCEPTION, 0)
    x.write(oprot)
    oprot.writeMessageEnd()
    oprot.get_transport().flush()
    return x

class buyAlbum_args(object):
    """
    Attributes:
     - ASIN
     - acct
    """
    def __init__(self, ASIN=None, acct=None):
        self.ASIN = ASIN
        self.acct = acct

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.ASIN = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.acct = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('buyAlbum_args')
        if self.ASIN is not None:
            oprot.writeFieldBegin('ASIN', TType.STRING, 1)
            oprot.writeString(self.ASIN)
            oprot.writeFieldEnd()
        if self.acct is not None:
            oprot.writeFieldBegin('acct', TType.STRING, 2)
            oprot.writeString(self.acct)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(self.ASIN)
        value = (value * 31) ^ hash(self.acct)
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class buyAlbum_result(object):
    """
    Attributes:
     - success
     - error
    """
    def __init__(self, success=None, error=None):
        self.success = success
        self.error = error

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = Album()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.error = PurchasingError()
                    self.error.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('buyAlbum_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.error is not None:
            oprot.writeFieldBegin('error', TType.STRUCT, 1)
            self.error.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(self.success)
        value = (value * 31) ^ hash(self.error)
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class enterAlbumGiveaway_args(object):
    """
    Attributes:
     - email
     - name
    """
    def __init__(self, email=None, name=None):
        self.email = email
        self.name = name

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.email = iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.name = iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('enterAlbumGiveaway_args')
        if self.email is not None:
            oprot.writeFieldBegin('email', TType.STRING, 1)
            oprot.writeString(self.email)
            oprot.writeFieldEnd()
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 2)
            oprot.writeString(self.name)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(self.email)
        value = (value * 31) ^ hash(self.name)
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class enterAlbumGiveaway_result(object):
    """
    Attributes:
     - success
    """
    def __init__(self, success=None):
        self.success = success

    def read(self, iprot):
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.BOOL:
                    self.success = iprot.readBool()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        oprot.writeStructBegin('enterAlbumGiveaway_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.BOOL, 0)
            oprot.writeBool(self.success)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __hash__(self):
        value = 17
        value = (value * 31) ^ hash(self.success)
        return value

    def __repr__(self):
        L = ['%s=%r' % (key, value)
            for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

