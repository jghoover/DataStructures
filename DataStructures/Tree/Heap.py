from operator import lt, gt
from math import log2, floor, inf


class Heap(object):
    """
    Binary Heap container class, providing min and max heaps.
    Class methods are implemented for optimal runtimes.
    Also provides heapsort and introsort algorithms.

    Todo
    ----
    Add implementations of built-in type conversion.
    I.e. seq, bool, etc.
    Modify __init__ so that it takes a boolean max_heap to determine
    if the heap is min or max.
    """

    @staticmethod
    def heapsort(m):
        """
        Heapsort comparative non-stable sorting algorithm.
        Runtime :math:O(n \log n).

        Parameters
        ----------
        m (list): The list of objects to sort.

        Returns
        -------
        A copy of the list `m`, sorted in nondecreasing order.
        """

        h = Heap(from_list=m)
        temp = []

        while not h.is_empty():
            temp.append(h._h[1])
            h._swap(1, h._last)
            h._last -= 1
            h._bubbledown(1)

        return temp

    @staticmethod
    def introsort(m):
        """
        Introsort hybrid comparative non-stable sorting algorithm.
        Runtime :math:O(n \log n).

        Parameters
        ----------
        m (list): The list of objects to be sorted.

        Returns
        -------
        list
            A copy of `m`, sorted in nondecreasing order.

        Notes
        -----
        Introsort is a hybrid sorting algorithm, consisting of
        quicksort, insertion sort, and heapsort.  The algorithm
        uses insertion sort on lists of length <= 16.  For other
        lists, quicksort is used until a maximum recursion depth
        of is reached, at which point heapsort is used.  This
        avoids the O(n^2) pathological runtime of quicksort.
        Further speed improvements result from the use of insertion
        sort on small lists.

        The maximum recursion depth is defined as:
        ``2*math.floor(math.log2(len(m)))``

        See [1]_ for an in-depth analysis of introsort.

        References
        ----------
        .. [1]: Musser, David R. (1997). "Introspective Sorting
            and Selection Algorithms". Software: Practice and
            Experience. Wiley. 27 (8): 983-993.
        """

        def _introsort(m, maxdepth):
            # base case: a list of length <= 1 is always sorted
            if len(m) <= 1:
                return m
            # insertion sort for lists of length <= 16
            elif len(m) <= 16:
                for k in range(1, len(m)):
                    while 0 < k and m[k] < m[k - 1]:
                        m[k], m[k - 1] = m[k - 1], m[k]
                        k -= 1
                return m
            # if we exceed the max recursion depth, switch to heapsort
            elif maxdepth <= 0:
                return Heap.heapsort(m)
            # quicksort in the regular case
            else:
                pivot = m[0]
                less = [x for x in m[1:] if x < pivot]
                more = [x for x in m[1:] if x >= pivot]

                return _introsort(less, maxdepth - 1) \
                    + [pivot] + _introsort(more, maxdepth - 1)

        return _introsort(m, 2 * floor(log2(len(m))))

    def __init__(self, from_list=None, max_heap=False):
        """
        Heap constructor.  Create a min or max heap,
        which may be either empty or initialized to contain
        a specified list.

        Parameters
        ----------
        from_list : list, optional
            Initialize the heap with these values.  Defaults to `None`.

        max_heap : Boolean, optional
            Specify the heap to be a maximum heap.
            Defaults to False, signifying a minimum heap.

        Other Parameters
        ----------------
        _comp : {operator.lt, operator.gt}
            Function used to compare heap elements
        _h : list
            The data stored in the heap
        _last : int
            The index of the last element in the heap
        _max_heap : Boolean
            Represents if the heap is a max or min heap.
        """

        self._max_heap = max_heap

        if self._max_heap:
            self._comp = gt
        else:
            self._comp = lt

        # 0-index is never used, so just put none there
        self._h = [None, ]
        self._last = 0

        if from_list:
            self._h += from_list
            self._last = len(from_list)
            self._heapify()

    def __add__(self, other):
        self.merge(other)

    # return True iff there is at least one item on the heap
    def __bool__(self):
        return not self.is_empty()

    def __len__(self):
        return self._last

    # indexing starts at 1, so only return slice starting at 1
    def __str__(self):
        return str(self._h[1:])


    def _parent(self, i):
        """
        Get the index of the parent of a node sitting at index `i`.

        Parameters
        ----------
        i : int
            The index of the node whose parent we want.

        Returns
        -------
        int
            The index of the parent node of `i`.
        """
        return i // 2

    def _left(self, i):
        """
        Get the index of the left child of a node sitting at index `i`.

        Parameters
        ----------
        i : int
            The index of the node whose left child we want.

        Returns
        -------
        int
            The index of the left child of the specified node,
            or `None` if there is no child.
        """
        lc = 2 * i
        return lc if lc <= self._last else None

    def _right(self, i):
        """
        Get the index of the right child of a node sitting at index `i`.

        Parameters
        ----------
        i : int
            The index of the node whose right child we want.

        Returns
        -------
        int
            The index of the right child of the specified node,
            or `None` if there is no child.

        """
        rc = 2 * i + 1
        return rc if rc <= self._last else None

    def _swap(self, i, j):
        """
        Exchange the values of the objects at indices `i` and `j`

        Args
        ----
        i : int
            First index of the pair to exchange.
        j : int
            Second index of the pair to exchange.
        """
        self._h[i], self._h[j] = self._h[j], self._h[i]

    def _bubbleup(self, i):
        """
        Recursively repair a damaged heap after an `insert()`.
        Runtime :math:O(\log n)

        Args
        ----
        i : int
            The index to start bubbling up from.
        """
        if i == 1 or \
                (self._comp(self._h[self._parent(i)], self._h[i])):
            return i

        self._swap(i, self._parent(i))
        return self._bubbleup(self._parent(i))

    def _bubbledown(self, i):
        """
        Recursively repair a heap after an `extract()`.
        Runtime :math:O(\log n)

        Args
        ----
        i : int
            Index to start bubbling down from.
        """
        lc = toSwap = self._left(i)
        rc = self._right(i)

        # no left child, so we're done.
        if not lc:
            return

        # right child exists and...
        if rc:
            # h[rc] < h[lc] (min heap)
            # h[rc] > h[lc] (max heap)
            if self._comp(self._h[rc], self._h[lc]):
                toSwap = rc

        # heap property is satisfied
        if self._comp(self._h[i], self._h[toSwap]):
            return

        # otherwise, swap and bubbledown again
        self._swap(i, toSwap)
        self._bubbledown(toSwap)

    def _heapify(self):
        """
        Construct a heap from a list of elements.
        Runtime :math:O(n)
        """
        for i in range(self._parent(self._last), 0, -1):
            self._bubbledown(i)

    # complexity: O(log n)
    def insert(self, item):
        """
        Add an element to the heap.
        Runtime :math:O(\log n)

        Parameters
        ----------
        item : object
            The element to be added to the heap.
            Must be comparable.
        """
        self._last += 1
        self._h.append(item)
        self._bubbleup(self._last)

    def extract(self):
        """
        Get the next item from the heap, removing it in the process.

        Returns
        -------
        object
            The root of the heap.  That is, the item with the
            most priority, or `None` if the heap is empty.
        """
        if self.is_empty():
            return None

        temp = self._h[1]
        # pull up last data to new root
        self._swap(1, self._last)
        self._last -= 1
        # remove old last
        self._h.pop()
        self._bubbledown(1)
        return temp

    def peek(self):
        """
        Get the next item from the heap, without removing it.

        Returns
        -------
        object
            The root of the heap.  That is, the item with the
            most priority, or `None` if the heap is empty.
        """
        return None if self.is_empty() else self._h[1]

    def merge(self, other):
        """
        Add a list of elements to the heap.
        Runtime :math:O(n)

        Parameters
        ----------
        other : list
            The list of elements to be added to the heap.
        """
        self._h += other
        self._last += len(other)
        self._heapify()

    def is_empty(self):
        return self._last <= 0

    def is_full(self):
        return False

    def get_kind(self):
        return "Maximum" if self._max_heap else "Minimum"


