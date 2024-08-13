class Actor:
    def __init__(self, data):
        self.id = data[0]
        self.first_name = data[1]
        self.last_name = data[2]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
