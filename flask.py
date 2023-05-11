from flask import Flask, request, abort

app = Flask(_name_)

@app.before_request
def waf_filter():
    # Block requests with SQL injection attempts
    if "'; DROP TABLE" in request.url:
        abort(403)

    # Block requests from known malicious IPs
    if request.remote_addr in ["127.0.0.1", "192.168.1.1"]:
        abort(403)

    # Log all requests
    with open("waf.log", "a") as f:
        f.write(f"{request.method} {request.url} from {request.remote_addr}\n")

if _name_ == '_main_':
    app.run()
