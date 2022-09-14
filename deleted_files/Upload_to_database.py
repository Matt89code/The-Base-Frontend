# import streamlit_authenticator as stauth
# import Database as db

# USER_ID = [1,2]
# usernames = ["mjackson","jbond"]
# names = ["mickael jackson", "james bond"]
# passwords = ["67890","12345"]

# hashed_passwords = stauth.Hasher(passwords).generate()

# # upload_list = [{'USER_ID':user_id, 'username': username, 'name': name, 'password': hashed_password} for user_id, username, name, hashed_password in zip(USER_ID,usernames, names, hashed_passwords)]
# upload_list = [{'USER_ID':user_id, 'username': username, 'name': name, 'password': password} for user_id, username, name, password in zip(USER_ID, usernames, names, passwords)]

# db.insert_user(upload_list)
