from flask import redirect
from __main__ import app

# CATCH-ALL
@app.route('/*', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def catch_all(u_path):
    return redirect('/')
