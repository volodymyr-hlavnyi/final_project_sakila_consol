class SearchQuery:
    def __init__(self, data):
        self.query = data[0]
        self.query_count = data[1]

    def __str__(self):
        return f"{self.query} ({self.query_count})"
