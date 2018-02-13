import unittest
from copy import deepcopy
from DataStructures import Heap


# note: excluding sorting methods
class HeapTestCase(unittest.TestCase):
    def setUp(self):
        self.minEmptyHeap = Heap(max_heap=False)
        self.maxEmptyHeap = Heap(max_heap=True)

        self.data = [737, 201, 869, 922, 365, 643, 218, 362, 86, 858, 877, 456, 393, 113, 111, 866, 491, 853, 708, 132,
                     722, 759, 691, 560, 349, 890, 889, 158, 924, 496, 518, 906, 591, 887, 900, 59, 515, 765, 645, 948,
                     182, 291, 556, 332, 566, 215, 431, 436, 154, 753, 392, 652, 149, 929, 326, 233, 856, 195, 312, 242,
                     216, 675, 895, 251, 10, 185, 99, 982, 68, 474, 462, 152, 348, 954, 343, 261, 432, 457, 228, 234,
                     881, 278, 597, 44, 977, 398, 879, 192, 553, 588, 787, 403, 783, 377, 590, 464, 613, 133, 811, 841]

        self.minheap = Heap(max_heap=False)
        self.maxheap = Heap(max_heap=True)

        for num in deepcopy(self.data):
            self.minheap.insert(num)
            self.maxheap.insert(num)

        self.minIterHeap = Heap(from_list=deepcopy(self.data), max_heap=False)
        self.maxIterHeap = Heap(from_list=deepcopy(self.data), max_heap=True)

        heaps = [self.minheap, self.maxheap, self.minIterHeap,  self.maxIterHeap, self.minEmptyHeap, self.maxEmptyHeap]
        names = ["min heap", "max heap", "min iter heap", "max iter heap", "min empty heap", "max empty heap"]
        self.nonempty = [(heaps[i], names[i]) for i in range(4)]
        self.empty = [(heaps[i], names[i]) for i in range(4, 6)]
        self.allheaps = [(heaps[i], names[i]) for i in range(6)]

    @staticmethod
    def is_heap(heap):
        for i in range(1, len(heap._h)):
            for child in [heap._left, heap._right]:
                # if child is None, we can skip it
                if child(i):
                    # continue if heap property is satisfied
                    # return False if it isn't
                    if not heap._comp(heap._h[i], heap._h[child(i)]):
                        return False

        return True

    # verify that we actually constructed a heap
    # iterate over parent/children and make sure heap property is satisfied
    def test_is_heap(self):
        for heap, name in self.allheaps:
            with self.subTest(heap=heap, name=name):
                # check that it's a heap
                self.assertTrue(self.is_heap(heap), "{0} unexpectedly not a heap".format(name))

        # verify that if we change the heap data, it becomes no longer a heap
        for heap, name in self.nonempty:
            with self.subTest(heap=heap, name=name):
                heap._h = deepcopy(self.data)
                heap._h.insert(0, None)
                self.assertFalse(self.is_heap(heap), "{0} unexpectedly a heap".format(name))

    @unittest.skip("Not written")
    def test_add(self):
        pass

    def test_bool(self):
        for heap, name in self.nonempty:
            with self.subTest(heap=heap, name=name):
                self.assertTrue(heap, "{0} unexpectedly False".format(name))

        for heap, name in self.empty:
            with self.subTest(heap=heap, name=name):
                self.assertFalse(heap, "{0} unexpectedly True".format(name))

    def test_len(self):
        for heap in [self.minheap, self.maxheap, self.minIterHeap, self.maxIterHeap, self.minEmptyHeap,
                     self.maxEmptyHeap]:

            with self.subTest(heap=heap):
                self.assertEqual(len(heap), len(heap._h[1:]), "heap length incorrect")

    def test_str(self):
        for heap in self.allheaps:
            with self.subTest(heap=heap):
                self.assertEqual(str(heap), str(heap._h[1:]), "heap string incorrect")

    @unittest.skip("Not written")
    def test_parent(self):
        for heap, name in self.allheaps:
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

