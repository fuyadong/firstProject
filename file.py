# -*- coding:utf-8 -*-

"""
Test memory usage
"""

import objgraph
from memory_profiler import profile


@profile(precision=4)
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a


def cycle_ref():
    x = []
    y = [x, [x], dict(x=x)]

    # objgraph.show_refs([y], filename='smaple-graph.png')
    objgraph.show_backrefs([x], filename='sample-backref-graph.png')
    objgraph.show_most_common_types()


class MyBigFatObject(object):
    pass


def leak_memory_test(_cache={}):
    print "lalla"
    _cache[42] = dict(foo=MyBigFatObject(),
                      bar=MyBigFatObject())

    mbfo = MyBigFatObject()


if __name__ == '__main__':
    # my_func()
    # cycle_ref()
    # import pydot
    # (graph,) = pydot.graph_from_dot_file('objgraph-8hdjQM.dot')
    # graph.write_png('smaple-graph.png')
    pass

leak_memory_test()
objgraph.show_growth()

