import streamlit as st 
import pandas as pd
import chardet
def app(state):
	st.title('Upload your data')
	st.write('Click the button below to add your dataset and check if your data is correct')
	upload = st.file_uploader('',accept_multiple_files = False)

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
					state.data = pd.read_csv(upload, sep = sep, encoding = result['encoding'])
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

					state.data = pd.read_csv(upload, skiprows = skip-1, header = header, sep = sep, encoding = result['encoding'])[0:last]
					#st.write(state.data.head(5))
				else:
					upload.seek(0)
					try:
						state.data = pd.read_csv(upload, sep = sep, encoding = result['encoding'])
					except  pd.errors.ParserError:
						st.write('Your separator is "%s" . It is problably wrong, open your file and check it. If it is ok file an issue. Sorry for the incovenience' %(sep))
					#st.write(state.data.head(5))
	
	#show begining of dataset
	try:
		st.write(state.data.head(5))
	except:
		st.write('Waiting...')

	# Data pre processing
	with st.beta_expander('Data Pre-Processing'):

		#deal with missing values
		if st.checkbox('Fill empty values ?', value = True):
			to_do_na = st.selectbox('Fill using:',('Numbers','Words','Dates'))
			if to_do_na == 'Numbers':
				new_val = st.number_input('Type the number', value = 0)
			elif to_do_na == 'Words':
				new_val = st.text_input('Type the word')
			else:
				new_val = st.date_input('Select date')
			try:
				state.data.fillna(new_val)
			except:
				st.write('Please upload your data')
		#Change column name
		if st.checkbox('Change column names ?', value  =  False):
			new_columns = {}
			for col in state.data.columns:
				new_columns[col] = st.text_input("Column '%s' new name"%col, value = col)
			state.data = state.data.rename(columns = new_columns)
	
	with st.beta_expander("See complete data"):
		st.write(state.data)

	with st.beta_expander("data visualisation"):
		st.write("here we will put multiple plots to help visualise your data")
	
	with st.beta_expander("Prediciton"):
		st.write('Here we will apply statistical modeling and artificial inteligence to create equations or to predict future values')
	
	with st.beta_expander('Report'):
		st.write('Here we will display or download a full report on your data')
	
	

		