from time import sleep
from copy import deepcopy

from src.constants import default_server_resources_consumption, empty_resources
from src.enums import MODEL_STATES
from src.TritonHttpClient import TritonHttpClient
from src.utils import dict_values_gte, list_of_dicts_find, reversed_ordered_dedupe, validate_occupied_resoruces


class TritonLRUHttpClientSync:
    def __init__(self, url, model_requirements_map):
        self.triton_http_client = TritonHttpClient(url)
        self.model_requirements_map = model_requirements_map
        self.lru_model_ids = self._get_loaded_models()
        
        print("TritonLRUHttpClientSync::init")
    
    def _get_loaded_models(self):
        model_repository_index = self.triton_http_client.get_model_repository_index()
        loaded_models = [model_dict['name'] for model_dict in model_repository_index if model_dict['state'] == MODEL_STATES.READY]
        return loaded_models

    def _compute_occupied_resources(self):
        print("TritonLRUHttpClientSync::_compute_occupied_resources")

        model_repository_index = self.triton_http_client.get_model_repository_index()

        occupied_resources = deepcopy(empty_resources)
        for model_dict in model_repository_index:
            if not model_dict['state'] == MODEL_STATES.READY:
                continue
            
            for resource_name in default_server_resources_consumption.keys():
                occupied_resources[resource_name] += self.model_requirements_map[model_dict['name']][resource_name]
        
        validate_occupied_resoruces(occupied_resources)

        print("  TritonLRUHttpClientSync::_compute_occupied_resources ---> ok")
        return occupied_resources
    
    def _compute_available_resources(self):
        print("TritonLRUHttpClientSync::_compute_available_resources")

        occupied_resources = self._compute_occupied_resources()
        
        available_resources = deepcopy(empty_resources)
        for resource_name in default_server_resources_consumption.keys():
            print(available_resources)
            print(occupied_resources)
            available_resources[resource_name] = 1.0 - occupied_resources[resource_name]
        
        print("  TritonLRUHttpClientSync::_compute_available_resources ---> ok")
        return available_resources
    
    def _unload_model_sync(self, model_id, max_poll_iterations=25, poll_interval=0.1):
        print("TritonLRUHttpClientSync::_unload_model_sync")

        self.triton_http_client.unload_model(model_id)

        current_poll_iteration = 0
        while current_poll_iteration < max_poll_iterations:
            print(f"  TritonLRUHttpClientSync::_unload_model_sync ---> poll iteration {current_poll_iteration}")
            if self._check_model_state(model_id, MODEL_STATES.UNAVAILABLE):
                print(f"    model unloaded")
                print(f"  TritonLRUHttpClientSync::_unload_model_sync ---> ok")
                return True
            
            print(f"    model is still loaded")
            sleep(poll_interval)
        
        print(f"  TritonLRUHttpClientSync::_unload_model_sync ---X model has not unloaded after {max_poll_iterations} of {poll_interval}s")
        return False
    
    def _unload_lru_model(self):
        print("TritonLRUHttpClientSync::_unload_lru_model")

        if len(self.lru_model_ids) == 0:
            print("  TritonLRUHttpClientSync::_unload_lru_model ---X lru_model_ids is len 0")
            return

        lru_model_id = self.lru_model_ids[0]
        self._unload_model_sync(lru_model_id)
        self.lru_model_ids.pop(0)
        print("  TritonLRUHttpClientSync::_unload_lru_model ---> ok")
    
    def _clear_required_resources(self, resource_requirements):
        print("TritonLRUHttpClientSync::_clear_required_resources")
        while not dict_values_gte(self._compute_available_resources(), resource_requirements):
            print("  TritonLRUHttpClientSync::_clear_required_resources ---> more resources required")
            self._unload_lru_model()
    
    def _check_model_state(self, model_id, target_model_state):
        print(f"TritonLRUHttpClientSync::_check_model_state")
        print(f"  TritonLRUHttpClientSync::_check_model_state ---> model_id = '{model_id}'")

        model_repository_index = self.triton_http_client.get_model_repository_index()
        
        model_dict = list_of_dicts_find(model_repository_index, 'name', model_id)
        if model_dict is None:
            print(f"  TritonLRUHttpClientSync::_check_model_state ---X model '{model_id}' does not exist in the repository index")
            return False
        
        print(f"  TritonLRUHttpClientSync::_check_model_state ---> model '{model_id}' is loaded")
        
        return model_dict['state'] == target_model_state
    
    def _check_and_load_model(self, model_id):
        print(f"TritonLRUHttpClientSync::_check_and_load_model")
        print(f"  TritonLRUHttpClientSync::_check_and_load_model ---> model_id = '{model_id}'")

        if self._check_model_state(model_id, MODEL_STATES.READY):
            print(f"  TritonLRUHttpClientSync::_check_and_load_model ---> model '{model_id}' is already loaded")
            return
        
        model_resource_requirements = self.model_requirements_map[model_id]
        
        print(f"  TritonLRUHttpClientSync::_check_and_load_model ---> _clear_required_resources")
        self._clear_required_resources(model_resource_requirements)
        
        print(f"  TritonLRUHttpClientSync::_check_and_load_model ---> triton_http_client.load_model")
        self.triton_http_client.load_model(model_id)

        print(f"  TritonLRUHttpClientSync::_check_and_load_model ---> ok")
    
    def get_available_models(self):
        print(f"TritonLRUHttpClientSync::get_available_models")

        model_repository_index = self.triton_http_client.get_model_repository_index()
        print(model_repository_index)
        available_models = [model_dict['name'] for model_dict in model_repository_index]

        print(f"  TritonLRUHttpClientSync::get_available_models ---> ok")
        print("")
        return available_models
    
    def infer(self, model_id):
        print(f"TritonLRUHttpClientSync::infer")
        print(f"  TritonLRUHttpClientSync::infer ---> model_id = {model_id}")

        print(f"  TritonLRUHttpClientSync::infer ---> _check_and_load_model")
        self._check_and_load_model(model_id)

        self.lru_model_ids.append(model_id)
        self.lru_model_ids = reversed_ordered_dedupe(self.lru_model_ids)
        print(f"  TritonLRUHttpClientSync::infer ---> update lru_model ids ok")
        
        print(f"  TritonLRUHttpClientSync::infer ---> triton_http_client.infer")
        inference_result = self.triton_http_client.infer(model_id)

        print(f"  TritonLRUHttpClientSync::infer ---> ok")
        print("")
        return inference_result
