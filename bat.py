import  streamlit as st

x = st.slider("select a value")
st.write(x,"squared is", x *x )
name = st.text_input('Name')
if not name:
  st.warning('Please input a name.')
  st.stop()
st.success('Thank you for inputting a name.')