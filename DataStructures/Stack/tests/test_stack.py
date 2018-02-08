import unittest
from DataStructures import Stack


class StackTestCase(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()
        for letter in "abcdefghijklmnopqrstuvwxyz":
            self.stack.push(letter)

        self.emptystack = Stack()

    def test_len(self):
        self.assertEqual(len(self.stack), 26, "Stack missing items")
        self.assertEqual(len(self.emptystack), 0, "Empty stack has something")

        # check adding an item to the stack increases its length by 1
        item = "aa"
        self.stack.push(item)
        self.emptystack.push(item)
        self.assertEqual(len(self.stack), 27, "Stack missing items after push")
        self.assertEqual(len(self.emptystack), 1, "Empty stack missing items after push")

        self.stack.pop()
        self.emptystack.pop()
        self.assertEqual(len(self.stack), 26, "Stack missing items after pop")
        self.assertEqual(len(self.emptystack), 0, "Empty stack missing items after pop")

    def test_str(self):
        letters = "abcdefghijklmnopqrstuvwxyz"
        string = str([letter for letter in letters])
        self.assertEqual(str(self.stack), string, "Stack string not equal")

        self.assertEqual(str(self.emptystack), str([]), "Empty stack string not equal")

    def test_bool(self):
        self.assertTrue(self.stack, "Stack is not true")
        self.assertFalse(self.emptystack, "Empty stack not false")

    def test_push(self):
        item = "aa"
        self.assertNotIn(item, self.stack._data, "Unexpected item in stack before push")
        self.stack.push(item)
        self.assertIn(item, self.stack._data, "Item missing from stack after push")

    def test_pop(self):
        self.assertEqual(self.stack.pop(), "z", "Unexpected item returned from pop")

        with self.assertRaises(IndexError, msg="Empty stack pop didn't raise IndexError"):
            self.emptystack.pop()

    def test_peek(self):
        self.assertEqual(self.stack.peek(), "z", "Unexpected item returned from peek")

        with self.assertRaises(IndexError, msg="Empty stack peek didn't raise IndexError"):
            self.emptystack.peek()

    def test_make_empty(self):
        self.assertTrue(self.stack, "Stack unexpectedly false")
        self.assertEqual(len(self.stack), 26, "Length of stack unexpectedly not 26")
        self.stack.make_empty()
        self.assertFalse(self.stack, "Stack after make_empty unexpectedly true")
        self.assertEqual(len(self.stack), 0, "Length of stack after make_empty unexpectedly not 0")
        self.assertListEqual(self.stack._data, [], "Stack._data after make_empty unexpectedly not empty list")

