import  streamlit as st

x = st.slider("select a value")
st.write(x,"squared is", x *x )