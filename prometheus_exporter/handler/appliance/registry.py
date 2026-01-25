class Registry(type):
    """Metaclass for registering appliance handlers."""

    mapper = {}

    def __new__(mcs, name, bases, attrs):
        klass = super(Registry, mcs).__new__(mcs, name, bases, attrs)
        if klass.KLASS:
            Registry.mapper[klass.KLASS] = klass
        return klass


registry = Registry.mapper
