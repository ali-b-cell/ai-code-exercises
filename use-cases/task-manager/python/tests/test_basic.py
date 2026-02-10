import unittest

class TestBasic(unittest.TestCase):
    def test_simple(self):
        """A simple test to verify testing works"""
        self.assertEqual(1 + 1, 2)

if __name__ == '__main__':
    unittest.main()
