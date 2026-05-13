from flask import Flask , render_template , send_from_directory , redirect, request , jsonify , session
import socket
import os 
import qrcode
import secrets, time
from flask_socketio import SocketIO , emit
from db_folder import initialization,fetch_history_data , historyUpload , file_expiry
import all_functions

app = Flask(__name__)
socketio = SocketIO(app)
print(os.environ.get('SECRET_KEY'))

app_password = 'harsh123'

# app.secret_key = os.environ.get('SECRET_KEY')

app.secret_key = 'key'

shared_folder = "shared"

temporary_links={}

# file_expiry_db={}


def get_local_ip_add():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip= s.getsockname()[0]
    finally:
        s.close()
    return ip



@app.route('/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')

        if password == app_password:
            session['authenticated'] = True
            return redirect('/')
        
    return render_template('login.html')

@app.route('/')
def choose_files():

    if not session.get('authenticated'):
        return redirect('/login')
    
    file_data = all_functions.get_file_data(shared_folder)

    file_expiry.cleanup_expired_files(shared_folder)
    return render_template('index.html',files = file_data)

@app.route('/upload', methods=['POST'])
def upload():

    if 'files' not in request.files:
        return redirect('/')
    
    upload_files = request.files.getlist('files')

    for file in upload_files:
        if file.filename == '':
            continue
        save_path = os.path.join(shared_folder, file.filename)

        file.save(save_path)


        historyUpload.upload(file.filename, request.remote_addr, all_functions.detect_device(request.headers.get('User-Agent')),time.strftime('%Y-%m-%d %H:%M:%S'))



    socketio.emit('file_updated',all_functions.get_file_data(shared_folder))

    return '', 200


@app.route('/generate-link/<filename>')
def generate_links(filename):
    token = secrets.token_urlsafe(16)
    temporary_links[token]={
        'file':filename,
        'expiry' : time.time() + 600
    }

    return redirect(f"/temp-download/{token}")

@app.route('/temp-download/<token>')
def temp_download(token):
    data = temporary_links.get(token)

    if not data:
        return 'invalid link'
    
    if time.time() > data['expiry']:
        temporary_links.pop(token)

        return 'Link Expired'
    
    return send_from_directory(shared_folder, data['file'],as_attachment= True)

# @app.route('/download/<filename>')
# def sharing(filename):
#     return send_from_directory(shared_folder, filename, as_attachment=True)

@app.route('/preview/<filename>')
def preview_file(filename):

    return send_from_directory(
        shared_folder,
        filename
    )

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    path = os.path.join(shared_folder, filename)

    if os.path.exists(path):
        os.remove(path)

    socketio.emit('file_deleted', all_functions.get_file_data(shared_folder))
    return redirect('/')

@app.route('/history')
def history():

    return render_template(
        'history.html',
        history=fetch_history_data.history()
    )



if __name__ == '__main__':
    port = 8080
    ip = get_local_ip_add()
    qr_token = secrets.token_urlsafe(8)
    host_url = f"http://{ip}:{port}"
    img = qrcode.make(f"{host_url}/login?token={qr_token}")
    os.makedirs("static", exist_ok=True)
    os.makedirs(shared_folder, exist_ok=True)
    img.save("static/qr.png")

    initialization.init_db()

    print(f"server is running on URL Address: {host_url}")

    # app.run(host="0.0.0.0", port=port, debug=True)

    socketio.run(
        app=app, host="0.0.0.0",port=port, debug=True
    )
    