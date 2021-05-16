import re
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import streamlit as st

from PIL import Image

from utility.colormaps import colormaps

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




st.title("WordCloud Titel")
st.write("Vælg population")


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



koen = st.sidebar.multiselect("Køn",['Mand','Kvinde'], default = ['Mand','Kvinde'] )
col_koen = 'Hvad er dit køn?'








landsdel = ['Nordsjælland', 'Nordjylland', 'Østjylland', 'Sydjylland',
       'Vest- og sydsjælland', 'København by', 'Københavns omegn',
       'Sydhavsøerne', 'Vestjylland', 'Bornholm', 'Østsjælland', 'Fyn']

landsdel_selected = st.sidebar.multiselect("Landsdel",options = landsdel, default = landsdel )

col_geo ='Hvilken landsdel kommer du fra?'



col_alder = 'Hvilken aldersgruppe tilhører du?'
aldersgrupper = [ '71+ år', '41-50 år', '61-70 år', '31-40 år', '17-20 år',
       '21-30 år', '51-60 år', '13-16 år']

alder_sel = st.sidebar.multiselect("Landsdel",options = aldersgrupper, default = aldersgrupper )



col_udd = 'Højest fuldførte uddannelse'
udd = [ 
'Grundskole (folkeskole, friskole, hjemmeskole, privatskole)',
'10. klasse' ,
'Gymnasial uddannelse (STX, HHX, HTX, HF)',
'Erhvervsuddannelse',
'Kort videregående uddannelse',
'Mellemlang videregående uddannelse',
'Lang videregående uddannelse']

udd_sel = st.sidebar.multiselect("Uddannelse",options = udd, default = udd )



df_kender = df[(df[col_hvor_ofte].isin(kender_ordet)) & (df[col_koen].isin(koen))  & (df[col_udd].isin(udd_sel))    & (df[col_geo].isin(landsdel_selected))     & (df[col_alder].isin(alder_sel))          ]
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


antal_ord = st.sidebar.number_input("Vælg antallet af ord",min_value = 1, value = 100, step = 1, format ="%i" )





color = st.sidebar.selectbox("Vælg farvetema", options = colormaps)

baggrundsfarve = st.sidebar.color_picker("vælg baggrundsfarve")

################################################
#
#
# Plot Wordcloud
#
#
################################################




wordcloud = WordCloud( stopwords = stopwords, max_words=antal_ord, background_color=baggrundsfarve, colormap=color,mask = mask, contour_width=0, contour_color='grey').generate(text)
fig = plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot(fig, figsize=(8, 5))

st.sidebar.write("Antal Svar:" + str(len(df_sub))  )







    ###############################################################################
    #
    # Layout
    #
    ###############################################################################

st.title('Fordelingen af antal svar')




filter_hist = st.selectbox("Vælg Filter",options = [col_koen,col_geo,col_alder])

df_nonan = df[df[col_hvor_ofte].notnull()]

fig1 = px.histogram(df_nonan, x=filter_hist, color = col_hvor_ofte )
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

st.plotly_chart(fig1)

    

