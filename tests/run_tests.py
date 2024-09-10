import unittest

if __name__ == '__main__':
    """
    Main execution point of the tests.
    """
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='./tests', pattern='*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)