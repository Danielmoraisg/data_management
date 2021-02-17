import numpy as np
import streamlit as st


def by_itself (column, operation):
	if operation == 'Cosine':
		return np.cos(column)
	elif operation == 'Tangent':
		return np.tan(column)
	elif operation == 'Sine':
		return np.sin(column)
	elif operation == 'Natural logarithm':
		return np.log(column)
	elif operation == 'Tangent':
		return np.tan(column)

def by_number (column, operation):
	if operation == 'sum':
		number = st.number_input('what is the number', value = 2.0)
		return column.apply(lambda x: x+number)
	elif operation == 'logarithm':
		base = st.number_input('what is the base', value = 10.0)
		return np.log(column) / np.log(base)
	elif operation == 'root':
		number =  st.number_input('what is the number of the root e.g., square root = 2', value = 2.0)
		return column.apply(lambda x: x**(1/number))
	elif operation == 'exponent':
		number = st.number_input('what is the exponent', value = 2.0)
		return column.apply(lambda x: x**number)
	elif operation == 'multiplication':
		number = st.number_input('what is the number', value = 2.0)
		return column.apply(lambda x: x*number)
	elif operation == 'division':
		number = st.number_input('what is the number', value = 2.0)
		return column.apply(lambda x: x/number)
	elif operation == 'subtraction':
		number = st.number_input('what is the number', value = 2.0)
		return column.apply(lambda x: x-number)

def by_column(column_1, column_2, operations):
	if operations =='sum':
		return column_1 + column_2
	elif operations == 'subtraction':
		return column_1 - column_2
	elif operations == 'division':
		return column_1 / column_2
	elif operations == 'multiplication':
		return column_1 * column_2
	elif operations == 'exponent':
		return column_1 ** column_2
	elif operations =='root':
		return column_1 ** (1/column_2)
	elif operations == 'logarithm':
		return np.log(column_1) / np.log(column_2)