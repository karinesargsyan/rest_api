import json
from requests import request
import pytest
import allure
import pytest_check as check
from python_rest_api.pytest_based_framework.requests import https_request

request = https_request()

@allure.title("Post method check in condition of right payload")
def test_post_201():
    payload = request.generateRequestPayload()
    
    try:
        response = request.post(json.dumps(payload))
        responseBody = response.json()

        check.is_in("_id", responseBody, "_id for posted object was not created on server")
        check.equal(response.status_code,201, "Wrong status code returned")
        del responseBody['_id']
        check.equal(responseBody,payload, "Response's body is different from posted body")

    except ValueError as e:
        pytest.fail(e.args[0])
    
    
@allure.title("Post method check in condition of incorrect payload")
def test_post_500():
    payload = [1, 2]
    payload_id = {
        "_id": "001",
        "name": "Name1",
        "age": 32,
        "surname": "Surname1"
    }
    
    try:
        response = request.post(json.dumps(payload))
        check.equal(response.status_code, 500, "Wrong status code returned for paylod with wrong body")

        response_id = request.post(json.dumps(payload_id))
        check.equal(response_id.status_code, 500, "Wrong status code returned for payload with id")


    except ValueError as e:
        pytest.fail(e.args[0])    


@allure.title("Get method check in case of a correct payload")
def test_get_all_200():
    try:
        random_payload = request.generateRequestPayload()
        initial_response_size = len(request.get().json())
        random_payload["_id"] = request.post(json.dumps(random_payload)).json()["_id"]
        final_response = request.get()
        final_response_body = final_response.json()
        final_size = len(final_response_body)

        check.equal(final_response.status_code, 200, "Wrong response: status_code must be 200")
        check.equal(final_size, initial_response_size+1, "The random payload was not added")
        check.equal(final_response_body[final_size-1], random_payload, "Last gotten response body is not equal to expected body")
      
    except ValueError as e:
        pytest.fail(e.args[0]) 

@allure.title("Get method check in case of a correct payload and unique ID")
def test_get_id_200():
    try:
        random_payload = request.generateRequestPayload()
        random_payload["_id"] = request.post(json.dumps(random_payload)).json()["_id"]
        get_response = request.get(random_payload["_id"])        

        check.equal(get_response.status_code, 200, "Wrong response: status_code must be 200")
        check.equal(get_response.json(), random_payload, "Last gotten response body is not equal to expected body")
      
    except ValueError as e:
        pytest.fail(e.args[0]) 

@allure.title("Put method check in case of a correct payload")
def test_put_200():
    try:
        random_payload = request.generateRequestPayload()
        updated_payload = request.generateRequestPayload(101, 1000)

        post_response_id = request.post(json.dumps(random_payload)).json()["_id"]
        get_response_initial_size = len(request.get().json()) 
        put_response = request.put(post_response_id,json.dumps(updated_payload))  
        get_response_by_id = request.get(post_response_id).json() 
        get_response_all_size = len(request.get().json())
        updated_payload["_id"] = post_response_id

        check.equal(put_response.status_code, 200, "Wrong response: status_code must be 200")
        check.equal(get_response_all_size, get_response_initial_size, "PUT changed the size")
        check.equal(get_response_by_id, updated_payload, "Payload is not updated")
      
    except ValueError as e:
        pytest.fail(e.args[0]) 


@allure.title("Delete method check in case of a correct payload")
def test_del_200():
    try:
        random_payload = request.generateRequestPayload()
        
        post_response_id = request.post(json.dumps(random_payload)).json()["_id"]
        get_response_initial_size = len(request.get().json()) 
        delete_response = request.delete(post_response_id)  
        get_response_final_size = len(request.get().json()) 
        delete_response_by_deleted_id = request.delete(post_response_id)        

        check.equal(delete_response.status_code, 200, "Wrong response: status_code must be 200")
        check.equal(get_response_final_size, get_response_initial_size - 1, "The last posted paylod was not deleted")
        check.equal(delete_response_by_deleted_id.status_code, 404, "Access to deleted element")
      
    except ValueError as e:
        pytest.fail(e.args[0]) 

@allure.title("Defined to delete all added information from the server")
def clean_up_server():
    try:
        for i in request.get().json():
            request.delete(i["_id"])
             
    except ValueError as e:
        pytest.fail(e.args[0]) 
