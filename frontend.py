import streamlit as st

def apply_style(page_name):
    """
    Central style injector utility. 
    Call this on any page by passing the respective page identifier string.
    """
    
    # ---------------------------------------------------------
    # 1. STYLE SHEET DICTIONARY MAP
    # ---------------------------------------------------------
    sheets = {
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
            font-size: 42px; 
            font-weight: 700;
            color: #1E3A5F; 
            margin-bottom: 5px; 
            font-family: 'Poppins', sans-serif;
        }

        .sub-title { 
            text-align: center;
            color: #5c6b7a; 
            margin-bottom: 40px; 
            font-size: 16px; 
        }

        .login-card {
            background: #1E3A5F; 
            padding: 40px; 
            border-radius: 20px;
            box-shadow: 0px 5px 20px rgba(0,0,0,0.12); 
            border: 1px solid #dce6f2;
        }

        div[data-testid="stForm"] {
            background-color: #1E3A5F; 
            padding: 30px; 
            border-radius: 20px;
            box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
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

        h3 { 
        color: white; 
        font-family: 'Poppins', sans-serif; 
        }

        .stCaption { 
        color: #dbe7f5 !important; 
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
        margin-top: 30px; f
        font-size: 13px; }
        </style>
        """,
        
        "home": """
        <style>
        .stApp { 
        background-color: #f4f8fc; 
        }
    
        h1 { 
        color: #1E3A5F; font-family: 
        'Poppins', sans-serif; 
        }

        .stTextInput input, .stSelectbox div[data-baseweb="select"] { 
        border-radius: 10px; 
        }

        .header-row { 
        background-color: #1E3A5F; 
        padding: 12px 15px; 
        border-radius: 12px; 
        color: white; 
        font-weight: 600; 
        margin-bottom: 10px; 
        }

        .resident-row { 
        background-color: white; 
        padding: 12px 15px; 
        border-radius: 12px; 
        margin-bottom: 10px; 
        box-shadow: 0px 2px 8px rgba(0,0,0,0.05); 
        border-left: 5px solid #1E3A5F; 
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

        </style>
        """,
        
        "profile": """
        <style>
        .stApp { background-color: #f4f8fc; }

        h1, h2, h3 { 
        color: #1E3A5F; 
        font-family: 'Poppins', 
        sans-serif; 
        }

        .section-card { 
        background-color: white; 
        padding: 25px; 
        border-radius: 18px; 
        margin-bottom: 20px; 
        box-shadow: 0px 3px 12px rgba(0,0,0,0.05); 
        border-left: 5px solid #1E3A5F; 
        }

        .stTextInput input, .stTextArea textarea, .stDateInput input, .stSelectbox div[data-baseweb="select"] { 
        border-radius: 10px; 
        }

        .stButton button { 
        background-color: #9500ff; 
        color: white; 
        border-radius: 10px; 
        border: none; 
        font-weight: 600; 
        }

        .stDownloadButton button { 
        background-color: #fa00af !important; 
        color: white !important; 
        border-radius: 10px !important; 
        border: none !important; 
        font-weight: 600 !important; 
        }

        .st-key-btn1 button { 
        background-color: #F44336; 
        color: white; 
        border-radius: 10px; 
        border: none; 
        font-weight: 600; 
        }

        .stFormSubmitButton button { 
        background-color: #fa00af; 
        color: white; 
        border-radius: 10px; 
        border: none; 
        font-weight: 600; 
        }

        .stButton button:hover, .stDownloadButton button:hover, .stFormSubmitButton button:hover { 
        background-color: #27496d; 
        color: white; 
        }

        .stAlert { 
        border-radius: 12px; 
        }

        </style>
        """,
        
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
        box-shadow: 0px 4px 18px rgba(0,0,0,0.06); }

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

    # --------------------------------------------------------
    # 2. RUN INJECTION SAFELY
    # ---------------------------------------------------------
    if page_name in sheets:
        st.markdown(sheets[page_name], unsafe_allow_html=True)
