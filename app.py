import re
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import streamlit as st
from PIL import Image


def _max_width_():
        max_width_str = f"max-width: 1000px;"
        st.markdown(
            f"""
        <style>
        .reportview-container .main .block-container{{
            {max_width_str}
        }}
        </style>    
        """,
            unsafe_allow_html=True,
        )

_max_width_()

################################################
#
#
# Initializing
#
#
################################################


mask = np.array(Image.open("masks/mask_bubble.png"))
df = pd.read_excel('randomWords.xlsx',sheet_name = 'Complete')




################################################
#
#
# Filter
#
#
################################################



words = [
"walkman",
"basseralle",
"nidsk",
"lurenkig/lurenkik",
"spølkum",
"gammelmodig",
"negerkys",
"dropskoger",]


ordet = st.sidebar.selectbox("Vælg Ord",options = words)
selected_ord = "'"+ ordet+ "'?" 







col_definer = "Hvordan vil du definere ordet " + selected_ord
col_hvor_ofte = "Hvor ofte bruger du ordet " + selected_ord



kender_ordet_list= [
'Jeg kender ordet, og bruger det en gang imellem',
'Jeg kender ordet, men bruger det ikke',
'Jeg kender ordet, og bruger det ofte',
'Jeg kender ikke ordet, og bruger det ikke',
np.NaN]



kender_ordet = st.multiselect("Hvor godt kender du ordet",kender_ordet_list, default = ['Jeg kender ordet, men bruger det ikke'] )

df_kender = df[(df[col_hvor_ofte].isin(kender_ordet))]
df_sub = df_kender[col_definer]
text = df_sub.str.cat(sep=' ').lower()


################################################
#
#
# STOPWORDFS
#
#
################################################




text_list_dub = text.split()
text_list = list( dict.fromkeys(text_list_dub) )
default_stop_list = list(set(["en", "og", "et", "det", "er", "den", "der", "af", "måske", "lidt", "eller"]) & set(text_list))
stopwords_selected = st.multiselect(
   'Fjern ord fra wordcloud',
   text_list,
   default=default_stop_list)


stopwords = set(STOPWORDS)
stopwords.update(stopwords_selected)




################################################
#
#
# Vælg Antal ord
#
#
################################################


antal_ord = st.sidebar.number_input("Vælg antallet af ord",min_value = 1, value = 10, step = 1, format ="%i" )





################################################
#
#
# Plot Wordcloud
#
#
################################################




wordcloud = WordCloud( stopwords = stopwords, max_words=antal_ord, background_color='rgb(246,246,246)', colormap='Set2',mask = mask, contour_width=1, contour_color='grey').generate(text)
fig = plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(fig, figsize=(8, 5))

st.sidebar.write("Antal Svar:" + str(len(df_sub))  )





df_nonan = df[df[col_hvor_ofte].notnull()]

fig1 = px.histogram(df_nonan, x=col_hvor_ofte, color = 'Hvilken aldersgruppe tilhører du?')
fig1['layout'].update(   
            #title = "Distribution of rates for SE home loan", 
            xaxis = dict( 
                automargin = True, 
                categoryorder = 'category ascending',
                ), 
            yaxis = dict(
                title = "Antal Svar"),
            legend = go.layout.Legend(
                    x=0.96,
                    y=0.99),
            margin = go.layout.Margin(
                t = 20 # top margin
                ),
            paper_bgcolor='rgb(246,246,246)',

            plot_bgcolor =  "rgba(0,0,0,0)",
            
            )

fig1.update_layout(width=1000,height=600)

    ###############################################################################
    #
    # Layout
    #
    ###############################################################################

st.title('Fordelingen af antal svar')

st.plotly_chart(fig1)

    

