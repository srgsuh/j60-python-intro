from collections import OrderedDict
from typing import  Hashable, Generic, Iterator, TypeVar
from sortedcontainers import SortedList
from dataclasses import dataclass
K = TypeVar('K', bound=Hashable)
V = TypeVar("V")

  ####################################################################################



class DictCache(OrderedDict[K, V]) :
    def __init__(self, maxsize=128):
        super().__init__() # calls constructor of OrderedDict that has all methods for keeping insertion order
        self.maxsize = maxsize
    # The  methods __getitem__ and __setitem__ should be overriden
    # Assumption: only following methods should be overriden for making tests from test_dict_cache.py passed
    # Hints as follows: 
    # super().__getitem__(key) calls method __getitem__ of OrderedDict
    # super().__setitem__(key, value) calls method __setitem__ of OrderedDict
    # consider using self.move_to_end(key) of OrderedDict for making item with the given key as most recent
    # consider using self.popitem(last=False) for removing least recent (eldest item)
    
    def __getitem__(self, key)->V:
       res =  super().__getitem__(key)
       self.move_to_end(key)
       return res

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
        if len(self) > self.maxsize:
            self.popitem(last = False)

@dataclass
class FreqCounter[K]:
    frequency: int
    key: K

        
class  LfuDictCache(Generic[K, V]):
    def __init__(self, max_size: int):
        #TODO write constructor for defining encapsulated data structure
        self.max_size = max_size
        self.data: DictCache[K, tuple[V, FreqCounter]] = DictCache(max_size)
        self.data_freq: SortedList = SortedList()
    
    def __update_frequency(self, counter: FreqCounter) -> FreqCounter:
        self.data_freq.remove(counter)
        new_counter = FreqCounter(counter.frequency + 1, counter.key)
        self.data_freq.add(new_counter)
        return new_counter

    def __getitem__(self, key: K) -> V:
        #TODO method for square braces operator [] getting key and returnin value with throwing
        #KeyError exception if key is missing
        value, counter = self.data[key]
        self.data[key] = value, self.__update_frequency(counter)
        return value

    def __setitem__(self, key: K, value: V):
        # TODO method for square braces operator [] either updating existing key-value association or adding a new one
        
        raise NotImplementedError() 
    def __delitem__(self, key: K):
        # TODO method for deleting key-value association from a dictionary with throwing KeyError exception
        # in the case of missing key like del dict[key] 
        raise NotImplementedError()
    def __iter__(self) -> Iterator[K]:
        # TODO method for iterating keys in arbitrary order 
        raise NotImplementedError()
    def __len__(self)->int:
        # TODO method returning number of key-value associations (pairs)
        raise NotImplementedError()
