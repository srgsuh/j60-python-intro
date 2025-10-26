from collections import OrderedDict
from typing import  Hashable, Generic, Iterator, TypeVar
from sortedcontainers import SortedDict
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

@dataclass(frozen=True)
class CacheNode[K, V]:
    key: K
    value: V
    count: int
        
class  LfuDictCache(Generic[K, V]):
    def __init__(self, max_size: int):
       #TODO write constructor for defining encapsulated data structure
       if max_size < 1:
           raise ValueError("The dictionary size cannot be less then 1")
       self.max_size = max_size
       self.nodes: dict[K, CacheNode[K, V]] = {}
       self.freq_dict: SortedDict = SortedDict()

    def __eject(self, cache_node: CacheNode[K, V]):
        ordered_dict: OrderedDict = self.freq_dict[cache_node.count]
        ordered_dict.pop(cache_node.key)
        if not ordered_dict:
            del self.freq_dict[cache_node.count]
    
    def __put(self, cache_node: CacheNode[K, V]):
        key, count = cache_node.key, cache_node.count
        if not count in self.freq_dict:
            self.freq_dict[count] = OrderedDict()
        ordered_dict: OrderedDict = self.freq_dict[count]
        ordered_dict[key] = cache_node
        self.nodes[key] = cache_node

    def __getitem__(self, key: K) -> V:
        #TODO method for square braces operator [] getting key and returnin value with throwing
        #KeyError exception if key is missing
        node = self.nodes[key]
        self.__eject(node)
        self.__put(CacheNode(key, node.value, node.count + 1))
        return node.value
    
    def __pop_last(self) -> CacheNode[K, V]:
        count, ordered_dict = self.freq_dict.peekitem(0)
        key, last_node = ordered_dict.popitem(last = False)
        if not ordered_dict:    
            del self.freq_dict[count]
        del self.nodes[key]
        
        return last_node

    def __setitem__(self, key: K, value: V):
        # TODO method for square braces operator [] either updating existing key-value association or adding a new one
        node: CacheNode[K, V] | None = self.nodes.get(key)
        if node:
            self.__eject(node)
        elif len(self) == self.max_size:
            self.__pop_last() 
        self.__put(CacheNode(key, value, node.count + 1 if node else 1))

    def __delitem__(self, key: K):
        # TODO method for deleting key-value association from a dictionary with throwing KeyError exception
        # in the case of missing key like del dict[key] 
        node: CacheNode[K, V] = self.nodes[key]
        self.__eject(node)
        del self.nodes[key]

    def __iter__(self) -> Iterator[K]:
        # TODO method for iterating keys in arbitrary order 
        return iter(self.nodes.keys())
    
    def __len__(self)->int:
        # TODO method returning number of key-value associations (pairs)
        return len(self.nodes)
