class Foo:
    _price = 0

    def __init__(self, inValue=0):
        self._value = inValue

    def test(self):
        print("teest")

    @property
    def price(self):
        """Getter: Called when you run `obj.price`"""
        print("Fetching price...")
        return self._price

    @price.setter
    def price(self, value):
        """Setter: Called when you run `obj.price = new_value`"""
        if value < 0:
            raise ValueError("Price cannot be negative!")
        print(f"Updating price... {value}")
        self._price = value


# Define getter and setter functions later
def get_value(self):
    return self._value


def set_value(self, val):
    self._value = val


# Add the property to the class post-declaration
Foo.value = property(get_value, set_value)


foo = Foo()
foo.a = 3
Foo.b = property(lambda self: self.a + 1)

foo.value = 10

print(foo.b)
print(foo.value)



foo.price = 123

print(foo.price)



