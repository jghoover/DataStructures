import operator
import unittest
from copy import deepcopy

from DataStructures import Heap


# note: excluding sorting methods
class HeapTestCase(unittest.TestCase):
    def setUp(self):
        self.minEmptyHeap = Heap(comparison=operator.lt)
        self.maxEmptyHeap = Heap(comparison=operator.gt)

        self.data = [737, 201, 869, 922, 365, 643, 218, 362, 86, 858, 877, 456, 393, 113, 111, 866, 491, 853, 708, 132,
                     722, 759, 691, 560, 349, 890, 889, 158, 924, 496, 518, 906, 591, 887, 900, 59, 515, 765, 645, 948,
                     182, 291, 556, 332, 566, 215, 431, 436, 154, 753, 392, 652, 149, 929, 326, 233, 856, 195, 312, 242,
                     216, 675, 895, 251, 10, 185, 99, 982, 68, 474, 462, 152, 348, 954, 343, 261, 432, 457, 228, 234,
                     881, 278, 597, 44, 977, 398, 879, 192, 553, 588, 787, 403, 783, 377, 590, 464, 613, 133, 811, 841]

        self.merge_data = [746, 74, 422, 75, 771, 360, 642, 157, 201, 859, 158, 456, 582, 880, 953, 595, 721, 295, 985,
                           132, 361, 1, 373, 38, 366, 939, 673, 519, 322, 994, 569, 71, 292, 650, 573, 720, 40, 561, 14,
                           389, 78, 452, 196, 729, 889, 807, 294, 47, 548, 234, 621, 12, 303, 997, 296, 742, 765, 283,
                           146, 563, 228, 534, 462, 346, 108, 310, 995, 795, 381, 98, 383, 495, 616, 198, 85, 568, 895,
                           785, 26, 37, 936, 301, 273, 293, 289, 988, 439, 407, 349, 334, 833, 129, 232, 520, 162, 911,
                           320, 968, 677, 870]

        self.minheap = Heap(comparison=operator.lt)
        self.maxheap = Heap(comparison=operator.gt)

        for num in deepcopy(self.data):
            self.minheap.insert(num)
            self.maxheap.insert(num)

        # use deepcopy so that we use different instances of data
        self.minIterHeap = Heap(from_list=deepcopy(self.data), comparison=operator.lt)
        self.maxIterHeap = Heap(from_list=deepcopy(self.data), comparison=operator.gt)

        heaps = [self.minheap, self.maxheap, self.minIterHeap,  self.maxIterHeap, self.minEmptyHeap, self.maxEmptyHeap]
        names = ["min heap", "max heap", "min iter heap", "max iter heap", "min empty heap", "max empty heap"]
        self.nonempty = [(heaps[i], names[i]) for i in range(4)]
        self.empty = [(heaps[i], names[i]) for i in range(4, 6)]
        self.allheaps = [(heaps[i], names[i]) for i in range(6)]

    @staticmethod
    def is_heap(heap):
        # todo: rewrite so that it just takes a list, not a heap
        for i in range(0, len(heap)):
            for child in [heap._left, heap._right]:
                # if child is None, we can skip it
                if child(i):
                    # continue if heap property is satisfied
                    # return False if it isn't
                    if not heap._comp(heap.data[i], heap.data[child(i)]):
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
                self.assertFalse(self.is_heap(heap), "{0} unexpectedly a heap".format(name))

    def test_bool(self):
        for heap, name in self.nonempty:
            with self.subTest(heap=heap, name=name):
                self.assertTrue(heap, "{0} unexpectedly False".format(name))

                heap.make_empty()
                self.assertFalse(heap, "{0} unexpectedly True".format(name))

        for heap, name in self.empty:
            with self.subTest(heap=heap, name=name):
                self.assertFalse(heap, "{0} unexpectedly True".format(name))

    def test_insert(self):
        numbers = [2, 500, 1000, 1345, -50]
        for heap, name in self.allheaps:
            with self.subTest(heap=heap, name=name):
                for num in numbers:
                    with self.subTest(num=num):
                        heap.insert(num)
                        self.assertIn(num, heap.data, "{0} unexpectedly not in {1} after insert".format(num, name))
                        self.assertTrue(self.is_heap(heap), "{0} unexpectedly not a heap after insert".format(name))

    def test_extract(self):
        for heap, name in self.nonempty:
            with self.subTest(heap=heap, name=name):
                # extract everything from the heap!
                root = deepcopy(heap.data[0])  # todo: rewrite this to choose min/max element
                self.assertEqual(root, heap.extract())

                heap.make_empty()
                self.assertFalse(heap)
                with self.assertRaises(IndexError):
                    heap.extract()

    def test_merge(self):
        for heap, name in self.allheaps:
            with self.subTest(heap=heap, name=name):
                # all this deepcopying is probably bad on run time/memory...
                premerge = deepcopy(heap.data) + deepcopy(self.merge_data)

                heap.merge(deepcopy(self.merge_data))
                self.assertTrue(self.is_heap(heap), "{0} unexpectedly not a heap".format(name))
                self.assertCountEqual(premerge, heap.data, "unexpected items missing/present in {0}".format(name))

    @unittest.skip("insert_extract test not written")
    def test_insert_extract(self):
        pass

    @unittest.skip("extract_insert test not written")
    def test_extract_insert(self):
        pass

    def test_is_empty(self):
        for heap, name in self.nonempty:
            self.assertFalse(heap.is_empty(), "{0} unexpectedly is_empty".format(name))

            heap.make_empty()
            self.assertTrue(heap.is_empty(), "{0} unexpectedly not is_empty after make_empty")

        for heap, name in self.empty:
            self.assertTrue(heap.is_empty(), "{0} unexpectedly not is_empty".format(name))



