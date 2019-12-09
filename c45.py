from c45lib import c45lib, utils
from classes.Expression import Expression

labels = [
    'Sex',
    'Length',
    'Diameter',
    'Height',
    'Whole weight',
    'Shucked weight',
    'Viscera weight',
    'Shell weight'
]

# gets the data and results from dataset
data = c45lib.get_data_from_file('datasets/abaloneFormatada.csv')
data = utils.convert_numeric_values(data)

c45lib.print_tree(c45lib.generate_tree(data))
