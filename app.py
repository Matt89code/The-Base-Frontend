import streamlit as st
from PIL import Image
from streamlit.components.v1 import html


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



image = Image.open('images/Base_Logo.png')
logo = Image.open('images/logo.png')
st.set_page_config(
    page_title="Base",
    page_icon=logo,
    layout="wide",
)

st.image(image)
st.write("BASE 0.0.1 (Beta)")
st.write("-----------")
st.markdown("# How to use BASE:")
st.markdown("### 1. Open BASE on the Sidebar (close Sidebar) 🏠")
st.write("### 2. Click on SignUp and create a account 🔒")
st.write("### 3. Login 🔑")
st.write("### 4. Now you are ready 🎉")
