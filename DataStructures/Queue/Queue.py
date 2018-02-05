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
            raise IndexError("No Queue item to dequeue")

    def peek(self):
        if len(self) > 0:
            return self._data[0]
        else:
            raise IndexError("No queue item to peek")

    def make_empty(self):
        self._data = []


class DEQueue(object):

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
            raise IndexError("No DEQueue item to pop")

    def pop_left(self):
        if len(self) > 0:
            return self._data.pop(0)
        else:
            raise IndexError("No DEQueue item to pop_left")

    def peek(self):
        if len(self) > 0:
            return self._data[-1]
        else:
            raise IndexError("No DEQueue item to peek")

    def peek_left(self):
        if len(self) > 0:
            return self._data[0]
        else:
            raise IndexError("No DEQueue item to peek_left")

    def make_empty(self):
        self._data = []
