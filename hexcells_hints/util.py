from collections.abc import MutableMapping


class SloppyDict(MutableMapping):
    def __init__(self, range, data):
        self.range = range
        self.data = data

    def __getitem__(self, key):
        for n in range(key - self.range, key + self.range + 1):
            if n in self.data:
                return self.data[n]
        return self.data[key]

    def __setitem__(self, key, value):
        for n in range(key - self.range, key + self.range + 1):
            if n in self.data:
                self.data[n] = value
        self.data[key] = value

    def __delitem__(self, key):
        for n in range(key - self.range, key + self.range + 1):
            if n in self.data:
                del self.data[n]
        del self.data[key]

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    def keys(self):
        return self.data.keys()
