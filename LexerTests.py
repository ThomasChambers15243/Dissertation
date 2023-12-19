import unittest


class Test(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


def suite():
    suite = unittest.TestSuite()

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    testRun = runner.run(suite())
    print(testRun)
