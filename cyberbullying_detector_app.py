import streamlit as st
import pickle
import pandas as pd


final_model_path = './data/final_model_pipe.pkl'
final_model_pipe = pickle.load(open(final_model_path,'rb'))

def detect(text, sens_output):
    pred = final_model_pipe.predict_proba(pd.Series([text]))
    proba = pred[0][1] 		   # probability that comment_text is in toxic class
    thresh = 1 - sens_output   # invert so that high sensitivity has low threshold
    if   proba < thresh:
        comment_rating = f"non-toxic"
    elif proba >= thresh:
        comment_rating = f"TOXIC"
    return comment_rating


st.title("Cyberbullying Detector App")
comment_text = st.text_input("Input comment to check here", value="Welcome to the Cyberbullying Detector!")



sens_output = st.slider('Sensitivity: ', min_value=0.0, max_value=1.0, value=0.5, step=0.1)

### Sample comments to try
#You're a stupid idiot
#You are awesome and I love you
#I am a cereal killer!

### Updates automatically after any change
rating = detect(comment_text, sens_output)
st.write(rating)

### To update only after clicking button
#unhide_output = st.button('Check')
#if unhide_output:
#	rating = detect(comment_text, sens_output)
#	st.write(rating)

