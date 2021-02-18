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

def by_column(cols, operations):
	if operations =='sum':
		return cols.sum(axis = 1)
	else:
		expression = ''
		for i in cols:
			#st.write(cols[i])
			if operations == 'subtraction':
				expression +="cols['%s']-"%i
			elif operations == 'division':
				expression +="cols['%s']/"%i
			elif operations == 'multiplication':
				expression +="cols['%s']*"%i
			elif operations == 'exponent':
				expression +="cols['%s']**"%i
		if operations == 'exponent':
			return eval(expression[:-2])
		else:
			return eval(expression[:-1])