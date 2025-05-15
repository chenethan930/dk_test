from openai import OpenAI
import streamlit as st
import base64
import requests
import time
import json
import random
import openai

client = OpenAI(
    api_key = st.secrets["api_key"],
)

prompt = """
Generate an image with the given style in the first input image. The output image should be in Chinese figure painting, characterized by fine brushwork, delicate lines, and a focus on traditional attire and formal composition. The style emphasizes meticulous detail and symbolic representation, hallmarks of the gongbi technique in traditional Chinese art
The person in the output image should look like the second input image, including their facial features. However, the person in output image should always wear a traditional Chinese robe, it's a deep blue robe with wide sleeves, and a broad, black sash draped diagonally across the chest. Underneath, a white inner garment with a visible collar is worn. This attire reflects the formal, dignified clothing of a traditional Chinese official, it also features a tall, angular black hat with distinct folds.
In addition, the person should not make any gestures and poses, but facial features are allowed (e.g. making faces, blinking, smiling). If the person is female and has long hair, you should make her have an updo in a tradition Chinese style. If the person has bangs, you should make her bangs wispy in a tradintional Chinese style. If the person is smiling, make sure they smile without showing teeth. Make sure the person look young and slim, and try to make their skin in good condition. Make the background green.
"""

st.header("Ancient Me_v3")
with st.form("my_form"):
    uploaded_file = st.file_uploader("Choose a file", type=["jpeg", "png", "jpg"])
    submitted = st.form_submit_button("Generate")

if submitted:

    col1, col2 = st.columns(2)

    bytes_data = uploaded_file.getvalue()
    base64_encoded_str = base64.b64encode(bytes_data).decode('utf-8')

    with col1:
        st.caption("Your Input")
        st.image(uploaded_file)

  
    try:
        while True:
            with col2:
                with st.spinner("Generating...", show_time=True):
                    start = time.time()
                    result = client.images.edit(
                        model="gpt-image-1",
                        image=[
                            open("poet2.png", "rb"),
                            uploaded_file
                        ],
                        size="1024x1536",
                        # size="1024x1024",
                        background="transparent",
                        quality="medium",
                        prompt=prompt
                    )

                    image_base64 = result.data[0].b64_json
                    image_bytes = base64.b64decode(image_base64)

                    end = time.time()
                    break

        with col2:
            st.caption("Your Output")
            st.image(image_bytes)

        length = end - start
        print("Time taken:", length, "seconds")
        print(result.usage)

    except openai.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.APIConnectionError as e:
        #Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        with col2:
            st.caption(f"現在有很多人在生圖，請稍後再試一次。")
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass
    