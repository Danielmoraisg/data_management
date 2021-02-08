import streamlit as st
from States import _get_state
from PIL import Image
#img = Image.open('pharmacy.png').convert('RGB')
#paginas
import home

st.set_page_config(page_title="Automated BI",page_icon=':fire:',layout="centered",initial_sidebar_state="collapsed")
state = _get_state()

PAGES = {
	"Home":home
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app(state)
state.sync()