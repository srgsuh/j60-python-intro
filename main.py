from collections import OrderedDict
from typing import  Hashable, Generic, Iterator, TypeVar
K = TypeVar('K', bound=Hashable)
V = TypeVar("V")

 ####################################################################################
class  LfuDictCache(Generic[K, V]):
    def __init__(self, max_size: int):
       #write constructor for defining encapsulated data structure
       if max_size < 1:
           raise ValueError("The dictionary size cannot be less then 1")
       self.max_size = max_size
       self.min_count = 1
       self.nodes: dict[K, int] = {} # stores frequencies of entries
       self.freq_dict: dict[int, OrderedDict] = {} # keys: frequencies of entries -> OrderedDict (as FIFO) of [K, V]

    def __extract(self, key: K, count: int) -> V:
        ordered_dict: OrderedDict = self.freq_dict[count]
        value: V = ordered_dict.pop(key)
        if not ordered_dict:
            del self.freq_dict[count]
            if count == self.min_count:
                self.min_count += 1
        return value
    
    def __put(self, key: K, value: V, count: int):
        ordered_dict: OrderedDict = self.freq_dict.setdefault(count, OrderedDict())
        ordered_dict[key] = value
        self.nodes[key] = count

    def __getitem__(self, key: K) -> V:
        #method for square braces operator [] getting key and returnin value with throwing
        #KeyError exception if key is missing
        count: int = self.nodes[key]
        value: V = self.__extract(key, count)
        self.__put(key, value, count + 1)
        
        return value
    
    def __pop_last(self) -> V:
        ordered_dict = self.freq_dict[self.min_count]
        key, value = ordered_dict.popitem(last = False)
        if not ordered_dict:    
            del self.freq_dict[self.min_count]
        del self.nodes[key]
        
        return value

    def __setitem__(self, key: K, value: V):
        # method for square braces operator [] either updating existing key-value association or adding a new one
        count: int = self.nodes.get(key, 0)
        if count:
            self.__extract(key, count)
        elif len(self) == self.max_size:
            self.__pop_last()
            self.min_count = 1
        self.__put(key, value, count + 1)

    def __delitem__(self, key: K):
        # method for deleting key-value association from a dictionary with throwing KeyError exception
        # in the case of missing key like del dict[key] 
        count: int = self.nodes[key]
        ordered_dict: OrderedDict = self.freq_dict[count]
        ordered_dict.pop(key)
        if not ordered_dict:
            del self.freq_dict[count]
            if count == self.min_count:
                self.min_count = min(self.freq_dict.keys())
        del self.nodes[key]

    def __iter__(self) -> Iterator[K]:
        # method for iterating keys in arbitrary order 
        return iter(self.nodes.keys())
    
    def __len__(self)->int:
        # method returning number of key-value associations (pairs)
        return len(self.nodes)
