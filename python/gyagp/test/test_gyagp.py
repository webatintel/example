import unittest

class Test(unittest.TestCase):
    def test_win32api(self):
        try:
            import win32api
            self.assertTrue(True)
        except ImportError:
            self.assertTrue(False) 
        
    def test_gyagp(self):
        try:
            import gyagp
            self.assertTrue(True)
        except ImportError:
            self.assertTrue(False)   

    def test_gyagp_module(self):
        try:
            from gyagp import module
            self.assertTrue(True)
        except ImportError:
            self.assertTrue(False)            

if __name__ == "__main__":
    unittest.main()
