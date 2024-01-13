from flask import Flask, request, render_template
import requests
import threading
app = Flask(__name__)

clid = '1172519095627960321'
secret = 'kLAx3iYIzL5Tge_sEo1hC6PhIHe1ZOIg'
url = 'http://localhost:8000/'
tkn = 'MTE3MjUxOTA5NTYyNzk2MDMyMQ.Gfw3Q1.xmlU2WlLas4dHSPMzVHNNmpzVqHszUjLXX9InY' 
def join(acc, guildid, id):
    headers = {
            "Authorization" : f"Bot {tkn}",
        }
    data = {
            "access_token": acc,
        }
    response = requests.put(f'https://discord.com/api/v9/guilds/{guildid}/members/{id}', headers=headers, json=data)
    print(response.text)
def main(accs, iddd):
    guildids = []
    with open("guilds.txt", 'r') as file:
        ids = file.read().splitlines()
        for id in ids:
            guildids.append(id)
    threads = []
    for guildid in guildids:
        thread = threading.Thread(target=join, args=(accs, guildid, iddd))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
def getuserid(accs):
    headers = {"Authorization": f"Bearer {accs}"}
    url = "https://discordapp.com/api/users/@me"
    r = requests.get(url, headers=headers)
    id = r.json()["id"]
    return id
@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'client_id': clid,
        'client_secret': secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': url,
        'scope': 'identify guilds.join',
    }
    response = requests.post('https://discord.com/api/oauth2/token', data=data)
    print(response.text)
    
    if response.status_code == 200:
        jsonn = response.json()
        accs = jsonn.get('access_token')
        print(accs)
        with open("accesstokens.txt", "a") as file:
            file.write(f'{accs}\n')
        id = getuserid(accs)
        main(accs, id)
    else:
        return f'Error{response.status_code}, {response.text}'

if __name__ == '__main__':
    app.run(port=8000, debug=True)
