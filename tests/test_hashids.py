from hashids import Hashids


def test_1():
    hashids = Hashids(salt="this is my salt")
    id = hashids.encode(1, 2, 3)
    print(id)
    numbers = hashids.decode(id)
    print(numbers)
