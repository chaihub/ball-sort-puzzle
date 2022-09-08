"""git_graphql_example.py

Program to extract git data using the GitHub GraphQL API.
Using Python library python-graphql-client; for details see
https://pypi.org/project/python-graphql-client/

Usage: #TODO

Created by Chaitanya Rajguru 01-Aug-2022
"""

from python_graphql_client import GraphqlClient
import asyncio

#TODO: token privacy
headers = {"Authorization": "Bearer my_token"}
client = GraphqlClient(endpoint="https://github.whirlpool.com/api/graphql")

# Asynchronous request example
# query = """
#     query {
#         viewer {
#             login
#         }
#     }
# """
# result = asyncio.run(client.execute_async(query=query, headers=headers))
# print(result['data']['viewer']['login'])


#TODO: Move queries to a file; combine into a single query if possible
query_first_page = """
    query($first:Int!) {
        organization(login:"gpo-electronics-legacyMKS") {
            repositories(first: $first) {
                totalCount
                edges {
                    node {
                        name
                        isEmpty
                    }
                    cursor
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }
"""
query_subseq_page = """
    query($first:Int!, $after:String) {
        organization(login:"gpo-electronics-legacyMKS") {
            repositories(first: $first, after: $after) {
                totalCount
                edges {
                    node {
                        name
                        isEmpty
                    }
                    cursor
                }
                pageInfo {
                    endCursor
                    hasNextPage
                }
            }
        }
    }
"""
page_size = 100
has_next_page = True
after = ''
initial_query = True
result = {}
repo_list = []

while has_next_page:
    if initial_query:
        vars = {'first': page_size}
        result = asyncio.run(client.execute_async(query=query_first_page, variables=vars, headers=headers))
        initial_query = False
    else:
        vars = {'first': page_size, 'after': after}
        result = asyncio.run(client.execute_async(query=query_subseq_page, variables=vars, headers=headers))

    if 'data' not in result or 'errors' in result:
        break

    after = result['data']['organization']['repositories']['pageInfo']['endCursor']
    has_next_page = result['data']['organization']['repositories']['pageInfo']['hasNextPage']
    for edge in result['data']['organization']['repositories']['edges']:
        repo_list.append([edge['node']['name'], edge['node']['isEmpty']])

with open('oldrepos.txt', 'w', encoding="utf-8") as outfile:
    outfile.write(f'Found {len(repo_list)} repositories\n')
    for _r in repo_list:
        outfile.write(f'{_r[0]} {str(_r[1])}\n')