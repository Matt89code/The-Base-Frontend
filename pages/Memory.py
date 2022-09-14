import streamlit as st
from streamlit.components.v1 import html
from google.cloud import bigquery
from google.oauth2 import service_account
import json
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





nav_button = st.button("🌐 General Network")
if nav_button:
    nav_page("general_network")


def retrieve_data_from_gcl(username):
    # loading credentials
    client = bigquery.Client(credentials=credentials,project=project_id)
    sql_query = f"""
    SELECT * FROM `lewagon-project-356008.user_infos.input_storage`
    WHERE USER_ID = "{username}"
    """

    phi = client.query(sql_query)
    phi.result()
    results = []
    n_list = []
    for i in phi.result():
        results.append(i)

    length = len(results)

    user_id_list = []
    for x in results:
        user_id_list.append(x[7])











    return results, length, user_id_list
# user_rows = retrieve_data_from_gcl(st.session_state)[0]
# row_len = retrieve_data_from_gcl()[1]
# user_id_list = retrieve_data_from_gcl()[2]
username = st.session_state.username
user_rows, row_len, user_id_list = retrieve_data_from_gcl(username)

newinfo_button  = st.button("🆕 Information")
if newinfo_button:
    nav_page("Information")

st.write("---------------")

st.markdown("# 🧠 Memory")
row_list = []
for i in user_rows:



    knowledge_button = st.button(i[8])

    row_list.append(i)
    if knowledge_button:
        for x in row_list:
            user_text_db = x[1]
            summary_db = x[2]
            keyword_db = json.loads(x[3])
            topic = json.loads(x[4])
            hierachy_db = json.loads(x[5])
            user_title = x[8]
            st.session_state["user_title"]  = user_title
            st.session_state["status"] = "DB_call"
            st.session_state["user_text_db"] = user_text_db
            st.session_state["summary_db"] = summary_db
            st.session_state["keyword_db"] = keyword_db
            st.session_state["topic"] = topic[0]
            st.session_state["hierachy_db"] = hierachy_db
            nav_page("Knowledge")
