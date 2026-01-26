import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

st.title('大学卒業予定者の就職状況')

df = pd.read_csv('FEH_00400402_260126104754.csv')