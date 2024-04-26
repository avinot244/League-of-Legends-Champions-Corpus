class RowContent:
    def __init__(self, text : str, label : int) -> None:
        self.text = text
        self.label = label

    def asDict(self):
        res : dict = dict()
        res["text"] = self.text
        res["label"] = self.label
        return res


class Row:
    def __init__(self, row_idx : int, row : RowContent) -> None:
        self.row_idx = row_idx
        self.row = row

    
    def asDict(self):
        res : dict = dict()
        res["row_idx"] = self.row_idx
        res["row"] = self.row.asDict()
        return res