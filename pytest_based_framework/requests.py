#from urllib import response
import requests
import random
import time

class https_request:
    def __init__(self):
       self.url="https://crudcrud.com/api/595e46b405d7429c918929a41c4581b4/unicorns"
       self.headers = {
            'Content-Type': 'application/json'
        }

    def post(self,payload):   
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        return response
   
    def get(self, id=''):   
        response = requests.request("GET", self.url+"/"+str(id), headers=self.headers)
        return response

    def put(self, id, payload): 
        response = requests.request("PUT", self.url+"/"+str(id), headers=self.headers, data = payload)
        return response

    def delete(self, id):   
        response = requests.request("DELETE", self.url+"/"+str(id), headers=self.headers)
        return response
            
    def generateRequestPayload(self, range_start=1, range_end=100):
        return {
        "timestamp": int(time.time()),
        "number": random.randint(range_start, range_end)
        }    
   
