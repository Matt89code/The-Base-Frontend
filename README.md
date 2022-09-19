# The-Base-Frontend

## Project Description

This project file provides the front end of the project The-Base-Backend project. 

Using Streamlit and Heruko. 

Written in Python. Except a block of code in Javascript for ease of navigation between pages.


## Navigation of Project

../pages/

![image](https://user-images.githubusercontent.com/108887806/191027467-613c7e7b-92eb-48bb-a17f-fb9d19936e37.png)


## BASE.py

The block of java script is within 

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

