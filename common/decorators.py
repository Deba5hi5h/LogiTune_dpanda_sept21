class Singleton:
    """
    This decorator prevents from wasting memory for allocating new class instances when these do not differ
    between each other.
    """

    instance = None

    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        if not self.instance:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


class LazyProperty(object):
    """
    A descriptor class that implements lazy evaluation of a property.

    LazyProperty is used as a decorator to define a lazily evaluated property.
    The value of the property is calculated only when accessed for the first time.
    The calculated value is then cached and returned for subsequent accesses.
    """
    def __init__(self, function):
        self.function = function
        self.name = function.__name__

    def __get__(self, obj, *args, **kwargs) -> object:
        obj.__dict__[self.name] = self.function(obj)
        return obj.__dict__[self.name]
