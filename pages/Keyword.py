import streamlit as st
import difflib
from streamlit.components.v1 import html
from PIL import Image

logo = Image.open('images/logo.png')
st.set_page_config(
    page_title="Base",
    page_icon=logo,
    layout="wide",
)

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

nav_button = st.button("Go Back")
if nav_button:
     nav_page("Knowledge")
st.title(f"🔑 {st.session_state.button.capitalize()}")
st.subheader(" 🌐 Definition")
st.write(st.session_state.googlesearch)
st.write("\n")
st.subheader(f"✂️ Text Sections including {st.session_state.button.capitalize()}")

infoscrape = st.session_state.info_scrape

for paar in infoscrape:
    st.write("--------------")
    for sentence, count in zip(paar, range(0,len(paar))):
        if count == 1:
            length_keyword = len(st.session_state.button.split(" "))
            tokens = sentence.split(" ")
            tokens = [ ' '.join(x) for x in zip(tokens[0::length_keyword], tokens[1::length_keyword])]
            substring = difflib.get_close_matches(st.session_state.button, tokens,cutoff = 0.2, n=1)[0]
            sentence = sentence.replace(substring, f'<b style="color:Red; ">{substring}</b>')
            st.markdown(sentence, unsafe_allow_html=True)
        else:
            st.markdown(sentence)
