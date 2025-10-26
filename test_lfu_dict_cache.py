from main import LfuDictCache
from unittest import TestCase, main
class TestLfuDictCache(TestCase):
    def setUp(self):
        self.cache = LfuDictCache(3)
        self.cache["a"] = 1
        self.cache["b"] = 2
        self.cache["c"] = 3
    def test_same_frequency(self): 
        self.cache["d"] = 4
        '''
        since the same frequency
        key "a" will be deleted as LRU (Least Recently Used)
        ''' 
        self.assertRaises(KeyError, lambda : self.cache["a"]) 
    def test_different_frequency(self):
        '''access the key "a" four times'''
        self.cache["a"] = 10
        self.assertEqual(10, self.cache["a"]) 
        self.cache["a"] = 40
        self.assertEqual(40, self.cache["a"])
        '''access "c" and "b"''' 
        self.assertEqual(3, self.cache["c"])
        self.assertEqual(2, self.cache["b"])
        self.cache["d"] = 4
        '''
        Least Recently used is "a" but it won't be deleted as it is Most Frequent Used 
        The "c" will be deleted because "b" and "c" used with the same frequency but
        "c" is Least Recently Used comparing with "b"
        '''
        self.assertRaises(KeyError, lambda: self.cache["c"])
        self.assertEqual(40, self.cache["a"])
        self.assertEqual(2, self.cache["b"])
        
    def test_iterating_deleting(self):
        self.__runIteratingTest(["a", "b", "c"])  
        del self.cache["c"] 
        self.__runIteratingTest(["a", "b"])
    def test_len(self):
        self.assertEqual(3, len(self.cache))    
        
    def __runIteratingTest(self, expected: list["str"]):
        actual: list[str]  = sorted([k for k in self.cache] )
        self.assertEqual(expected, actual)  
        
if __name__ == "__main__":
    main()
        
         