
# from google.cloud import bigquery
# from google.oauth2 import service_account

# project_id = 'lewagon-project-356008'

# credentials = service_account.Credentials.from_service_account_file('google_credential.json')
# client = bigquery. Client(credentials= credentials,project=project_id)

# # dataset_id = 'user_infos'
# table_id = 'lewagon-project-356008.user_infos.user'

# def insert_user(upload_list):

#     insert = client.insert_rows_json(table_id, upload_list)

#     return insert

# def fetch_all_users():

#     query_job = client.query("""
#     SELECT *
#     FROM user_infos.user
#     LIMIT 1000 """)

#     results = query_job.result()
#     results = results.to_dataframe

#     return results()

# def get_user(username):

#     query_job = client.query("""
#     SELECT f
#     FROM user_infos.user
#     LIMIT 1000 """)

#     results = query_job.result()

#     return resultss
