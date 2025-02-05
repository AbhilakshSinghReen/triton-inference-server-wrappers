docker run --rm \
  --name tritonserver-lru-wrapper \
  --network host \
  -e APP_MODE=PRODUCTION \
  -e TRITON_HTTP_URL="http://localhost:7000" \
  tritonserver-lru-wrapper
