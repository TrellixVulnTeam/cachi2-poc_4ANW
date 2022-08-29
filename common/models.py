class Request:
    def __init__(self, id, url, ref, flags=None):
        self.id = id
        self.url = url
        self.ref = ref
        self.flags = [] if flags == None else flags
