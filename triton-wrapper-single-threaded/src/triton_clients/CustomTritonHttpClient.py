from requests import Session


class TritonHttpClient:
    def __init__(self, url):
        self.base_url = "http://" + url
        self.requests_session = Session()
        
        print("Initialized TritonHttpClient")

    def get_model_repository_index(self):
        print("        TritonHttpClient::get_model_repository_index")

        endpoint = self.base_url + "/model-repository"
        response = self.requests_session.get(endpoint)

        if response.status_code != 200:
            print(f"          TritonHttpClient::get_model_repository_index ---X returned non-200 status code: {response.status_code}")
            raise ValueError("  TritonHttpClient::get_model_repository_index returned non-200 status code")
        
        response_data = response.json()
        model_repository_state = response_data['result']['model_repository_state']
    
        print("          TritonHttpClient::get_model_repository_index ---> ok")
        return model_repository_state
    
    def load_model(self, model_id):
        print("        TritonHttpClient::load_model")

        endpoint = self.base_url + "/load-model" + f"?modelId={model_id}"
        response = self.requests_session.post(endpoint)

        if response.status_code != 200:
            print(f"          TritonHttpClient::load_model ---X returned non-200 status code: {response.status_code}")
            raise ValueError("  TritonHttpClient::load_model returned non-200 status code")
        
        print("          TritonHttpClient::load_model ---> ok")
        return True

    def unload_model(self, model_id):
        print("        TritonHttpClient::unload_model")

        endpoint = self.base_url + "/unload-model" + f"?modelId={model_id}"
        response = self.requests_session.post(endpoint)

        if response.status_code != 200:
            print(f"          TritonHttpClient::unload_model ---X returned non-200 status code: {response.status_code}")
            raise ValueError("  TritonHttpClient::unload_model returned non-200 status code")
        
        print("          TritonHttpClient::unload_model ---> ok")
        return True

    def infer(self, model_id):
        print("          TritonHttpClient::infer")

        endpoint = self.base_url + "/infer" + f"?modelId={model_id}"
        response = self.requests_session.post(endpoint)

        if response.status_code != 200:
            print(f"          TritonHttpClient::infer ---X returned non-200 status code: {response.status_code}")
            raise ValueError("  TritonHttpClient::infer returned non-200 status code")
        
        print("          TritonHttpClient::infer ---> ok")
        return True
