from flask import Flask, request, Response
from requests import Session

from src.config import APP_MODE, DEVLOPMENT_HOST, DEVLOPMENT_PORT, TRITON_HTTP_URL, model_requirements_map
from src.responses import explicit_model_control_not_allowed_response
from src.triton_clients import TritonLRUHttpClientSync


triton_requests_session = Session()
triton_url = TRITON_HTTP_URL.replace("https://", "").replace("http://", "")
triton_lru_http_client = TritonLRUHttpClientSync(triton_url, model_requirements_map)

app = Flask(__name__)


@app.route('/v2/repository/models/<model_name>/load', methods=['POST'])
def load_model(model_name):
    return explicit_model_control_not_allowed_response


@app.route('/v2/repository/models/<model_name>/unload', methods=['POST'])
def unload_model(model_name):
    return explicit_model_control_not_allowed_response


@app.route('/v2/models/<model_name>/infer', methods=['POST'])
def infer_model(model_name):
    triton_http_request_url = f"{TRITON_HTTP_URL}/v2/models/{model_name}/infer"
    triton_http_request_headers = {
        key: value for key, value in request.headers if key != 'Host'
    }
    triton_http_request_data = request.data

    triton_lru_http_client.pre_infer(model_name)
    
    triton_http_response = triton_requests_session.post(
        triton_http_request_url, data=triton_http_request_data, headers=triton_http_request_headers
    )
    
    # NOTE we here exclude all "hop-by-hop headers" defined by RFC 2616 section 13.5.1
    # ref. https://www.rfc-editor.org/rfc/rfc2616#section-13.5.1
    flask_response_excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    flask_response_headers = [
        (k,v) for k,v in triton_http_response.raw.headers.items()
        if k.lower() not in flask_response_excluded_headers
    ]

    flask_response = Response(triton_http_response.content, triton_http_response.status_code, flask_response_headers)
    return flask_response

    
if __name__ == '__main__':
    if APP_MODE != "DEVELOPMENT":
        raise ValueError("app.py::main block cannot be run in 'PRODUCTION' mode.")
    
    app.run(host=DEVLOPMENT_HOST, port=DEVLOPMENT_PORT, threaded=False, debug=False)
