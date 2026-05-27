import streamlit as st

def apply_style(page_name):
    """
    Central style injector utility. 
    Call this on any page by passing the respective page identifier string.
    """
    
    # 1. STYLE SHEET REPOSITORY, Dito nakalagay lahat ng CSS stylesheets para sa bawat page, organized by page name keys, wrok here now - PixelatedCorn
    sheets = {
        #For Login Page
        "login": """
        <style>
        @import url('https://googleapis.com');

        html, body, [class*="css"] { 
        font-family: sans-serif; 
        }

        .stApp { 
        background-color: white; 
        }

        .block-container {
        padding-top: 2rem; 
        }

        .main-title {
            text-align: center; 
            font-size: 70px; 
            font-weight: 800;
            color: #1E3A5F !important; 
            margin-bottom: 5px; 
            font-family: 'Poppins', sans-serif;
        }

        .sub-title { 
            text-align: center;
            color: #5c6b7a; 
            margin-bottom: 40px; 
            font-size: 16px; 
        }

        div[data-testid="stForm"] {
            background-color: #1E3A5F;
            padding: 40px;
            border-radius: 25px;
            box-shadow: 0px 5px 20px rgba(0,0,0,0.12);
            max-width: 500px;
            margin: auto;
        }

        div[data-testid="stForm"] label { 
        color: white !important; 
        }

        .stTextInput input {
            border-radius: 12px; 
            border: 1px solid #cfd9e6; 
            padding: 10px;
            background-color: white !important; 
            color: black !important;
        }

        label, .stTextInput label { 
            color: #1E3A5F !important; 
            font-family: sans-serif; 
            font-weight: 600; 
        }

        .stButton button {
            background-color: #1E3A5F; 
            color: white; 
            border-radius: 12px;
            border: none; 
            padding: 12px; 
            font-weight: 600; 
            font-size: 15px;
        }

        .stButton button:hover { 
        background-color: #27496d; 
        color: white; 
        }

        .footer-text { text-align: center; 
        color: #5c6b7a; 
        margin-top: 30px; 
        font-size: 13px; }
        </style>
        """,
        
        # for Home Page
        "home": """
        <style>
        .stApp { 
        background-color: #f4f8fc; 
        }
    
        h1 { 
        color: #1E3A5F; font-family: 
        'Poppins', sans-serif; 
        }

        /* TEXT INPUT + SELECTBOX LABELS ONLY */
        .stTextInput label p,
        .stSelectbox label p {
            font-size: 20px !important;
            font-weight: 800 !important;
            color: #1E3A5F !important;
        }
        label p {
            font-weight: 800 !important;
        }


        .header-row { 
            background-color: #1E3A5F; 
            padding: 14px 15px; 
            border-radius: 12px 12px 0 0; 
            color: white; 
            font-weight: 600; 
            border-bottom: 2px solid #dce6f2;
        }

        div[data-testid="stHorizontalBlock"] {
            align-items: center;
            padding-top: 2px;
            padding-bottom: 2px;
        }

        .stButton button { 
            background-color: #1E3A5F; 
            color: white; 
            border-radius: 10px; 
            border: none; 
            font-weight: 600; 
        }

        .stButton button:hover { 
            background-color: #27496d; 
            color: white; 
        }

        /* REMOVE TOP SPACE */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }

        /* OPTIONAL: bawasan pa */
        div[data-testid="stAppViewContainer"] {
            padding-top: 0rem !important;
        }

        /* INPUT CONTAINER */
        .stTextInput div[data-baseweb="input"] {
            border: 2px solid black !important;
            border-radius: 12px !important;
            background: transparent !important;
            min-height: 55px !important;
        }

        /* SELECTBOX */
        .stSelectbox div[data-baseweb="select"] {
            border: 2px solid black !important;
            border-radius: 12px !important;
            background: transparent !important;
            min-height: 55px !important;
            align-items: center !important;
        }

        .stSelectbox input {
            opacity: 0 !important;
            position: absolute !important;
        }

        /* INPUT TEXT */
        .stTextInput input {
            font-size: 18px !important;
            font-weight: 600 !important;
            background: transparent !important;
        }

        </style>
        """,

        #for Profile Page
        "profile": """
        <style>
        .stApp { background-color: #f4f8fc; }

        .info-section {
        border-bottom: 1px solid #c7d3e0;
        margin-bottom: 15px;
        padding-bottom: 10px;
        }

        h1, h2, h3 { 
        color: #1E3A5F; 
        font-family: 'Poppins', 
        sans-serif; 
        }

        .stTextInput input, .stTextArea textarea, .stDateInput input, .stSelectbox div[data-baseweb="select"] { 
        border-radius: 10px; 
        }

        .stFormSubmitButton button {
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 12px !important;
            transition: background-color 0.2s ease-in-out !important;
        }

        .stFormSubmitButton button:has(p:contains("Cancel")),
        .stFormSubmitButton button:contains("Cancel") {
            background-color: #D32F2F !important; /* Bold Crimson Red */
        }

        .stFormSubmitButton button:has(p:contains("Cancel")):hover,
        .stFormSubmitButton button:contains("Cancel"):hover {
            background-color: #9A1F1F !important; /* Dark Red hover */
        }

        .stFormSubmitButton button:has(p:contains("Save")),
        .stFormSubmitButton button:contains("Save") {
            background-color: #2E7D32 !important; /* Bold Emerald Green */
        }
        
        .stFormSubmitButton button:has(p:contains("Save")):hover,
        .stFormSubmitButton button:contains("Save"):hover {
            background-color: #1B5E20 !important; /* Dark Green hover */
        }



        .stDownloadButton button { 
        background-color: #fa00af !important; 
        color: white !important; 
        border-radius: 10px !important; 
        border: none !important; 
        font-weight: 600 !important; 
        }

        .stAlert { 
        border-radius: 12px; 
        }

        .section-title{
        color:#163B65;
        font-size:20px;
        font-weight:700;
        margin-bottom:15px;
        }
        </style>
        """,
        
        #for Accounts Page
        "accounts": """
        <style>

        .page-title { 
        font-size: 34px; 
        font-weight: 700; 
        color: #1E3A5F; 
        margin-bottom: 25px; 
        font-family: 'Poppins', sans-serif; 
        }

        .stTextInput input { 
        border-radius: 12px; 
        border: 1px solid #cfd9e6; 
        padding: 10px; 
        background-color: white; 
        }

        .stButton button { 
        background-color: #1E3A5F; 
        color: white; 
        border: none; 
        border-radius: 12px; 
        font-weight: 600; 
        padding: 10px; 
        transition: 0.2s; 
        }

        .stButton button:hover { 
        background-color: #27496d; 
        color: white; 
        }

        [data-testid="stDataFrame"] { 
        border-radius: 18px; 
        overflow: hidden; 
        border: 1px solid #dce6f2; 
        box-shadow: 0px 4px 15px rgba(0,0,0,0.05); 
        background: white; padding: 5px; 
        }

        .stApp { 
        background-color: #f5f9ff; 
        }

        label, p, div { 
        font-family: sans-serif; 
        }

        h1, h2, h3 { font-family: 'Poppins', sans-serif; }
        </style>
        """,

        #for Reports Page
        "reports": """
        <style>
        @import url('https://googleapis.com');

        .stApp { 
        background-color: #f4f8fd; 
        font-family: sans-serif; 
        }

        .block-container { 
        padding-top: 2rem; 
        }

        h1 { 
        color: #163B65; 
        font-family: 'Poppins', sans-serif; 
        font-weight: 700; 
        font-size: 42px; 
        }

        h2, h3 { 
        color: #163B65; 
        font-family: 'Poppins', sans-serif; 
        font-weight: 600; 
        }

        p, label, div { 
        font-family: sans-serif; 
        }

        [data-testid="metric-container"] { 
        background: white; 
        border-radius: 22px; 
        padding: 20px; 
        border: 1px solid #dbe7f3; 
        box-shadow: 0px 4px 18px rgba(0,0,0,0.06); 
        }

        [data-testid="metric-container"] label { 
        color: #5c6b7a; 
        font-size: 14px; 
        }

        [data-testid="metric-container"] [data-testid="stMetricValue"] { 
        color: #163B65; 
        font-family: 'Poppins', sans-serif; 
        font-weight: 700; 
        }

        .element-container:has(canvas) { 
        background: white; 
        border-radius: 22px; 
        padding: 20px; 
        box-shadow: 0px 4px 18px rgba(0,0,0,0.06); 
        border: 1px solid #dbe7f3; 
        margin-bottom: 20px; 
        }

        [data-testid="stDataFrame"] { 
        background: white; 
        border-radius: 20px; 
        overflow: hidden; 
        border: 1px solid #dbe7f3; 
        box-shadow: 0px 4px 18px rgba(0,0,0,0.05); 
        padding: 8px; 
        }

        .stSelectbox > div > div { 
        border-radius: 12px; 
        }

        .stDownloadButton button { 
        background-color: #163B65; 
        color: white; 
        border: none; 
        border-radius: 14px; 
        padding: 12px; 
        font-weight: 600; 
        transition: 0.2s; 
        }

        .stDownloadButton button:hover { 
        background-color: #245082; 
        color: white; 
        }

        hr { 
        border: none; 
        height: 1px; 
        background-color: #dce6f2; 
        margin-top: 25px; 
        margin-bottom: 25px; 
        }

        </style>
        """
    }

    if page_name in sheets:
        st.markdown(sheets[page_name], unsafe_allow_html=True)
