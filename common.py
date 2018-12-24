class Directory:
    def __init__(self, name, files=[], directories=[]):
        self.name = name
        self.files = files
        self.directories = directories


class Source:
    def __init__(self, filename, src=""):
        self.filename = filename
        self.src = src
