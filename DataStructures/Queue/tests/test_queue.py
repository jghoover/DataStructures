import unittest
from DataStructures import Queue


class QueueTestCase(unittest.TestCase):
    def setUp(self):
        self.emptyqueue = Queue()

        self.queue = Queue()
        for letter in "abcdefghijklmnopqrstuvwxyz":
            self.queue.enqueue(letter)

    def test_len(self):
        self.assertEqual(len(self.queue), 26, "Queue length not 26")
        self.assertEqual(len(self.emptyqueue), 0, "Empty queue length not 0")

        self.queue.enqueue("aa")
        self.assertEqual(len(self.queue), 27, "Queue length not 27 after enqueue")

        self.queue.dequeue()
        self.assertEqual(len(self.queue), 26, "Queue length not 26 after dequeue")

        self.queue.make_empty()
        self.assertEqual(len(self.queue), 0, "Queue length not 0 after make_empty")

    def test_str(self):
        letters = "abcdefghijklmnopqrstuvwxyz"
        string = str([letter for letter in letters])
        self.assertEqual(str(self.queue), string, "Queue string not equal")
        self.assertEqual(str(self.emptyqueue), str([]), "Empty queue string not equal")

    def test_bool(self):
        self.assertTrue(self.queue, "Queue unexpectedly false")
        self.assertFalse(self.emptyqueue, "Empty queue unexpectedly true")

    def test_enqueue(self):
        item = "aa"
        self.assertNotIn(item, self.queue._data)
        self.queue.enqueue(item)
        self.assertIn(item, self.queue._data)
        self.assertEqual(item, self.queue._data[-1])

    def test_dequeue(self):
        self.assertEqual(self.queue.dequeue(), "a")
        self.assertNotIn("a", self.queue._data)

        with self.assertRaises(IndexError):
            self.emptyqueue.dequeue()

    def test_peek(self):
        self.assertEqual(self.queue.peek(), "a")
        self.assertIn("a", self.queue._data)

        with self.assertRaises(IndexError):
            self.emptyqueue.peek()

    def test_make_empty(self):
        self.assertTrue(self.queue)
        self.queue.make_empty()
        self.assertEqual(self.queue._data, [])
