import streamlit as st
from streamlit_observable import observable

observers = observable("County Brush", 
    notebook="d/4f9aa5feff9761c9",
    targets=["viewof fipscodes"], 
    observe=["selectedCounties"]
)

selectedCounties = observers.get("selectedCounties")