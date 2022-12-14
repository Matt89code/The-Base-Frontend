import streamlit as st
import requests
import streamlit.components.v1 as components
import networkx as nx
from pyvis.network import Network
import pandas as pd
import graphviz as graphviz
from streamlit.components.v1 import html
from PIL import Image
import json
from google.cloud import bigquery
from google.oauth2 import service_account

logo = Image.open('images/logo.png')
st.set_page_config(
    page_title="Base",
    page_icon=logo,
    layout="wide",
)

def googlesearch_api(user_input):
    #API Request - Youtube
    response = requests.get(
    'https://baseapi-qsjgkov3gq-ew.a.run.app/googlesearch',
    params={'word': user_input}).json()
    return response

def info_source(keyword, user_text):
    response = requests.get(
    'https://baseapi-qsjgkov3gq-ew.a.run.app/keyword_source_info',
    params={'keyword': keyword,
            'text': user_text}).json()
    return response

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

def new_info():
    if st.session_state['status'] == "Running":
        nav_button = st.button("???? Memory")
        if nav_button:
            nav_page("Memory")
        st.markdown(f"# ?????? {st.session_state.user_title}")
        st.write("\n")
        st.markdown("## Summary")
        summary = st.session_state.summary
        st.write(st.session_state.summary)
        st.markdown("## Keywords")
        keywords = st.session_state.keyword
        for word in keywords:
            button = st.button(word.capitalize())
            if button:
                googlesearch = googlesearch_api(word)
                user_text = st.session_state.user_text
                info_scrape = info_source(word, user_text)
                st.session_state['info_scrape'] = info_scrape
                st.session_state["googlesearch"] = googlesearch
                st.session_state["button"] = word
                nav_page("Keyword")

        keywords = st.session_state.keyword
        keyword_hierachy = st.session_state.keyword_hierachy

        # # #Get rid of doubles ('ai', 'computer science', 'computer science')
        # counter = 0
        # for yes in keyword_hierachy:
        #     if word[0] == word[1]:
        #         keyword_hierachy[counter].pop(0)
        #     counter +=1

        #delete duplicates (not error tested)
        none = 0
        counter_lists = 0
        new_hierachy = []
        for word in keyword_hierachy:
            counter_lists = 0
            current_hierachy = []
            counter = 0
            for key in word:
                try:
                    if word[counter-1] == word[counter]:
                        none +=1
                    else:
                        current_hierachy.append(key)
                except:
                    none +=1
                counter += 1
            new_hierachy.append(current_hierachy)
            counter_lists +=1

        keyword_hierachy = new_hierachy



        #Network(notebook=True)
        st.markdown('## Knowledge Network')
        physics=st.sidebar.checkbox('add physics interactivity?')
        def simple_func(physics):
            #initialize graph
            nx_graph = nx.cycle_graph(0)
            # Layer 1
            none = 0
            counter_nodes = 1
            topic = False
            info_nodes = {}
            double = False
            sizes = {1:45, 2: 35, 3:30, 4:25, 5:15, 6:10, 7:5}
            for keyword in keyword_hierachy:
                double = False
                counter_layers = 1
                for word in keyword:
                    if double:
                        if word not in info_nodes.keys():
                            group = info_nodes[word_double][1]
                            node = info_nodes[word_double][0]
                            nx_graph.add_node(counter_nodes, size=sizes[group+1], label=word, title=word, group=group+1)
                            nx_graph.add_edge(node, counter_nodes, weight=10)
                            double = False
                            counter_nodes+=1
                            counter_layers = group+2
                        double = False
                    else:
                        if counter_layers == 1:
                            if not topic:
                                nx_graph.add_node(counter_nodes, size=45, label=word, title=word, group=1)
                                topic = True
                                counter_nodes += 1
                        elif counter_layers == 2:
                            if word in info_nodes.keys():
                                double = True
                                word_double = word
                            else:
                                nx_graph.add_node(counter_nodes, size=35, label=word, title=word, group=2)
                                try:
                                    nx_graph.add_edge(1, counter_nodes, weight=10)
                                except:
                                    none +=1
                                info_nodes[word] = (counter_nodes, counter_layers)
                                counter_nodes += 1
                        elif counter_layers == 3:
                            if word in info_nodes.keys():
                                double = True
                                word_double = word
                            else:
                                nx_graph.add_node(counter_nodes, size=30, label=word, title=word, group=3)
                                try:
                                    nx_graph.add_edge(counter_nodes-1, counter_nodes, weight=10)
                                except:
                                    none +=1
                                info_nodes[word] = (counter_nodes, counter_layers)
                                counter_nodes += 1
                        elif counter_layers == 4:
                            if word in info_nodes.keys():
                                double = True
                                word_double = word
                            else:
                                nx_graph.add_node(counter_nodes, size=25, label=word, title=word, group=4)
                                try:
                                    nx_graph.add_edge(counter_nodes-1, counter_nodes, weight=10)
                                except:
                                    none +=1
                                info_nodes[word] = (counter_nodes, counter_layers)
                                counter_nodes += 1
                        elif counter_layers == 5:
                            if word in info_nodes.keys():
                                double = True
                                word_double = word
                            else:
                                nx_graph.add_node(counter_nodes, size=15, label=word, title=word, group=5)
                                try:
                                    nx_graph.add_edge(counter_nodes-1, counter_nodes, weight=10)
                                except:
                                    none +=1
                                info_nodes[word] = (counter_nodes, counter_layers)
                                counter_nodes += 1
                        elif counter_layers == 6:
                            if word in info_nodes.keys():
                                double = True
                                word_double = word
                            else:
                                nx_graph.add_node(counter_nodes, size=10, label=word, title=word, group=6)
                                try:
                                    nx_graph.add_edge(counter_nodes-1, counter_nodes, weight=10)
                                except:
                                    none +=1
                                info_nodes[word] = (counter_nodes, counter_layers)
                                counter_nodes += 1
                        elif counter_layers == 7:
                            if word in info_nodes.keys():
                                double = True
                                word_double = word
                            else:
                                nx_graph.add_node(counter_nodes, size=5, label=word, title=word, group=7)
                                try:
                                    nx_graph.add_edge(counter_nodes-1, counter_nodes, weight=10)
                                except:
                                    none +=1
                                info_nodes[word] = (counter_nodes, counter_layers)
                                counter_nodes += 1

                        counter_layers +=1



            options = {
                "nodes":{
                    "font":{
                        "size": 20,
                        "bold":True
                    }
                },
                "edges":{
                    "color":'blue',
                    "smooth":False
                },
                "physics":{
                    "barnesHut":{
                        "gravitationalConstant":-500000,
                        "centralGravity":12,
                        "springLength": 50,
                        "springConstant": 0.7,
                        "damping": 3,
                        "avoidOverlap": 10
                    }
                },
                "interaction":{
                    "selectConnectedEdges": True,
                        "dragNodes": True,
                        "hideEdgesOnDrag": False,
                        "hideNodesOnDrag": False
        }}
            nt = Network("600px", "800px",notebook=True, heading="")
            nt.options = options
            nt.from_nx(nx_graph)
            #physics=st.sidebar.checkbox('add physics interactivity?')
            if physics:
                nt.show_buttons(filter_=['physics'])
            nt.show('test.html')
        simple_func(physics)
        HtmlFile = open("test.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        components.html(source_code, height = 1200,width=1200)


def db_info():
    nav_button = st.button("???? Memory")
    if nav_button:
        nav_page("Memory")
    st.markdown(f"# ?????? {st.session_state.user_title}")
    st.write("\n")
    st.markdown("## Summary")
    summary = st.session_state.summary_db
    st.write(st.session_state.summary_db)
    st.markdown("## Keywords")
    keywords = st.session_state.keyword_db
    for word in keywords:
        button = st.button(word.capitalize())
        if button:
            googlesearch = googlesearch_api(word)
            user_text = st.session_state.user_text_db
            info_scrape = info_source(word, user_text)
            st.session_state['info_scrape'] = info_scrape
            st.session_state["googlesearch"] = googlesearch
            st.session_state["button"] = word
            nav_page("Keyword")

    keywords = st.session_state.keyword_db
    keyword_hierachy = st.session_state.hierachy_db


        #Get rid of doubles ('ai', 'computer science', 'computer science')
    counter = 0
    for word in keyword_hierachy:
        if word[0] == word[1]:
            keyword_hierachy[counter].pop(0)
        counter +=1

    #Network(notebook=True)
    st.markdown('## Knowledge Network')
    physics=st.sidebar.checkbox('add physics interactivity?')
    def simple_func(physics):
        #initialize graph
        nx_graph = nx.cycle_graph(0)
        # Layer 1
        none = 0
        counter_nodes = 1
        topic = False
        info_nodes = {}
        double = False
        sizes = {1:45, 2: 35, 3:30, 4:25, 5:15, 6:10, 7:5}
        for keyword in keyword_hierachy:
            double = False
            counter_layers = 1
            for word in keyword:
                if double:
                    if word not in info_nodes.keys():
                        group = info_nodes[word_double][1]
                        node = info_nodes[word_double][0]
                        nx_graph.add_node(counter_nodes, size=sizes[group+1], label=word, title=word, group=group+1)
                        nx_graph.add_edge(node, counter_nodes, weight=10)
                        double = False
                        counter_nodes+=1
                        counter_layers = group+2
                    double = False
                else:
                    if counter_layers == 1:
                        if not topic:
                            nx_graph.add_node(counter_nodes, size=45, label=word, title=word, group=1)
                            topic = True
                            counter_nodes += 1
                    elif counter_layers == 2:
                        if word in info_nodes.keys():
                            double = True
                            word_double = word
                        else:
                            nx_graph.add_node(counter_nodes, size=35, label=word, title=word, group=2)
                            try:
                                nx_graph.add_edge(1, counter_nodes, weight=10)
                            except:
                                none +=1
                            info_nodes[word] = (counter_nodes, counter_layers)
                            counter_nodes += 1
                    elif counter_layers == 3:
                        if word in info_nodes.keys():
                            double = True
                            word_double = word
                        else:
                            nx_graph.add_node(counter_nodes, size=30, label=word, title=word, group=3)
                            try:
                                nx_graph.add_edge(counter_nodes-1, counter_nodes, weight=10)
                            except:
                                none +=1
                            info_nodes[word] = (counter_nodes, counter_layers)
                            counter_nodes += 1
                    elif counter_layers == 4:
                        if word in info_nodes.keys():
                            double = True
                            word_double = word
                        else:
                            nx_graph.add_node(counter_nodes, size=25, label=word, title=word, group=4)
                            try:
                                nx_graph.add_edge(counter_nodes-1, counter_nodes, weight=10)
                            except:
                                none +=1
                            info_nodes[word] = (counter_nodes, counter_layers)
                            counter_nodes += 1
                    elif counter_layers == 5:
                        if word in info_nodes.keys():
                            double = True
                            word_double = word
                        else:
                            nx_graph.add_node(counter_nodes, size=15, label=word, title=word, group=5)
                            try:
                                nx_graph.add_edge(counter_nodes-1, counter_nodes, weight=10)
                            except:
                                none +=1
                            info_nodes[word] = (counter_nodes, counter_layers)
                            counter_nodes += 1
                    elif counter_layers == 6:
                        if word in info_nodes.keys():
                            double = True
                            word_double = word
                        else:
                            nx_graph.add_node(counter_nodes, size=10, label=word, title=word, group=6)
                            try:
                                nx_graph.add_edge(counter_nodes-1, counter_nodes, weight=10)
                            except:
                                none +=1
                            info_nodes[word] = (counter_nodes, counter_layers)
                            counter_nodes += 1
                    elif counter_layers == 7:
                        if word in info_nodes.keys():
                            double = True
                            word_double = word
                        else:
                            nx_graph.add_node(counter_nodes, size=5, label=word, title=word, group=7)
                            try:
                                nx_graph.add_edge(counter_nodes-1, counter_nodes, weight=10)
                            except:
                                none +=1
                            info_nodes[word] = (counter_nodes, counter_layers)
                            counter_nodes += 1

                    counter_layers +=1



        options = {
            "nodes":{
                "font":{
                    "size": 20,
                    "bold":True
                }
            },
            "edges":{
                "color":'blue',
                "smooth":False
            },
            "physics":{
                "barnesHut":{
                    "gravitationalConstant":-500000,
                    "centralGravity":12,
                    "springLength": 50,
                    "springConstant": 0.7,
                    "damping": 3,
                    "avoidOverlap": 10
                }
            },
            "interaction":{
                "selectConnectedEdges": True,
                    "dragNodes": True,
                    "hideEdgesOnDrag": False,
                    "hideNodesOnDrag": False
    }}
        nt = Network("600px", "800px",notebook=True, heading="")
        nt.options = options
        nt.from_nx(nx_graph)
        #physics=st.sidebar.checkbox('add physics interactivity?')
        if physics:
            nt.show_buttons(filter_=['physics'])
        nt.show('test.html')
    simple_func(physics)
    HtmlFile = open("test.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height = 1200,width=1200)




def error():
    error_message = st.write("ERROR")
    return error_message

def main_page():

    if st.session_state['status'] == "DB_call":
        db_info()

    if st.session_state['status'] == "Running":
        new_info()

    else:
        error()


page_names_to_funcs = {
    f"{st.session_state.topic}": main_page
}

selected_page = st.sidebar.selectbox("Select a Topic", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

# test
