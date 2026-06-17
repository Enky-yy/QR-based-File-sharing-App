from flask import Flask , render_template , send_from_directory , redirect, request , jsonify , session, send_file
import socket
import os 
import qrcode
import secrets, time
import io
from flask_socketio import SocketIO , emit
from db_folder import initialization,fetch_history_data , historyUpload , file_expiry , authentication , ocr_search, delete_history
import all_functions
from werkzeug.security import(
    generate_password_hash,
    check_password_hash
)
from cryptography.fernet import Fernet
from ai_addition import ocr_engine
import uuid

app = Flask(__name__)
socketio = SocketIO(app)
# print(os.environ.get('SECRET_KEY'))

app.secret_key = os.environ.get('SECRET_KEY')
# use export SECRET_KEY="YOUR_SECRET_KEY" before starting app to use upper version of secret key

ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
# use export ENCRYPTION_KEY="YOUR_ENCRYPTION_KEY" before starting app to use upper version of secret key

# app.secret_key = 'key'
# ENCRYPTION_KEY = b'key'

# with open ('secrets.txt', 'r')as f:
#     ENCRYPTION_KEY=f.read(-1)

cipher = Fernet(ENCRYPTION_KEY)

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
        username = request.form.get('username')
        password = request.form.get('password')

        user =authentication.login(username)

        if user and check_password_hash(user[1], password):
            session['user_id']= user[0]
            session['username']= username

        if not session.get('user_id'):
            return redirect('/login')
        return redirect('/')
        
    return render_template('login.html')

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password')

        hash_password = generate_password_hash(password)

        authentication.signup(username,hash_password)

        return redirect('/login')
    
    return render_template('/signup.html')

@app.route('/logout')
def logout():
    session.clear()

    return redirect('/login')


@app.route('/')
def choose_files():

    if not session.get('user_id'):
        return redirect('/login')
    
    file_data = all_functions.get_file_data(shared_folder)

    file_expiry.cleanup_expired_files(shared_folder)
    return render_template('index.html',files = file_data)

@app.route('/search')
def search():
    query = request.args.get('q','').strip()

    # print(query)

    if not query:
        return jsonify([])

    results = ocr_search.ocr_search(query)
    # print(results)

    files = [
        result[0] for result in results
        
    ]
    # print (files)

    return jsonify(files)

@app.route('/upload', methods=['POST'])
def upload():

    if 'files' not in request.files:
        return redirect('/')
    
    upload_files = request.files.getlist('files')

    for file in upload_files:
        if file.filename == '':
            continue

        file_id = str(uuid.uuid4())

        unique_filename = f"{file_id}_{file.filename}"
        save_path = os.path.join(shared_folder,unique_filename)

        file.save(save_path)

        ocr_text=''

        if file.filename.lower().endswith(('.png','.jpeg','.jpg')):
            ocr_text= ocr_engine.extract(save_path)
            print('ocr: ',ocr_text)

        with open(save_path, 'rb') as f:
            data = f.read()
            # print(len(data))
        

        encrypted_data = cipher.encrypt(data)
        # print(len(encrypted_data))

        with open(save_path, 'wb') as f:
            f.write(encrypted_data)


        historyUpload.upload(file_id,unique_filename,file.filename, request.remote_addr, all_functions.detect_device(request.headers.get('User-Agent')),time.strftime('%Y-%m-%d %H:%M:%S'), ocr_text)



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
    
    # print(data['file'])
    
    path = os.path.join(shared_folder, data['file'])

    with open(path,'rb') as f:
        encrypted_data =f.read()

    decrypted_data =cipher.decrypt(encrypted_data)
    
    return send_file(
        io.BytesIO(decrypted_data),
        download_name=data['file'],
        as_attachment=True
    )

# @app.route('/download/<filename>')
# def sharing(filename):
#     return send_from_directory(shared_folder, filename, as_attachment=True)

@app.route('/preview/<filename>')
def preview_file(filename):

    path = os.path.join(
        shared_folder,
        filename
    )

    with open(path, 'rb') as f:

        encrypted_data = f.read()

    decrypted_data =cipher.decrypt(encrypted_data)
    print(len(decrypted_data))
    # print(decrypted_data)

    original_name = filename.split('_',1)[1]


    return send_file(
        io.BytesIO(decrypted_data),
        download_name=original_name
    )

@app.route('/delete/<file_id>', methods=['POST'])
def delete_file(file_id):

    result = delete_history.select_data(file_id)

    if result:
        stored_filename = result[0]

        path = os.path.join(shared_folder, stored_filename)

        if os.path.exists(path):
            os.remove(path)
        
        delete_history.delete_history(file_id)

    socketio.emit('file_updated', all_functions.get_file_data(shared_folder))
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
    