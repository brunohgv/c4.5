def convert_numeric_values(dataset):
    new_dataset = []
    for row in dataset:
        new_row = []
        for index, col in enumerate(row):
            try:
                if index != len(row) - 1:
                    col = float(col)
                new_row.append(col)
            except ValueError:
                new_row.append(col)

        new_dataset.append(new_row)

    return new_dataset


def get_unique_values(dataset, column):
    return set(row[column] for row in dataset)


def is_continuous(value):
    try:
        return isinstance(value, (float, int))
    except ValueError:
        return False
