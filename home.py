import streamlit as st 
import pandas as pd

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
			#options for plain text upload
			elif state.name.split('.')[1] == 'csv' or state.name.split('.')[1] == 'txt' :
				if st.checkbox('More options', value = False):
					state.data = pd.read_csv(upload)
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

					#state.data = pd.read_csv(upload, skiprows = skip-1, header = header)[0:last]
					#st.write(state.data.head(5))
				else:
					upload.seek(0)
					state.data = pd.read_csv(upload)
					#st.write(state.data.head(5))
	st.write(state.data.head(5))
	with st.beta_expander('Data Pre-Processing'):
		if st.checkbox('Fill empty values ?'):
			to_do_na = st.selectbox('Fill using:',('Numbers','Words','Dates'))
			if to_do_na == 'Numbers':
				new_val = st.number_input('Type the number', value = 0)
			elif to_do_na == 'Words':
				new_val = st.text_input('Type the word')
			else:
				new_val = st.date_input('Select date')
			state.data.fillna(new_val)
	with st.beta_expander("See complete data"):
		st.write(state.data)

	
	

		