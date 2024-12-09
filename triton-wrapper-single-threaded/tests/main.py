from random import choice as rand_choice

from tqdm import tqdm

from src.TritonLRUHttpClientSync import TritonLRUHttpClientSync


num_inference_tests = 1_000
triton_url = "localhost:8020"
model_requirements_map = {
    "bengali_iitd": {
        "cpu": 0.2499,
        "ram": 0.13,
        "gpu": 0.2499,
        "vram": 0.18
    },
    "hindi_iitd": {
        "cpu": 0.2499,
        "ram": 0.13,
        "gpu": 0.2499,
        "vram": 0.18
    },
    "kashmiri_iitd": {
        "cpu": 0.2499,
        "ram": 0.13,
        "gpu": 0.2499,
        "vram": 0.18
    },
    "konkani_iitd": {
        "cpu": 0.2499,
        "ram": 0.13,
        "gpu": 0.2499,
        "vram": 0.18
    },
    "malayalam_iitd": {
        "cpu": 0.2499,
        "ram": 0.13,
        "gpu": 0.2499,
        "vram": 0.18
    },
    "marathi_iitd": {
        "cpu": 0.2499,
        "ram": 0.13,
        "gpu": 0.2499,
        "vram": 0.18
    },
    "oriya_iitd": {
        "cpu": 0.2499,
        "ram": 0.13,
        "gpu": 0.2499,
        "vram": 0.18
    },
    "tamil_iitd": {
        "cpu": 0.2499,
        "ram": 0.13,
        "gpu": 0.2499,
        "vram": 0.18
    },
}

def main():
    triton_http_client = TritonLRUHttpClientSync(triton_url, model_requirements_map)

    available_models = triton_http_client.get_available_models()

    for _i in range(num_inference_tests):
        target_model_id = rand_choice(available_models)
        triton_http_client.infer(target_model_id)

if __name__ == "__main__":
    main()
