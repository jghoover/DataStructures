import unittest
from DataStructures import DoubleEndedQueue


class DEQueueTestCase(unittest.TestCase):
    def setUp(self):
        self.deq = DoubleEndedQueue()
        self.emptydeq = DoubleEndedQueue()

        for letter in "abcdefghijklmnopqrstuvwxyz":
            self.deq.append(letter)

    def test_len(self):
        self.assertEqual(len(self.deq), 26, "DEQ length not 26")
        self.assertEqual(len(self.emptydeq), 0, "Empty deq length not 0")

        # check append, append_left
        self.deq.append("aa")
        self.assertEqual(len(self.deq), 27, "DEQ length not 27 after append")
        self.deq.append_left("ab")
        self.assertEqual(len(self.deq), 28, "DEQ length not 28 after append_left")

        # check pop, pop_left
        self.deq.pop()
        self.assertEqual(len(self.deq), 27, "DEQ length not 27 after pop")
        self.deq.pop_left()
        self.assertEqual(len(self.deq), 26, "DEQ length not 26 after pop_left")

        # check make_empty
        self.deq.make_empty()
        self.assertEqual(len(self.deq), 0, "DEQ length not 0 after make_empty")

    def test_str(self):
        letters = "abcdefghijklmnopqrstuvwxyz"
        string = str([letter for letter in letters])
        self.assertEqual(str(self.deq), string, "DEQ string incorrect")

        self.assertEqual(str(self.emptydeq), str([]), "Empty DEQ string incorrect")

    def test_bool(self):
        self.assertTrue(self.deq, "DEQ unexpectedly false")
        self.assertFalse(self.emptydeq, "Empty DEQ unexpectedly true")

    def test_append(self):
        item = "aa"
        self.assertNotIn(item, self.deq._data, "item unexpectedly in deq")
        self.deq.append(item)
        self.assertIn(item, self.deq._data, "item unexpectedly not in deq")
        self.assertEqual(item, self.deq._data[-1], "item unexpectedly not in place")

    def test_append_left(self):
        item = "aa"
        self.assertNotIn(item, self.deq._data, "item unexpectedly in deq")
        self.deq.append_left(item)
        self.assertIn(item, self.deq._data, "item unexpectedly not in deq")
        self.assertEqual(item, self.deq._data[0], "item unexpectedly not in place")

    def test_pop(self):
        self.assertEqual(self.deq.pop(), "z", "unexpected item from pop")

    def test_pop_left(self):
        self.assertEqual(self.deq.pop_left(), "a", "unexpected item from pop_left")

    def test_peek(self):
        self.assertEqual(self.deq.peek(), "z", "unexpected item from peek")
        self.assertIn("z", self.deq._data)

    def test_peek_left(self):
        self.assertEqual(self.deq.peek_left(), "a", "unexpected item from peek_left")
        self.assertIn("a", self.deq._data)

    def test_make_empty(self):
        self.assertTrue(self.deq)
        self.assertFalse(self.emptydeq)

        self.deq.make_empty()
        self.emptydeq.make_empty()

        self.assertFalse(self.deq)
        self.assertFalse(self.emptydeq)

        self.assertEqual(self.deq._data, [])
