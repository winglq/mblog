from mblog.lib.event import EventEngine


def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")
    event_engine = EventEngine.get_instance()
    event_engine.stop()
