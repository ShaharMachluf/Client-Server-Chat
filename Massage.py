class Massage:
    def __init__(self, src, text, dest=None):
        self.src = src
        if dest is None:
            self.dest = "all"
        else:
            self.dest = dest
        self.text = text

    def __repr__(self):
        return "from: " + self.src + " to: " + self.dest + " \n" + self.text + ""
