class Request:
    def __init__(self, url, ref, flags=None, source_dir="app"):
        self.url = url
        self.ref = ref
        self.flags = [] if flags == None else flags
        self.source_dir=source_dir
 