import requests

def join_server(token, server_invite):
    header = {"authorization": token}
    results = requests.post("https://discord.com/api/v10/invites/{}".format(server_invite), headers=header)
    print(results.content)

join_server("TOKEN_HERE", "ionetofficial")
