package com.jventura.pybridge;

/*
import org.msgpack.core.MessagePack;
import org.msgpack.core.MessageUnpacker;
import org.msgpack.core.MessageBufferPacker;
*/

import org.msgpack.core.MessageBufferPacker;
import org.msgpack.core.MessagePack;
import org.msgpack.core.MessageUnpacker;

/**
 * Modified version of PyBridge to use msgpack instead of json
 * (msgpack is 3x-10x faster than json in python)
 * @see https://gist.github.com/cactus/4073643
 */
public class PyBridge {

    /**
     * Initializes the Python interpreter.
     *
     * @param datapath the location of the extracted python files
     * @return error code
     */
    public static native int start(String datapath);

    /**
     * Stops the Python interpreter.
     *
     * @return error code
     */
    public static native int stop();

    /**
     * Sends a byte payload to the Python interpreter.
     *
     * @param payload the payload byte array
     * @return a byte array with the result
     */
   // public static native String invoke(String payload);

    /**
     * Sends a MessageBufferPacker payload to the Python interpreter.
     *
     * @param payload MessageBufferPacker payload
     * @return MessageUnpacker response
     */
//    public static MessageUnpacker invoke(MessageBufferPacker packer) {
//        byte[] result = invoke(packer.toByteArray());
//        return MessagePack.newDefaultUnpacker(result);
//    }

    // Load library
    static {
        System.loadLibrary("pybridge");
        System.loadLibrary("jnius");
    }
}
