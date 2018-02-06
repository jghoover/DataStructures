class Queue(object):

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)

    def __bool__(self):
        return bool(self._data)

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if len(self) > 0:
            return self._data.pop(0)
        else:
            raise IndexError("Cannot dequeue from empty Queue")

    def peek(self):
        if len(self) > 0:
            return self._data[0]
        else:
            raise IndexError("Cannot peek from empty Queue")

    def make_empty(self):
        self._data = []


class DoubleEndedQueue(object):

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)

    def __bool__(self):
        return bool(self._data)

    def append(self, item):
        self._data.append(item)

    def append_left(self, item):
        self._data.insert(0, item)

    def pop(self):
        if len(self) > 0:
            return self._data.pop()
        else:
            raise IndexError("Cannot pop from empty DEQueue")

    def pop_left(self):
        if len(self) > 0:
            return self._data.pop(0)
        else:
            raise IndexError("Cannot pop_left from empty DEQueue")

    def peek(self):
        if len(self) > 0:
            return self._data[-1]
        else:
            raise IndexError("Cannot peek from empty DEQueue")

    def peek_left(self):
        if len(self) > 0:
            return self._data[0]
        else:
            raise IndexError("Cannot peek_left from empty DEQueue")

    def make_empty(self):
        self._data = []
