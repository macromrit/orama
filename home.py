import streamlit as st # the go-to UI framework
import google.generativeai as genai # for accessing gemini models
import PIL.Image # for processing images


st.set_page_config(
    page_title="όραμα",
    page_icon="🦅",
    layout="wide",
)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def get_response(image_path, query):
    try:
        img = PIL.Image.open(image_path)
        response = model.generate_content(
            [F"""{query}""",
            img], 
            stream=True,
            safety_settings=[
                            {"category":'HARM_CATEGORY_HARASSMENT',
                            "threshold":'block_none'},
                                {"category":'HARM_CATEGORY_DANGEROUS_CONTENT',
                                "threshold":'block_none'},
                                {"category":'HARM_CATEGORY_HATE_SPEECH',
                                "threshold":'block_none'}])
        
        response.resolve()
        
        return response.text
    except:
        return "You query seems harmful or something went wrong, try again"


def get_perception(image_path):
    try:
        img = PIL.Image.open(image_path)
        response = model.generate_content(img)
        return response.text
    except:
        return "Gemini's taking a bit of time, give it a moment and retry!"
    
def is_valid_key(api_key) -> bool:
    # testing valid api key
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        model.generate_content("Hello")
        return True
    except:
        return False


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

brdr1, col1, brdr2, col2, brdr3 = st.columns([1, 3, 1, 3, 1])

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

with col1:
    st.write('# όραμα 🦅')
    st.write("##### Got any queries about your image❓. Get them resolved then ✅")
    st.divider()
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# API key's being read from the api house

# get API key from the user as an input
with col1:
    GOOGLE_API_KEY = st.text_input('Input Enter Gemini\'s API key', placeholder='input the api-key generated')
    st.write("###### Get your API key from <a href='https://makersuite.google.com/app/apikey'>MakerSuite</a>", unsafe_allow_html=True)
    st.divider()



if not GOOGLE_API_KEY:
    with col1:
        st.info('Please Upload Gemini\'s API key, Which you generated', icon="ℹ️")    
    validity = None

else:
    validity = is_valid_key(GOOGLE_API_KEY)

if validity == False:
    with col1:
        st.error('Invalid API key Provided', icon="🚨")
if validity == True:
    with col1:
        st.success('API key accepted successfully', icon="✅")

with col1:
    st.divider()

# with open('GOOGLE_API_KEY.txt') as jammer:
#     GOOGLE_API_KEY  = jammer.read()

# activating the api to use models
genai.configure(api_key=GOOGLE_API_KEY)
# model being used - session_states to not reload on and on and on

model = genai.GenerativeModel('gemini-pro-vision')

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


with col1:
    uploaded_file = st.file_uploader("#### Upload an Image", accept_multiple_files=False, disabled=True if not validity else False)

# if not validity:
#     with col1:
#         st.divider()
#         st.warning('API key not uploaded.', icon="⚠️")

if not uploaded_file:
    with col1:
        st.divider()
        if not validity:
            st.warning(('API key not uploaded.' if validity == None else "Invalid API key uploaded.") + " Can't accept an image", icon="⚠️")
        else:
            st.info('Please Upload an Image of type jpg, png or jpeg', icon="ℹ️")
    
    with col2:
        llms_understanding = st.text_area(
        "#### Orama's understanding of the image fed",
        """Image not uploaded yet❗""",
        disabled=True,
        height = 100
    )
        
        st.write(f'No response generated ❗')
        
        st.divider()

    with col2:
        query = st.text_area(
    "#### Hit Orama with questions about the image uploaded",
    
    """Image not uploaded yet❗""",
    
    height = 200,

    disabled=True
    )

        st.write(f'No response generated ❗')

        st.divider()  
    

        llms_response = st.text_area(
    
    "#### Orama's Response",
    
    """Image not uploaded yet❗""",
    
    height = 200,
    
    disabled=True
    )

        st.write(f'No response generated ❗')

elif uploaded_file.name.split(".")[-1].casefold() not in ['jpg', 'png', 'jpeg']:
    with col2:
        st.warning('Please Upload an Image of type jpg, png or jpeg', icon="⚠️")
else:

    with open(F'images/output.{uploaded_file.name.split(".")[-1]}', 'wb') as jammer:
        jammer.write(uploaded_file.read())
    with col1:
        with st.expander("image uploaded", expanded=True):
            st.image(F'images/output.{uploaded_file.name.split(".")[-1]}', caption='Responses will be based on this image')


    with col2:
        llms_understanding = st.text_area(
    "#### Orama's understanding of the image fed",
    get_perception(F'images/output.{uploaded_file.name.split(".")[-1]}'),
    height = 100
    )

        st.write(f'LLM\'s perception is of {len(llms_understanding)} characters.')

        st.divider()



    with col2:
        query = st.text_area(
    "#### Hit Orama with questions about the image uploaded",
    
    """Hit the questions you want to, based on the image uploaded""",
    
    height = 200
    )

        st.write(f'You query is of {len(query)} characters.')

        st.divider()  
    

        llms_response = st.text_area(
    
    "#### Orama's Response",
    
    """No query received yet.""" if query == """Hit the questions you want to, based on the image uploaded""" else get_response(F'images/output.{uploaded_file.name.split(".")[-1]}', query),

    height = 200,
    )

        st.write(f'LLM\'s reponse is of {len(llms_response)} characters.')


# print(get_response(F'images/output.jpg', "does the young man look hot"))`
