import streamlit as st
import base64
import csv
import requests

import pandas as pd

st.set_page_config(page_title="Rank Tracker",page_icon="📈",layout="wide"   )

st.title('Rank Tracker by Francis X')
st.header("Rank Tracker (Serpstack API Edition)")
st.markdown("DIM")
st.markdown(" X ")
st.markdown("2022")

form = st.form(key='rankTrackerForm')

serpstack_key = form.text_input("Input Serpstack API key",value="")



device = form.selectbox('Choose Device (Mobile/Tablet or Desktop)',('desktop','mobile','tablet'))
google_domain = form.text_input('Enter Google Domain (google.fr, google.de, ...)',value='google.com')


keywordQuery = form.text_input('Enter Keyword(s). If multiple, separate with a comma.',value=None)
domainQuery = form.text_input('Enter Domain(s). If multiple, separate with a comma.',value=None)


submit_button = form.form_submit_button(label='Submit')

if submit_button:

    if "," not in keywordQuery and "," not in domainQuery:

        serp_results = requests.get(f"http://api.serpstack.com/search?access_key={serpstack_key}&query={keywordQuery}&device={device}&google_domain={google_domain}&auto_location=1")
        position = "Either not ranking or >18"

        for every in serp_results.json()["organic_results"]:
            if domainQuery in every["domain"]:
                position = every["position"]
            else:
                pass
        
        if position == "Either not ranking or >18":
            output = st.write(f"{domainQuery} is either not ranking or >18 for {keywordQuery}")

        else:
            output = st.write(f"{domainQuery} ranks #{position} for the keyword '{keywordQuery}' on {device} on {google_domain}.")


    elif "," in keywordQuery and "," in domainQuery:

        df = pd.DataFrame()


        keywordQuery = keywordQuery.split(",")

        df['Keywords'] = keywordQuery
        df['Google Domain'] = google_domain
        df['Device'] = device

        domainQuery = domainQuery.split(",")

        progressBar = st.progress(len(domainQuery)*len(keywordQuery))
        progressCount = 0
        progressBar = progressBar.progress(progressCount/(len(domainQuery)*len(keywordQuery)))

        for domain in domainQuery:

            listPosition = []

            for keyword in keywordQuery:

                serp_results = requests.get(f"http://api.serpstack.com/search?access_key={serpstack_key}&query={keyword}&device={device}&google_domain={google_domain}&auto_location=1")
                position = "Either not ranking or >18"

                for result in serp_results.json()["organic_results"]:
                    if domain in result["domain"]:
                        position = result["position"]
                    else:
                        pass

                listPosition.append(str(position))
                print(position)
                print(listPosition)

                progressCount = progressCount + 1
                progressBar = progressBar.progress(progressCount/(len(domainQuery)*len(keywordQuery)))
            
            df[domain] = listPosition
        st.dataframe(df)


    elif "," not in keywordQuery and "," in domainQuery:

        df = pd.DataFrame()

        df['Keywords'] = keywordQuery
        df['Google Domain'] = google_domain
        df['Device'] = device

        domainQuery = domainQuery.split(",")

        progressBar = st.progress(len(domainQuery))
        progressCount = 0

        for domain in domainQuery:

            listPosition = []

            serp_results = requests.get(f"http://api.serpstack.com/search?access_key={serpstack_key}&query={keywordQuery}&device={device}&google_domain={google_domain}&auto_location=1")
            position = "Either not ranking or >18"

            for result in serp_results.json()["organic_results"]:
                if domain in result["domain"]:
                    position = result["position"]
                else:
                    pass

            listPosition.append(str(position))

            progressCount = progressCount + 1
            progressBar = progressBar.progress(progressCount/(len(domainQuery)))
            
            df[domain] = listPosition

        st.dataframe(df)

    elif "," in keywordQuery and "," not in domainQuery:

        df = pd.DataFrame()

        keywordQuery = keywordQuery.split(",")

        df['Keywords'] = keywordQuery
        df['Google Domain'] = google_domain
        df['Device'] = device

        listPosition = []

        progressBar = st.progress(len(keywordQuery))
        progressCount = 0

        for keyword in keywordQuery:

            serp_results = requests.get(f"http://api.serpstack.com/search?access_key={serpstack_key}&query={keyword}&device={device}&google_domain={google_domain}&auto_location=1")
            position = "Either not ranking or >18"

            for result in serp_results.json()["organic_results"]:
                if domainQuery in result["domain"]:
                    position = result["position"]
                else:
                    pass

            listPosition.append(str(position))

            progressCount = progressCount + 1
            progressBar = progressBar.progress(progressCount/(len(keywordQuery)));