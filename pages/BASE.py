import streamlit as st
from PIL import Image
from streamlit.components.v1 import html
import yaml
import streamlit_authenticator as stauth


def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)

col1, col2, col3 , col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

with col1:
    pass
with col2:
    pass
with col3:
    pass
with col4:
    pass
with col5:
    pass
with col6:
    pass
with col7:
    pass
with col8:
    pass
with col9:
    center_button = st.button("Sign in")
    if center_button:
        nav_page("Authentication")
with col10:
    center_button = st.button("Sign up")
    if center_button:
        nav_page("Registration")

image = Image.open('images/Base_Logo.png')
logo = Image.open('images/logo.png')

st.image(image)

st.markdown("<h1 style='text-align: center; color: #579DFF;'>Turning Information into Knowledge</h1>", unsafe_allow_html=True)
