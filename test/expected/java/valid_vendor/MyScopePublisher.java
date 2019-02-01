/**
 * Autogenerated by Frugal Compiler (2.27.0)
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *
 * @generated
 */

package include_vendor.java;

import com.workiva.frugal.FContext;
import com.workiva.frugal.exception.TApplicationExceptionType;
import com.workiva.frugal.middleware.InvocationHandler;
import com.workiva.frugal.middleware.ServiceMiddleware;
import com.workiva.frugal.protocol.*;
import com.workiva.frugal.provider.FScopeProvider;
import com.workiva.frugal.transport.FPublisherTransport;
import com.workiva.frugal.transport.FSubscriberTransport;
import com.workiva.frugal.transport.FSubscription;
import com.workiva.frugal.transport.TMemoryOutputBuffer;
import org.apache.thrift.TException;
import org.apache.thrift.TApplicationException;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;
import org.apache.thrift.protocol.*;

import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;
import java.util.EnumMap;
import java.util.Set;
import java.util.HashSet;
import java.util.EnumSet;
import java.util.Collections;
import java.util.BitSet;
import java.nio.ByteBuffer;
import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import javax.annotation.Generated;




@Generated(value = "Autogenerated by Frugal Compiler (2.27.0)", date = "2015-11-24")
public class MyScopePublisher {

	public interface Iface {
		public void open() throws TException;

		public void close() throws TException;

		public void publishnewItem(FContext ctx, some.vendored.pkg.Item req) throws TException;

	}

	public static class Client implements Iface {
		private static final String DELIMITER = ".";

		private final Iface target;
		private final Iface proxy;

		public Client(FScopeProvider provider, ServiceMiddleware... middleware) {
			target = new InternalMyScopePublisher(provider);
			List<ServiceMiddleware> combined = Arrays.asList(middleware);
			combined.addAll(provider.getMiddleware());
			middleware = combined.toArray(new ServiceMiddleware[0]);
			proxy = InvocationHandler.composeMiddleware(target, Iface.class, middleware);
		}

		public void open() throws TException {
			target.open();
		}

		public void close() throws TException {
			target.close();
		}

		public void publishnewItem(FContext ctx, some.vendored.pkg.Item req) throws TException {
			proxy.publishnewItem(ctx, req);
		}

		protected static class InternalMyScopePublisher implements Iface {

			private FScopeProvider provider;
			private FPublisherTransport transport;
			private FProtocolFactory protocolFactory;

			protected InternalMyScopePublisher() {
			}

			public InternalMyScopePublisher(FScopeProvider provider) {
				this.provider = provider;
			}

			public void open() throws TException {
				FScopeProvider.Publisher publisher = provider.buildPublisher();
				transport = publisher.getTransport();
				protocolFactory = publisher.getProtocolFactory();
				transport.open();
			}

			public void close() throws TException {
				transport.close();
			}

			public void publishnewItem(FContext ctx, some.vendored.pkg.Item req) throws TException {
				String op = "newItem";
				String prefix = "";
				String topic = String.format("%sMyScope%s%s", prefix, DELIMITER, op);
				TMemoryOutputBuffer memoryBuffer = new TMemoryOutputBuffer(transport.getPublishSizeLimit());
				FProtocol oprot = protocolFactory.getProtocol(memoryBuffer);
				oprot.writeRequestHeader(ctx);
				oprot.writeMessageBegin(new TMessage(op, TMessageType.CALL, 0));
				req.write(oprot);
				oprot.writeMessageEnd();
				transport.publish(topic, memoryBuffer.getWriteBytes());
			}
		}
	}
}
