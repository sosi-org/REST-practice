import unittest

# dont forget the (unittest.TestCase)
class TrivialTest(unittest.TestCase):

    def test_fail1(self):
        """ deliberately failing test. """
        self.assertEqual(2, 2)

if __name__ == '__main__':
    unittest.main()
