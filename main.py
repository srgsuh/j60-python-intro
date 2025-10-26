from collections import OrderedDict
from typing import  Hashable, Generic, Iterator, TypeVar
from sortedcontainers import SortedDict
from dataclasses import dataclass
K = TypeVar('K', bound=Hashable)
V = TypeVar("V")

 ####################################################################################
@dataclass(frozen=True)
class CacheNode[V]:
    value: V
    count: int
        
class  LfuDictCache(Generic[K, V]):
    def __init__(self, max_size: int):
       #TODO write constructor for defining encapsulated data structure
       if max_size < 1:
           raise ValueError("The dictionary size cannot be less then 1")
       self.max_size = max_size
       self.nodes: dict[K, CacheNode[V]] = {}
       self.freq_dict: SortedDict = SortedDict() # keys: frequencies of entries, values: OrderedDict (as FIFO) of nodes

    def __eject(self, key: K, count: int):
        ordered_dict: OrderedDict = self.freq_dict[count]
        ordered_dict.pop(key)
        if not ordered_dict:
            del self.freq_dict[count]
    
    def __put(self, key: K, cache_node: CacheNode[V]):
        count = cache_node.count
        ordered_dict: OrderedDict = self.freq_dict.setdefault(count, OrderedDict())
        ordered_dict[key] = cache_node
        self.nodes[key] = cache_node

    def __getitem__(self, key: K) -> V:
        #TODO method for square braces operator [] getting key and returnin value with throwing
        #KeyError exception if key is missing
        node = self.nodes[key]
        self.__eject(key, node.count)
        self.__put(key, CacheNode(node.value, node.count + 1))
        return node.value
    
    def __pop_last(self) -> CacheNode[V]:
        count, ordered_dict = self.freq_dict.peekitem(0)
        key, last_node = ordered_dict.popitem(last = False)
        if not ordered_dict:    
            del self.freq_dict[count]
        del self.nodes[key]
        
        return last_node

    def __setitem__(self, key: K, value: V):
        # TODO method for square braces operator [] either updating existing key-value association or adding a new one
        node: CacheNode[V] | None = self.nodes.get(key)
        if node:
            self.__eject(key, node.count)
        elif len(self) == self.max_size:
            self.__pop_last() 
        self.__put(key, CacheNode(value, node.count + 1 if node else 1))

    def __delitem__(self, key: K):
        # TODO method for deleting key-value association from a dictionary with throwing KeyError exception
        # in the case of missing key like del dict[key] 
        node: CacheNode[V] = self.nodes[key]
        self.__eject(key, node.count)
        del self.nodes[key]

    def __iter__(self) -> Iterator[K]:
        # TODO method for iterating keys in arbitrary order 
        return iter(self.nodes.keys())
    
    def __len__(self)->int:
        # TODO method returning number of key-value associations (pairs)
        return len(self.nodes)
