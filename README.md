PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION

Introduction:
1.PhonePe Pulse is a data visualization and exploration tool offered by PhonePe, a digital payments platform in India. It is designed to provide insights and analytics on various aspects of digital transactions processed through the PhonePe platform. 
2.We create a web app to analyse the Phonepe transaction and users depending on Years,Quarters,States and Type of transaction and also give a Geographical and Geo Visualization ouputs.

TOOLS:
1.VS Code
2.MYSQL
3.Python
4.Juphyter Notebook

PACKAGES:

import os
import pandas as pd
import json
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image

EXTRACT DATA
   We clon the data from Phonepe Github repositary by using python libraries

PROCESS
  1. We process the colned datas by using python codes and convert that datas into DataFrame format.
  2. Then create a connection to MYSQL server and create a tables for all needed datas.
  3. And fetch all SQL datas into DataFrame format for extract the relevant details
    
VISUALIZATION
     Finally, create a Dashboard by using Streamlit application and applying dropdown and sliders on the Dashboard and show the outputs on Chart and Geo visualization format.
  





