import unittest

print("fine")

# dont forget the (unittest.TestCase)

class TrivialTest(unittest.TestCase):

    def test_fail1(self):
        """ deliberately failing test. """
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
