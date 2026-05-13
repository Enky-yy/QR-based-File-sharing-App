from flask import Flask , render_template , send_from_directory , redirect, request , jsonify
import socket
import os 
import qrcode

app = Flask(__name__)

shared_folder = "shared"

def format_file_size(size):

    for unit in ['B','KB','MB', 'GB', "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024

def get_local_ip_add():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip= s.getsockname()[0]
    finally:
        s.close()
    return ip

@app.route('/')
def choose_files():
    file_data = []

    for file in os.listdir(shared_folder):

        path = os.path.join(shared_folder, file)

        if os.path.isfile(path):

            size = os.path.getsize(path)

            file_data.append({
                'name': file,
                'size': format_file_size(size)
            })


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

    return '', 200

@app.route('/download/<filename>')
def sharing(filename):
    return send_from_directory(shared_folder, filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    path = os.path.join(shared_folder, filename)
    if os.path.exists(path):
        os.remove(path)
    return redirect('/')



if __name__ == '__main__':
    port = 8080
    ip = get_local_ip_add()
    host_url = f"http://{ip}:{port}"
    img = qrcode.make(host_url)
    os.makedirs("static", exist_ok=True)
    os.makedirs(shared_folder, exist_ok=True)
    img.save("static/qr.png")

    print(f"server is running on URL Address: {host_url}")

    app.run(host="0.0.0.0", port=port, debug=True)
    