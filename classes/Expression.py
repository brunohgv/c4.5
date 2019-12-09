from c45lib import utils


class Expression:

    def __init__(self, col_index, value):
        self.col_index = col_index
        self.value = value

    def compare_row(self, row):
        if utils.is_continuous(row[self.col_index]):
            return self.value < row[self.col_index]
        else:
            return self.value == row[self.col_index]

    def __repr__(self):
        symbol = ">" if utils.is_continuous(self.value) else '=='
        return "Column {0} {1} {2}?".format(self.col_index, symbol, self.value)
