from flask import Flask, request, abort

app = Flask(__name__)

# Define a list of blocked IP addresses
blocked_ips = set()

# Define a simple rule to block requests with "SQL injection" in the query string
def waf_rule(request):
    if "SQL injection" in request.args.get("q", ""):
        return True
    return False

@app.before_request
def waf_middleware():
    if request.remote_addr in blocked_ips:
        abort(403) # Block the request if the IP is in the blocked list

    if waf_rule(request):
        blocked_ips.add(request.remote_addr)
        abort(403) # Block the request if it matches the rule

@app.route('/')
def home():
    return 'Welcome to my web application!'

if __name__ == '__main__':
    app.run()