class PriorityQueue(Heap):
    """
    Priority Queue class, implemented using a binary heap.
    Provides min and max priority queues.
    """

    def __init__(self, from_list=None, max_heap=False):
        self._h = [None, ]
        self._index = {}
        self._last = 0
        self._max_heap = max_heap

        if self._max_heap:
            self._comp = lambda x, y: x[0] > y[0]
            self._prioritized = inf
        else:
            self._comp = lambda x, y: x[0] < y[0]
            self._prioritized = -inf

        if from_list:
            self._h += from_list
            self._last = len(from_list)
            self._heapify()

    def __contains__(self, item):
        try:
            self._index[item]
        except KeyError:
            return False

        return True

    def __getitem__(self, key):
        return self.get_priority(key)

    # pq.insert(item, priority) == pq[item] = priority
    def __setitem__(self, key, value):
        self.insert(key, value)

    def __delitem__(self, key):
        self.remove(key)

    def _swap(self, i, j):
        self._h[i], self._h[j] = self._h[j], self._h[i]

        # update index dict
        self._index[self._h[i][1]] = i
        self._index[self._h[j][1]] = j

    # complexity: O(log n)
    def insert(self, item, key):
        self._last += 1
        self._h.append((key, item))
        self._index[item] = self._bubbleup(self._last)

    # also called extract min/max
    def extract(self):
        if self.is_empty():
            return None

        item = self._h[1][1]
        # pull up last data to new root
        self._swap(1, self._last)
        # remove from dictionary
        del self._index[item]
        self._last -= 1
        # remove old last
        self._h.pop()
        self._bubbledown(1)
        return item

    def peek(self):
        return None if self.is_empty() else self._h[1][1]

    def get_priority(self, item):
        index = self._index[item]
        return self._h[index][0]

    # takes O(log n) time
    # could use a fibonacci heap to lower this to O(1) amoritized,
    # but fibonacci heaps have bad memory performance
    # modify this to take into account min or max heap
    def update_key(self, item, key):
        index = self._index[item]
        oldKey = self._h[index][0]
        self._h[index] = (key, item)

        # is there a better way to write this mess of conditionals?
        if key < oldKey:
            if self._max_heap:
                self._bubbledown(index)
            else:
                self._bubbleup(index)
        else:
            if self._max_heap:
                self._bubbleup(index)
            else:
                self._bubbledown(index)

    # i.e. cancel a job
    # O(log n)
    def remove(self, item):
        self.update_key(item, self._prioritized)
        self.extract()
