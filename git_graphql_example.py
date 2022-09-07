"""git_graphql_example.py

Program to extract git data using the GitHub GraphQL API.
Using Python library python-graphql-client; for details see
https://pypi.org/project/python-graphql-client/

Usage: #TODO

Created by Chaitanya Rajguru 01-Aug-2022
"""

from python_graphql_client import GraphqlClient
import asyncio

headers = {"Authorization": "Bearer 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"}
client = GraphqlClient(endpoint="https://github.whirlpool.com/api/graphql")

query = """
    query {
        viewer {
            login
        }
    }
"""

# Asynchronous request
result = asyncio.run(client.execute_async(query=query, headers=headers))

print(result['data']['viewer']['login'])


query_initial = """
    query($first:Int!) {
        organization(login:"gpo-electronics-legacy") {
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
query_subseq = """
    query($first:Int!, $after:String) {
        organization(login:"gpo-electronics-legacy") {
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
count = 0

while has_next_page:
    if initial_query:
        vars = {'first': page_size}
        result = asyncio.run(client.execute_async(query=query_initial, variables=vars, headers=headers))
        initial_query = False
    else:
        vars = {'first': page_size, 'after': after}
        result = asyncio.run(client.execute_async(query=query_subseq, variables=vars, headers=headers))

    if 'data' not in result or 'errors' in result:
        break

    after = result['data']['organization']['repositories']['pageInfo']['endCursor']
    has_next_page = result['data']['organization']['repositories']['pageInfo']['hasNextPage']
    count += len(result['data']['organization']['repositories']['edges'])

#TODO: Collect and print results
print(f'Found {count} repositories')