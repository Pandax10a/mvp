

from uuid import uuid4
from flask import Flask, make_response, request
import dbhelpers as dh
import apihelpers as a
import json
import dbcreds as d
import requests


app = Flask(__name__)

@app.post('/api/client')
def new_client():

    salt = uuid4().hex
    valid_check=a.check_endpoint_info(request.json, ['username', 'email', 'password', 
    'api_key'])
    if(valid_check != None):
        return make_response(json.dumps(valid_check, default=str), 400)
    
    
    

    result = dh.run_statement('CALL new_client(?,?,?,?,?)', [request.json.get('username'), request.json.get('email'),
    request.json.get('password'), salt, request.json.get('api_key')])

    if(type(result) == list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

@app.post('/api/client-login')
def client_login():
    token = uuid4().hex
    is_valid=a.check_endpoint_info(request.json, ['email', 'password'])
    if(is_valid != None):
        return make_response(json.dumps(is_valid, default=str), 400)
    result = dh.run_statement('CALL client_login(?,?,?)', [request.json.get('email'),
    request.json.get('password'), token])
    if(type(result)==list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 400)

@app.post('/api/inventory')
def client_inventory():

    myrecipes=requests.get('https://api.guildwars2.com/v2/account/recipes', params={
        "access_token": "276AFC0E-F2CD-8B49-9349-F8A60015193379CDF517-3757-4F10-BB05-C5ED8FC493C4"
    })

    # my_inventory_coin =requests.get('https://api.guildwars2.com/v2/account/wallet', params={
    # "access_token": "276AFC0E-F2CD-8B49-9349-F8A60015193379CDF517-3757-4F10-BB05-C5ED8FC493C4"})

    # is_valid = a.check_endpoint_info(request.json, ['copper', 'recipes'])
    # if(is_valid != None):
    #     return make_response(json.dumps(is_valid, default=str), 400)

    for recipe in myrecipes.json()[:10]:
        result = dh.run_statement('CALL client_recipes(?)', [recipe])

    if(type(result)==list):
        return make_response(json.dumps(result, default=str), 200)
    else:
        return make_response(json.dumps(result, default=str), 401)    

myrecipes=requests.get('https://api.guildwars2.com/v2/account/recipes', params={
    "access_token": "276AFC0E-F2CD-8B49-9349-F8A60015193379CDF517-3757-4F10-BB05-C5ED8FC493C4"
})
# my10recipe = []
# my10recipe.append(myrecipes[1])
# for index, x in zip(range(1), myrecipes):
#     print(index, x.decode("utf-8"))

print(myrecipes.json()[:10])

    



if(d.production_mode == True):
    print("Running in Production Mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
    app.run(debug=True)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)