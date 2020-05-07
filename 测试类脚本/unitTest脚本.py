import unittest

class test(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_1(self):
        self.assertEqual(1, 1)
    def test_2(self):
        self.assertEqual(1, 2)
    def test_3(self):
        self.assertEqual(1, 1)

# unittest.main()

if __name__=="__main__":

    # unittest.main()

    suite = unittest.TestSuite()
    suite.addTest(test("test_1"))
    suite.addTest(test("test_2"))
    suite.addTest(test("test_3"))

    rerun_results = unittest.TextTestRunner(verbosity=2).run(suite)
    print("1111111111111111111111111111111111111")
    for x in rerun_results.success:
        print(dir(x))
    print("1111111111111111111111111111111111111")