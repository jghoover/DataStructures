from math import log2, floor, inf
from operator import lt, gt


class Heap(object):
    """
    Binary Heap container class, providing min and max heaps.
    Class methods are implemented for optimal runtimes.
    Also provides heapsort and introsort algorithms.
    """

    @staticmethod
    def heapsort(iterable, reversed=False):
        """
        Heapsort comparative non-stable sorting algorithm.
        Runtime O(n log n).

        Parameters
        ----------
        iterable : iterable
            The collection of objects to sort.
        reversed : bool, optional
            If True, sort the list in nonincreasing order.  Otherwise, sort in nondecreasing.

        Returns
        -------
        A copy of the list `iterable`, sorted in nondecreasing order (if `reversed` is False)
        or in nonincreasing order (if `reversed` is True).
        """

        # todo: rewrite this to take key for sorting
        if reversed:
            comparison = gt
        else:
            comparison = lt
        h = Heap(from_list=iterable, comparison=comparison)
        temp = []

        while not h.is_empty():
            temp.append(h._h[1])
            h._swap(1, h._last)
            h._last -= 1
            h._bubbledown(1)

        return temp

    @staticmethod
    def introsort(iterable):
        """
        Introsort hybrid comparative non-stable sorting algorithm.
        Runtime O(n log n).

        Parameters
        ----------
        iterable : iterable
            The list of objects to be sorted.

        Returns
        -------
        list
            A copy of `iterable`, sorted in nondecreasing order.

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

        def _introsort(iterable, maxdepth):
            # base case: a list of length <= 1 is always sorted
            if len(iterable) <= 1:
                return iterable
            # insertion sort for lists of length <= 16
            elif len(iterable) <= 16:
                for k in range(1, len(iterable)):
                    while 0 < k and iterable[k] < iterable[k - 1]:
                        iterable[k], iterable[k - 1] = iterable[k - 1], iterable[k]
                        k -= 1
                return iterable
            # if we exceed the max recursion depth, switch to heapsort
            elif maxdepth <= 0:
                return Heap.heapsort(iterable)
            # quicksort in the regular case
            else:
                pivot = iterable[0]
                less = [x for x in iterable[1:] if x < pivot]
                more = [x for x in iterable[1:] if x >= pivot]

                return _introsort(less, maxdepth - 1) \
                    + [pivot] + _introsort(more, maxdepth - 1)

        return _introsort(iterable, 2 * floor(log2(len(iterable))))

    @staticmethod
    def select_k(iterable, k, comparison=None):
        # todo: figure out the bound at which doing this is more efficient than doing a sort: k << n
        # idea: heapify the first k items of the list, using the opposite ordered as desired
        # (i.e. max heap if largest is False) then loop over the rest of the list, doing a replace_root if the next
        # item is < (or > if largest is True) for the rest of the list.  Then return heap.data
        # analysis:
        # O(k) : build a heap of the first k elements
        # + O(n-k) : loop through the rest of the elements
        # * O(log k) : if every one of the rest of the elements needs to be put in the heap
        # = O(k + (n-k)log k) = O(k + n log k - k log k) = O(n log k)
        """
        Select the `k` smallest/largest elements from dataset `iterable`.
        Runtime: O(n log k)

        Parameters
        ----------
        iterable : iter
            Dataset to select elements from.
        k : int
            Number of elements to select from the dataset.
        comparison : function, optional
            Specify how to compare the elements of `iterable`.  Defaults to `None`, representing normal less/greater
            than comparison.


        Returns
        -------
        list
            The `k` smallest (if `largest` is `False`) or largest (if `largest` is `True`) elements from `iterable`.
        """

        if k < 0 or k > len(iterable):
            raise ValueError("k must be in the range [0, len(iterable)={0}]".format(len(iterable)))

        if not comparison:
            comparison = lt

        # logic to check if it's more efficient to just use a sorting algorithm---k ~ n
        # todo: investigate what this bound on k needs to be
        heap = Heap(iterable[:k], comparison=comparison)
        for element in iterable[k:]:
            if comparison(element, heap.peek()):
                heap.extract_insert(element)

        return heap.data

    def __init__(self, from_list=None, comparison=None):
        # todo: investigate using loops instead of recursion for bubbleup/bubbledown to prevent stack badness
        """
        Heap constructor.  Create a min or max heap,
        which may be either empty or initialized to contain
        a specified list.

        Parameters
        ----------
        from_list : iterable, optional
            Initialize the heap with these values.  Defaults to `None`.

        comparison : function, optional
            Specify how to compare items in the heap.  Default of `None` indicates operator.lt

        Other Parameters
        ----------------
        _comp : {operator.lt, operator.gt}
            Function used to compare heap elements
        _h : list
            The data stored in the heap
        _last : int
            The index of the last element in the heap
        _max_heap : bool
            Represents if the heap is a max or min heap.
        """

        if comparison is None:
            comparison = lt

        self._comp = comparison

        # 0-index is never used, so just put none there
        self._h = []
        self._last = -1

        if from_list:
            self._h += from_list
            self._last = len(from_list) - 1
            self._heapify()

    def __iter__(self):
        return (x for x in self._h)

    def __add__(self, other):
        """
        Merge with another heap or iterable.

        Parameters
        ----------
        other : iterable
            The sequence of items to be added to the heap.  Items must be comparable.
        """
        self.merge(other)

    # return True iff there is at least one item on the heap
    def __bool__(self):
        return bool(self._h)

    def __len__(self):
        return len(self._h)

    # indexing starts at 1, so only return slice starting at 1
    def __str__(self):
        return str(self._h)

    @property
    def data(self):
        return self._h

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
        return (i - 1) // 2

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
        lc = 2 * i + 1
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
        rc = 2 * i + 2
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
        Recursively repair a damaged heap after `insert()`.
        Runtime O(log n)

        Args
        ----
        i : int
            The index to start bubbling up from.
        """
        parent = self._parent(i)

        if i == 0 or (self._comp(self._h[parent], self._h[i])):
            return i

        self._swap(i, parent)
        return self._bubbleup(parent)

    def _bubbledown(self, i):
        """
        Recursively repair a heap after `extract()`, or called repeatedly from `heapify()`.
        Runtime O(log n)

        Args
        ----
        i : int
            Index to start bubbling down from.
        """
        lc = toSwap = self._left(i)
        rc = self._right(i)

        # no left child, so we're done.
        if lc is None:
            return

        # right child exists and...
        if rc is not None:
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
        Note that all nodes at index > parent(last) have no children,
        and so running bubbledown on them would be wasted work.  Thus,
        we can start bubbling down at parent(last).

        Runtime O(n)
        """
        for i in range(self._parent(self._last), -1, -1):
            self._bubbledown(i)

    def insert(self, item):
        """
        Add an element to the heap.
        Runtime O(log n)

        Parameters
        ----------
        item : comparable
            The element to be added to the heap.
        """
        self._last += 1
        self._h.append(item)
        self._bubbleup(self._last)

    def extract(self):
        """
        Get the next item from the heap, removing it in the process.
        Runtime O(log n)

        Returns
        -------
        object
            The root of the heap.  That is, the item with the
            most priority.

        Raises
        ------
        IndexError
            If the heap is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot extract from empty heap")

        temp = self._h[0]
        # pull up last data to new root
        self._swap(0, self._last)
        self._last -= 1
        # remove old last
        self._h.pop()
        self._bubbledown(0)
        return temp

    def extract_insert(self, item):
        """
        Remove and return the root, and insert a new item.
        Faster than explicitly calling an extract followed by an insert.

        Parameters
        ----------
        item : object
            Element to be added to the heap.

        Returns
        -------
        object
            The element at the root of the heap, before inserting `item`.

        """
        if self.is_empty():
            raise IndexError("Cannot extract from empty heap")

        toReturn = self._h[0]
        self._h[0] = item
        self._bubbledown(0)
        return toReturn

    def insert_extract(self, item):
        """
        Insert a new item and extract, and remove and return the root.
        Faster than explicitly calling an insert followed by an extract.

        Parameters
        ----------
        item : object
            Element to be added to the heap.

        Returns
        -------
        object
            The element at the root of the heap, after inserting `item`.
        """
        # if the heap is empty, or the item will end up as the root, then there's no point in modifying the heap
        if not self.is_empty() and self._comp(self._h[0], item):
            self._h[0], item = item, self._h[0]
            self._bubbledown(0)

        return item

    def peek(self):
        """
        Get the next item from the heap, without removing it.
        Runtime O(1)

        Returns
        -------
        object
            The root of the heap.  That is, the item with the
            most priority.

        Raises
        ------
        IndexError
            If the heap is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot peek from empty heap")

        return self._h[0]

    def merge(self, other):
        """
        Add a list of elements to the heap.
        Runtime O(n)

        Parameters
        ----------
        other : iterable
            The collection of elements to be added to the heap.
        """
        self._h += other
        self._last += len(other)
        self._heapify()

    def is_empty(self):
        """
        Check if there are items in the heap.

        Returns
        -------
        bool
            True if there are items in the heap, false otherwise.
        """
        return self._last < 0

    def make_empty(self):
        self._h = []
        self._last = -1


class PriorityQueue(Heap):
    """
    Priority Queue class, implemented using a binary heap, providing min and max priority queues.  Elements inserted
    into the Priority Queue must be immutable. Note that while duplicate elements are valid, no guarantees are made
    as to which instance will be modified with `remove()` and `update_key()` functions, or their syntactic sugar.
    This behavior can be mitigated by inserting elements as tuples containing the desired item and a sequential
    variable.

    Attributes
    ----------
    """

    def __init__(self, from_list=None, max_heap=False):
        # todo: move Other Parameters to class docstring
        # todo: rewrite PriorityQueue in a more OOP manner, or make it its own class
        # todo: rewrite PQ with changes made to heap
        """
        Initialize a new Priority Queue.

        Parameters
        ----------
        from_list : iterable, optional
            Initialize the list containing these arguments.  Defaults to None, representing an empty heap.
        max_heap : bool, optional
            If true, initialize heap as a max heap, otherwise initialize a min heap. Defaults to False.

        Other Parameters
        ----------------
        _h : list
            Heap data
        _index : dict
            Dictionary to store the index position of items in the heap.
            Keys are the item object of a (priority, item) tuple.  Values are the
            index position in `_h`.
        _last : int
            The index position of the final element in the heap.  Used for reparing heaps
            and for checking if the heap is empty.
        _max_heap : bool
            If True, the heap is a max heap.  Otherwise, the heap is a min heap.
        _comp : function
            The comparison function used to check the heap property.  Written as a lambda
            function that compares only the priority object of a (priority, item) tuple.
        _prioritized : {-inf, inf}
            The maximum value any priority can take.  `-inf` for min heaps, and `inf` for max
            heaps.  Used in `remove()`.
        """
        self._h = []
        self._index = {}
        self._last = 0
        self._max_heap = max_heap

        if self._max_heap:
            self._comp = lambda x, y: x[0] > y[0]
            self._prioritized = inf
        else:
            self._comp = lambda x, y: x[0] < y[0]
            self._prioritized = -inf

        # todo: rewrite this so it actually works
        if from_list:
            self._h += from_list
            self._last = len(from_list)
            self._heapify()

    def __contains__(self, item):
        """
        Check if the Priority Queue contains `item`.

        Parameters
        ----------
        item : object
           The element to check for containment.

        Returns
        -------
        bool
            True if `item` is in the Priority Queue, False otherwise.
        """
        return item in self._index

    def __getitem__(self, key):
        """
        Obtain the priority of the item `key`.  If duplicate instances of `key` are present, no guarantees are made as
        to which one's priority will be returned.

        Parameters
        ----------
        key : object
           The item whose priority we are obtaining.

        Returns
        -------
        object
            The priority of heap element `key`.

        See Also
        --------
        get_priority : Method to obtain the priority of an item.
        """
        return self.get_priority(key)

    def __setitem__(self, key, value):
        """
        If `key` is not already present in the Priority Queue, add it with priority `value`.  If `key` is already
        present, update its priority to `value`.  If duplicate items need to be inserted into the Priority Queue,
        you must use `insert()`.

        Parameters
        ----------
        key
            The item to be inserted.
        value
            The priority of the item being inserted.

        See Also
        --------
        insert : Method to insert an item with priority.
        update_key : Method to change the priority of an arbitrary item.
        """
        if key in self:
            self.update_priority(key, value)
        else:
            self.insert(key, value)

    def __delitem__(self, key):
        """
        Remove an instance of the item `key` from the Priority Queue. If duplicate instances of `key` are present,
        no guarantees are made as to which instance will be removed.

        Parameters
        ----------
        key
            The item to be removed.

        See Also
        --------
        remove : Method to remove a single instance of `item`.
        """
        self.remove(key)

    def _swap(self, i, j):
        """
        Exchange the items at indices `i` and `j` and update the index dict.

        Parameters
        ----------
        i, j : int
            The index positions of the elements we are swapping.
        """
        self._h[i], self._h[j] = self._h[j], self._h[i]

        # update index dict
        self._index[self._h[i][1]] = i
        self._index[self._h[j][1]] = j

    def insert(self, item, key):
        """
        Add element `item` to the heap with priority `key`.  The element `item` must be immutable.
        Runtime O(log n)

        Parameters
        ----------
        item : object
            The object to be added to the heap.
        key : object
            The priority of `item`.

        See Also
        --------
        __setitem__ : Syntactic sugar for adding an item to the Priority Queue or updating its priority.
        """
        self._last += 1
        self._h.append((key, item))
        self._index[item] = self._bubbleup(self._last)

    # also called extract min/max
    def extract(self):
        """
        Dequeue.  Remove and return the item with the highest priority.
        Runtime O(log n)

        Returns
        -------
        object
            The item at the root of the heap.

        Raises
        ------
        IndexError
            If the Priority Queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot extract from empty Priority Queue")

        item = self._h[1][1]

        # todo: make sure this works
        if self._last > 1:
            # remove extracted item from dict
            del self._index[item]
            # pull up last data to root
            self._h[1] = self._h[self._last]
            self._last -= 1
            # update index of new root
            self._index[self._h[1][1]] = 1
            # remove old last data
            self._h.pop()
            # repair heap
            self._bubbledown(1)
        else:
            # the priority queue is now empty
            del self._index[item]
            self._last -= 1
            self._h.pop()

        return item

    def peek(self):
        """
        Return, but don't remove, the item at the root of the heap.
        Runtime O(1)

        Returns
        -------
        object
            The item at the root of the heap.

        Raises
        ------
        IndexError
            If the Priority Queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot peek from empty Priority Queue")

        # todo: make sure this doesn't return the priority, just the item
        return self._h[1]

    def get_priority(self, item):
        """
        Get the priority of `item` in the heap.  If duplicate instances of `item` are present, no guarantees are made
        as to which instance's priority will be returned.

        Parameters
        ----------
        item : object
            The element whose priority we are getting.

        Returns
        -------
        comparable
            The priority of `item`.

        Raises
        ------
        KeyError
            If `item` is not in the Priority Queue.

        See Also
        --------
        __getitem___ : Syntactic sugar for obtaining the priority of an item.
        """
        if item not in self:
            raise KeyError("Item {0} not present in Priority Queue".format(repr(item)))

        index = self._index[item]
        return self._h[index][0]

    def update_priority(self, item, priority):
        """
        Change the priority of an arbitrary element Priority Queue element `item`.  If duplicate instances of `item`
        are present, no guarantees are made as to which instance will be updated.
        Runtime O(log n)

        Parameters
        ----------
        item
            The element of the heap whose priority we are updating
        priority
            The new priority of `item`

        Raises
        ------
        KeyError
            If `item` is not in the Priority Queue.

        See Also
        --------
        __setitem__ : Syntactic sugar to update the priority of `item`.
        """
        if item not in self:
            raise KeyError("Item {0} not present in Priority Queue".format(repr(item)))

        index = self._index[item]
        oldKey = self._h[index][0]
        self._h[index] = (priority, item)

        # is there a better way to write this mess of conditionals?
        if priority < oldKey:
            if self._max_heap:
                self._bubbledown(index)
            else:
                self._bubbleup(index)
        else:
            if self._max_heap:
                self._bubbleup(index)
            else:
                self._bubbledown(index)

    def remove(self, item):
        # todo: rewrite this.
        # Instead of using prioritized, just swap with last, pop _h, and compare the old last with its new parent.
        # If comp(old_last, parent) is true (i.e. old_last < parent), then bubbleup, else bubbledown.
        """
        Remove a single instance of `item` from the Priority Queue.  If duplicate instances of `item` are present, no
        guarantees are made as to which instance will be removed.
        Runtime O(log n)

        Parameters
        ----------
        item : object
           The element to be removed.

        Raises
        ------
        KeyError
            If `item` is not in the Priority Queue.

        See Also
        --------
        __delitem__ : Syntactic sugar to remove an instance of `item`.
        """

        if item not in self:
            raise KeyError("Item {0} not present in Priority Queue".format(repr(item)))

        self.update_priority(item, self._prioritized)
        self.extract()
