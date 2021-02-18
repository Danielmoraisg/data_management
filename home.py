import streamlit as st 
import pandas as pd
import chardet

from Data_transformation import *

def app(state):
	st.title('Upload your data')
	st.write('Click the button below to add your dataset and check if your data is correct')
	upload = st.file_uploader('',accept_multiple_files = False)
	placeholder_data = {'vWMF9pPHn2':'placeholder'}
	state.data = pd.DataFrame(placeholder_data, columns = ['vWMF9pPHn2'], index = [0])
	if upload is not None:
			state.name = upload.name
			if state.name.split('.')[1] == 'xlsx' or state.name.split('.')[1] == 'xls' :
				data = upload.read()
				excel = pd.ExcelFile(data)
				sheet = st.selectbox('Sheet from excel file to be used',excel.sheet_names)
				
				#options for excel upload
				if st.checkbox('More options', value = False):
					state.data = pd.read_excel(data, sheet_name = sheet)
					total = len(state.data)
					if st.checkbox('Select first and last row of the dataset'):
						skip = st.number_input('Beginning of the dataset', value = 1)
						last = st.number_input('End of the dataset', value = total)
					else:
						skip = 0
						last = total
					if st.checkbox('Does your data has a Header?', value = True):
						header = 0
					else:
						header = None

					state.data = pd.read_excel(data, sheet_name = sheet, skiprows = skip-1, header = header)[0:last]
					#st.write(state.data.head(5))
				else:
					state.data = pd.read_excel(data, sheet_name = sheet)
					#st.write(state.data.head(5))
			
			elif state.name.split('.')[1] == 'csv' or state.name.split('.')[1] == 'txt' :
				result = chardet.detect(upload.read(100000))
				sep = st.text_input('What is the field separator ?', value = ',')
				#options for plain text upload
				if st.checkbox('More options', value = False):
					if st.checkbox('Select decimal marker'):
						dec = st.text_input('Decimal marker', value = ',')
					else:
						dec = ','
					if st.checkbox('Select thousands marker'):
						thou = st.text_input('Thousands marker', value = '.')
					else:
						thou = '.'					
					upload.seek(0)
					state.data = pd.read_csv(upload, sep = sep, encoding = result['encoding'], decimal = dec, thousands = thou)
					total = len(state.data)
					if st.checkbox('Select first and last row of the dataset'):
						skip = st.number_input('Beginning of the dataset', value = 1)
						last = st.number_input('End of the dataset', value = total)
					else:
						skip = 0
						last = total
					if st.checkbox('Does your data has a Header?', value = True):
						header = 0
					else:
						header = None
					upload.seek(0)
					#st.write(pd.read_csv(upload))

					state.data = pd.read_csv(upload, skiprows = skip-1, header = header, sep = sep,thousands = thou, encoding = result['encoding'], decimal = dec)[0:last]
					#st.write(state.data.head(5))
				else:
					upload.seek(0)
					try:
						state.data = pd.read_csv(upload, sep = sep, encoding = result['encoding'])
					except  pd.errors.ParserError:
						st.write('Your separator is "%s" . It is problably wrong, open your file and check it. If it is ok file an issue. Sorry for the incovenience' %(sep))
					#st.write(state.data.head(5))
	
	#show begining of dataset
	if 'vWMF9pPHn2' not in state.data.columns:
		st.write(state.data.head(5))
	else:
		st.write('Waiting...')

	# Data pre processing
	with st.beta_expander('Data Pre-Processing'):

		#deal with missing values
		st.write("**If you don't have missing values in your data you can uncheck the box bellow**" )
		if st.checkbox('Fill empty values', value = True):
			cols = []
			for i in state.data.columns:
				if st.checkbox('%s has missing values to tranform'%(i)):
					cols.append(i)
			for i in cols:
				method = None
				to_do_na = st.selectbox('Fill %s using:'%(i),('Numbers','Words','Dates','Previous value','Next value'), key = i)
				if to_do_na == 'Numbers':
					new_val = st.number_input('Type the number', value = 0, key = i)
					state.data.fillna({i:new_val}, inplace = True)
				elif to_do_na == 'Words':
					new_val = st.text_input('Type the word', key = i)
					state.data.fillna({i:new_val}, inplace = True)
				elif to_do_na == 'Dates':
					new_val = st.date_input('Select date', key = i)
					state.data.fillna({i:new_val}, inplace = True)
				elif to_do_na == 'Previous value':
					method = 'ffill'
					state.data[i].fillna(method = method, inplace = True)
				elif to_do_na == 'Next value':
					method = 'bfill'
					state.data[i].fillna(method = method, inplace = True)

			#Change column name
		if st.checkbox('Change column names ?', value  =  False):
			new_columns = {}
			for col in state.data.columns:
				new_columns[col] = st.text_input("Column '%s' new name"%col, value = col)
			state.data = state.data.rename(columns = new_columns)
# Modify dataset
	with st.beta_expander('Data transformation'):

		if st.checkbox('Simple mathematical operations'):
			type_of_operations = ['Operation using a single number e.g., column + 4', 'Operation using multiple columns element wise e.g., column 1 + column 2 + column 3']
			selection_of_type = st.selectbox('Which type of operation do you want?', type_of_operations)
			operations = ['sum','subtraction','division','multiplication','exponent','root','logarithm','Natural logarithm','Cosine','Sine','Tangent']
			operation_type = st.selectbox('Select type of operation',operations)

			if type_of_operations[0] == selection_of_type:
				transf_col = st.selectbox('select column to be used. You can only use columns with numbers',state.data.select_dtypes(exclude = 'O').columns)
				if operation_type in ['Natural logarithm','Cosine','Sine','Tangent']:
					new_col = by_itself(state.data[transf_col],operation_type)
				else:
					new_col = by_number(state.data[transf_col],operation_type)
			elif type_of_operations[1] == selection_of_type:
				N_cols_used = st.number_input('Select the number of columns that are going to be used', value = 2)
				if operation_type in ['Natural logarithm','Cosine','Sine','Tangent','root','logarithm']:
					st.write('Operation not supported between columns. Try "Operation using a single number"')
				else:
					cols = []
					for i in range(N_cols_used):
						cols.append(st.selectbox('Column %i' %(i+1),[i for i in state.data.select_dtypes(exclude = 'O').columns if i not in cols]))
					new_col = by_column(state.data[cols],operation_type)
			new_col_name = st.text_input('Name your new column. If there you name it as some existing column it will replace the old one', value = 'New')
			state.data[new_col_name] = new_col
		elif st.checkbox('Complex mathematical operations'):
			st.write('**WORK IN PROGRESS**')

#put new vector in the data
	with st.beta_expander("See complete data"):
		st.write(state.data)

	with st.beta_expander("Data visualisation"):
		st.write("here we will put multiple plots to help visualise your data")
	
	with st.beta_expander("Prediciton"):
		st.write('Here we will apply statistical modeling and artificial inteligence to create equations or to predict future values')
	
	with st.beta_expander('Report'):
		st.write('Here we will display or download a full report on your data')
	
	

		