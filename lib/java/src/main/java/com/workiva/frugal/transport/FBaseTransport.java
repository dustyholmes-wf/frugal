package com.workiva.frugal.transport;

import com.workiva.frugal.exception.FMessageSizeException;
import com.workiva.frugal.protocol.FRegistry;
import org.apache.thrift.TException;
import org.apache.thrift.transport.TTransportException;
import org.slf4j.Logger;

import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;


/**
 * FBaseTransport implements the buffered write (and ready, until 2.0) data
 * shared by all FTransports.
 */
public abstract class FBaseTransport extends FTransport {

    private final Logger logger;
    private FRegistry registry;
    private final int requestBufferSize;
    private final ByteBuffer requestBuffer;

    // TODO: Remove with 2.0
    protected final BlockingQueue<byte[]> frameBuffer;
    protected static final byte[] FRAME_BUFFER_CLOSED = new byte[0];
    private byte[] currentFrame = new byte[0];
    private int currentFramePos;

    FBaseTransport(int requestBufferSize, Logger logger) {
        this.requestBufferSize = requestBufferSize;
        this.requestBuffer = ByteBuffer.allocate(requestBufferSize);
        this.frameBuffer = null;
        this.logger = logger;
    }

    // TODO: Remove with 2.0
    FBaseTransport(int requestBufferSize, int frameBufferSize, Logger logger) {
        this.requestBufferSize = requestBufferSize;
        this.requestBuffer = ByteBuffer.allocate(requestBufferSize);
        this.frameBuffer = new ArrayBlockingQueue<>(frameBufferSize);
        this.logger = logger;
    }

    /**
     * Set the FRegistry on the FTransport.
     *
     * @param registry FRegistry to set on the FTransport.
     */
    @Override
    public void setRegistry(FRegistry registry) {
        this.registry = registry;
    }

    /**
     * Close the frame buffer and signal close
     * @param cause
     */
    void close(final Exception cause) {
        try {
            frameBuffer.put(FRAME_BUFFER_CLOSED);
        } catch (InterruptedException e) {
            logger.warn("could not close frame buffer: " + e.getMessage());
        }
        registry.close();
        signalClose(cause);
    }

    /**
     * Reads up to len bytes into the buffer.
     *
     * @throws TTransportException
     *
     * TODO: Remove all read logic with 2.0
     */
    public int read(byte[] bytes, int off, int len) throws TTransportException {
        if (currentFramePos == currentFrame.length) {
            try {
                currentFrame = frameBuffer.take();
                currentFramePos = 0;
            } catch (InterruptedException e) {
                throw new TTransportException(TTransportException.END_OF_FILE, e.getMessage());
            }
        }
        if (currentFrame == FRAME_BUFFER_CLOSED) {
            throw new TTransportException(TTransportException.END_OF_FILE);
        }
        int size = Math.min(len, currentFrame.length);
        System.arraycopy(currentFrame, currentFramePos, bytes, off, size);
        currentFramePos += size;
        return size;
    }

    /**
     * Writes the bytes to a buffer. Throws FMessageSizeException if the buffer exceeds
     * {@code requestBufferSize}.
     *
     * @throws TTransportException
     */
    public void write(byte[] bytes, int off, int len) throws TTransportException {
        if (requestBuffer.remaining() < len) {
            int size = len + requestBufferSize - requestBuffer.remaining();
            requestBuffer.clear();
            throw new FMessageSizeException(
                    String.format("Message exceeds %d bytes, was %d bytes",
                            requestBufferSize, size));
        }
        requestBuffer.put(bytes, off, len);
    }

    protected boolean isRequestData() {
        return requestBuffer.position() > 0;
    }

    /**
     * Get the request bytes and reset the buffer.
     *
     * @return request bytes
     * TODO: Remove this with 2.0
     */
    protected byte[] getRequestBytes() {
        byte[] data = new byte[requestBuffer.position()];
        requestBuffer.flip();
        requestBuffer.get(data);
        requestBuffer.clear();
        return data;
    }

    /**
     * Get the framed request bytes and reset the buffer.
     *
     * @return request bytes
     */
    protected byte[] getFramedRequestBytes() {
        int numBytes = requestBuffer.position();
        byte[] data = new byte[numBytes + 4];
        requestBuffer.flip();
        requestBuffer.get(data, 4, numBytes);
        requestBuffer.clear();
        encodeFrameSize(numBytes, data);
        return data;
    }

    /**
     * Execute a frugal frame (NOTE: this frame must include the frame size).
     *
     * @param frame frugal frame
     * @throws TException
     */
    void execute(byte[] frame) throws TException {
        registry.execute(Arrays.copyOfRange(frame, 4, frame.length));
    }

    private static void encodeFrameSize(final int frameSize, final byte[] buf) {
        buf[0] = (byte)(0xff & (frameSize >> 24));
        buf[1] = (byte)(0xff & (frameSize >> 16));
        buf[2] = (byte)(0xff & (frameSize >> 8));
        buf[3] = (byte)(0xff & (frameSize));
    }
}
