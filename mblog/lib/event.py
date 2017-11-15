import Queue
import threading
import time

from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class Event(object):
    def __init__(self, etype, edata):
        self.type = etype
        self.data = edata


class EventEngine(object):
    _instance = None

    def __init__(self):
        self.q = Queue.Queue()
        self.stopped = True
        self.thread = None
        self.event_handles = {}

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = EventEngine()
        return cls._instance

    def put(self, event):
        self.q.put(event)

    def process(self):
        while not self.stopped:
            while not self.q.empty():
                event = self.q.get(block=False)
                if event.type in self.event_handles:
                    for handle in self.event_handles[event.type]:
                        handle(event)
            time.sleep(1)

    def start(self):
        self.stopped = False
        self.thread = threading.Thread(target=self.process)
        self.thread.start()
        LOG.info("Event engine started")

    def stop(self):
        self.stopped = True
        self.thread.join()
        LOG.info("Event engine stopped")

    def register(self, event_type, handle):
        if self.event_handles.get(event_type, None) is None:
            self.event_handles[event_type] = []
        self.event_handles[event_type].append(handle)

