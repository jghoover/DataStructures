import unittest
from DataStructures import Heap


# note: excluding sorting methods
class HeapTestCase(unittest.TestCase):
    def setUp(self):
        # todo: check min/max: empty heap, heap init. by inserting a bunch, heap init. from an iterable
        self.minEmptyHeap = Heap(max_heap=False)
        self.maxEmptyHeap = Heap(max_heap=True)

        self.data = [737, 201, 869, 922, 365, 643, 218, 362, 86, 858, 877, 456, 393, 113, 111, 866, 491, 853, 708, 132,
                     722, 759, 691, 560, 349, 890, 889, 158, 924, 496, 518, 906, 591, 887, 900, 59, 515, 765, 645, 948,
                     182, 291, 556, 332, 566, 215, 431, 436, 154, 753, 392, 652, 149, 929, 326, 233, 856, 195, 312, 242,
                     216, 675, 895, 251, 10, 185, 99, 982, 68, 474, 462, 152, 348, 954, 343, 261, 432, 457, 228, 234,
                     881, 278, 597, 44, 977, 398, 879, 192, 553, 588, 787, 403, 783, 377, 590, 464, 613, 133, 811, 841]

        self.minheap = Heap(max_heap=False)
        self.maxheap = Heap(max_heap=True)

        for num in self.data:
            self.minheap.insert(num)
            self.maxheap.insert(num)

        self.minIterHeap = Heap(from_list=self.data, max_heap=False)
        self.maxIterHeap = Heap(from_list=self.data, max_heap=True)

    # verify that we actually constructed a heap
    # iterate over parent/children and make sure heap property is satisfied
    def test_is_heap(self):
        # todo: figure out how to pass a heap to this function and verify it, i.e. for after merge
        for heap in [self.minheap, self.maxheap, self.minIterHeap, self.maxIterHeap]:
            with self.subTest(heap=heap):
                for i in range(1, len(heap._h)):
                    with self.subTest(i=i):
                        # if child is None, then we don't care about it
                        if heap._left(i):
                            parent = heap._h[i]
                            child = heap._h[heap._left(i)]
                            self.assertTrue(heap._comp(parent, child),
                                            "{0}, {1} unexpectedly violates heap condition for {2}".format(parent,
                                                                                                           child, heap))
                        if heap._right(i):
                            parent = heap._h[i]
                            child = heap._h[heap._right(i)]
                            self.assertTrue(heap._comp(parent, child),
                                            "{0}, {1} unexpectedly violates heap condition for {2}".format(parent,
                                                                                                           child, heap))

    @unittest.skip("Not written")
    def test_add(self):
        pass

    def test_bool(self):
        self.assertTrue(self.minheap, "minheap unexpectedly false")
        self.assertTrue(self.maxheap, "maxheap unexpectedly false")
        self.assertTrue(self.minIterHeap, "minIterHeap unexpectedly false")
        self.assertTrue(self.maxIterHeap, "maxIterHeap unexpectedly false")

        self.assertFalse(self.minEmptyHeap, "minEmptyHeap unexpectedly true")
        self.assertFalse(self.maxEmptyHeap, "maxEmptyHeap unexpectedly true")

    def test_len(self):
        for heap in [self.minheap, self.maxheap, self.minIterHeap, self.maxIterHeap, self.minEmptyHeap,
                     self.maxEmptyHeap]:

            with self.subTest(heap=heap):
                self.assertEqual(len(heap), len(heap._h[1:]), "heap length incorrect")

    def test_str(self):
        for heap in [self.minheap, self.maxheap, self.minIterHeap, self.maxIterHeap, self.minEmptyHeap,
                     self.maxEmptyHeap]:
            with self.subTest(heap=heap):
                self.assertEqual(str(heap), str(heap._h[1:]), "heap string incorrect")

    @unittest.skip("Not written")
    def test_parent(self):
        pass

    @unittest.skip("Not written")
    def test_left(self):
        pass

    @unittest.skip("Not written")
    def test_right(self):
        pass

    @unittest.skip("Not written")
    def test_swap(self):
        pass

    @unittest.skip("Not written")
    def test_bubbleup(self):
        pass

    @unittest.skip("Not written")
    def test_bubbledown(self):
        pass

    @unittest.skip("Not written")
    def test_heapify(self):
        pass

    @unittest.skip("Not written")
    def test_insert(self):
        pass

    @unittest.skip("Not written")
    def test_extract(self):
        pass

    @unittest.skip("Not written")
    def test_peek(self):
        pass

    @unittest.skip("Not written")
    def test_merge(self):
        pass

    @unittest.skip("Not written")
    def test_is_empty(self):
        pass

    @unittest.skip("Not written")
    def test_get_kind(self):
        pass

