#!/usr/bin/python
# Created 08/2010.  Unknown Source
'''
class Singleton(object):
  _instance = None
  def __new__(class_, *args, **kwargs):
    if not isinstance(class_._instance, class_):
        class_._instance = object.__new__(class_, *args, **kwargs)
    return class_._instance
'''
class Singleton(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        """This method overrides calls to the __new__
class method of any class that inherits from Singleton,
giving us a chance to return a single instance of
that object.
"""
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

#'''
def test():
    class S(Singleton):
        pass

    s1 = S()
    s2 = S()
    
    print("id(s1) =", id(s1))
    print("id(s2) =", id(s2))

if __name__ == "__main__":
    test()
