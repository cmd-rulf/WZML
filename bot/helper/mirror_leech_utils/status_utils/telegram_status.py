from ...ext_utils.status_utils import (
    MirrorStatus,
    EngineStatus,
    get_readable_file_size,
    get_readable_time,
)


class TelegramStatus:
    def __init__(self, listener, obj, gid, status, hyper=False):
        self.listener = listener
        self._obj = obj
        self._size = self.listener.size
        self._gid = gid
        self._status = status
        self.engine = EngineStatus().STATUS_TGRAM + (" (HyperDL)" if hyper else "")

    def processed_bytes(self):
        return get_readable_file_size(self._obj.processed_bytes)

    def size(self):
        return get_readable_file_size(self._size)

    def status(self):
        if self._status == "up":
            return MirrorStatus.STATUS_UPLOAD
        return MirrorStatus.STATUS_DOWNLOAD

    def name(self):
        return self.listener.name

    def progress(self):
        try:
            progress_raw = self._obj.processed_bytes / self._size * 100
        except ZeroDivisionError:
            progress_raw = 0
        return f"{round(progress_raw, 2)}%"

    def speed(self):
        return f"{get_readable_file_size(self._obj.speed)}/s"

    def eta(self):
        try:
            seconds = (self._size - self._obj.processed_bytes) / self._obj.speed
            return get_readable_time(seconds)
        except ZeroDivisionError:
            return "-"

    def gid(self):
        return self._gid

    def task(self):
        return self._obj
