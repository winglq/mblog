def stream_iter(stream, chunk_size):
    while True:
        ctx = stream.read(chunk_size)
        if not ctx:
            break
        yield ctx
