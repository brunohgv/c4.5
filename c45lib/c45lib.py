import csv
from c45lib import utils
import math
from classes.Expression import Expression
from classes.Node import Node
from enum import Enum


def get_data_from_file(file_path):
    data = []
    with open(file_path, 'rU') as file:
        content = csv.reader(file, delimiter=',')
        for line in content:
            data.append(line)

    return data


def get_attribute_count(data, column):
    results_labels = {}

    # gets all possible results
    for row in data:
        if results_labels.get(row[column]) is None:
            results_labels[row[column]] = 0
        else:
            results_labels[row[column]] += 1

    return results_labels


def calculate_entropy(dataset):
    total = len(dataset)
    if total == 0:
        return 0
    labels_count = get_attribute_count(dataset, len(dataset[0]) - 1)

    entropy = 0

    for label in labels_count:
        if not (total == 0 or labels_count[label] == 0):
            entropy -= (labels_count[label] / total) * math.log((labels_count[label] / total), 2)

    return entropy


def calculate_gain(original_set, divided_sets):
    original_set_count = len(original_set)
    original_impurity = calculate_entropy(original_set)

    divided_sets_weights = [(len(subset) / original_set_count) for subset in divided_sets]

    impurity_after_split = 0

    for index in range(len(divided_sets)):
        impurity_after_split += divided_sets_weights[index] * calculate_entropy(divided_sets[index])

    gain = original_impurity - impurity_after_split
    return gain


def split_data(data, ignored_indexes):
    divided_data = []
    best_expression = None
    max_gain = float("-inf")

    for attribute_index in range(len(data[0]) - 1):
        if attribute_index not in ignored_indexes:
            attribute_values = list(utils.get_unique_values(data, attribute_index))
            if utils.is_continuous(attribute_values[0]):
                sorted_data = list(data)
                sorted_data.sort(key=lambda row: row[attribute_index])
                for row in range(len(sorted_data) - 1):
                    if sorted_data[row][attribute_index] != sorted_data[row + 1][attribute_index]:
                        middle_value = (sorted_data[row][attribute_index] + sorted_data[row + 1][attribute_index]) / 2
                        left = []
                        right = []
                        expression = Expression(attribute_index, middle_value)
                        for row_to_compare in range(len(sorted_data) - 1):
                            # print(attribute_index, row, row_to_compare)
                            if expression.compare_row(sorted_data[row_to_compare]):
                                left.append(sorted_data[row_to_compare])
                            else:
                                right.append(sorted_data[row_to_compare])

                        gain = calculate_gain(sorted_data, [left, right])

                        if gain > max_gain:
                            best_expression = expression
                            max_gain = gain
                            divided_data = [left, right]

            else:
                divided = []
                for value in attribute_values:
                    divided.append([])

                print(divided)
                for value_index, value in enumerate(attribute_values):
                    expression = Expression(attribute_index, value)
                    for row in data:
                        if expression.compare_row(row):
                            divided[value_index].append(row)

                    gain = calculate_gain(data, divided)

                    if gain > max_gain:
                        best_expression = expression
                        max_gain = gain
                        divided_data = divided

    return best_expression, divided_data


def remove_column(data, column_index):
    new_data = data

    for index, row in enumerate(new_data):
        del row[column_index]

    return new_data


def generate_tree(data, ignored_indexes=[]):

    if len(data) == 0:
        return Node(None, None, [])

    if len(data[0]) - len(ignored_indexes) == 1:
        return Node(count_classes(data), None, [])

    best_expression, divided_data = split_data(data, ignored_indexes)
    print(best_expression)
    ignored_indexes.append(best_expression.col_index)
    return Node(None, best_expression, [generate_tree(sub_data, ignored_indexes) for sub_data in divided_data])


def print_tree(tree, depth=0):
    spacer = ''

    for i in range(depth):
        spacer += '    '

    if tree.expression is None and tree.label is not None:
        print("{0}{1}".format(spacer, tree.label))
    else:
        print("{0}{1}".format(spacer, tree.expression))
        for child in tree.children:
            print_tree(child, depth + 1)


def count_classes(data):
    results_count = get_attribute_count(data, len(data[0]) - 1)
    max_result = max(results_count, key=results_count.get)
    return max_result
