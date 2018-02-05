class Stack(object):

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return str(self._data)

    def __bool__(self):
        return bool(self._data)

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if len(self) > 0:
            return self._data.pop()
        else:
            raise IndexError("No Stack item to pop")

    def peek(self):
        if len(self) > 0:
            return self._data[-1]
        else:
            raise IndexError("No Stack item to peek")

    def make_empty(self):
        self._data = []
