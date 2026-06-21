# QR-Based Local File Sharing App

A secure local-network file sharing application that allows users to transfer files between devices using QR codes. The platform provides encrypted storage, real-time updates, OCR-powered search, temporary download links, and user authentication.

## Features

### Secure File Sharing

* Upload and share files across devices connected to the same network
* Access the application instantly by scanning a generated QR code
* Secure user authentication with login and signup functionality

### End-to-End File Protection

* Files are encrypted before being stored on the server using Fernet encryption
* Decryption happens only when a file is downloaded or previewed

### OCR-Powered Search

* Automatically extracts text from uploaded images
* Search files using the text content inside images
* Makes image-based documents easily discoverable

### Real-Time Updates

* Live file list synchronization using Socket.IO
* Connected devices receive updates when files are uploaded or deleted

### Temporary Sharing Links

* Generate secure temporary download links
* Links automatically expire after a predefined duration

### File Management

* Drag-and-drop file uploads
* Multiple file upload support
* File preview functionality
* File deletion support
* Upload history tracking

### Device Tracking

* Records upload device information
* Stores upload timestamps and IP information

## Tech Stack

### Backend

* Flask
* Flask-SocketIO
* SQLite
* Cryptography (Fernet)

### Frontend

* HTML
* CSS
* JavaScript

### AI Features

* OCR Engine
* OCR-based Semantic File Search

## Project Structure

```text
├── app.py
├── ai_addition/
│   └── ocr_engine.py
├── db_folder/
│   ├── authentication.py
│   ├── fetch_history_data.py
│   ├── historyUpload.py
│   ├── file_expiry.py
│   ├── ocr_search.py
│   └── delete_history.py
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   └── history.html
├── static/
│   ├── style.css
│   ├── script.js
│   └── qr.png
├── shared/
└── requirements.txt
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/QR-based-File-sharing-App.git

cd QR-based-File-sharing-App
```

### Create Virtual Environment

```bash
python -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

install tesseract-git-eng on your system to access ocr Search

### Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

ENCRYPTION_KEY=your_fernet_key
```

Generate a Fernet key:

```python
from cryptography.fernet import Fernet

print(Fernet.generate_key().decode())
```

### Run Application

```bash
python app.py
```

The server will start on:

```text
http://<local-ip>:8080
```

Scan the generated QR code from another device on the same network to access the application.

## Workflow

1. User logs in.
2. Uploads one or more files.
3. Files are optionally processed through OCR.
4. Files are encrypted and stored securely.
5. Metadata is saved to the database.
6. Connected devices receive real-time updates.
7. Users can preview, search, download, or delete files.

## Security Features

* Password hashing using Werkzeug
* Session-based authentication
* Encrypted file storage using Fernet
* Temporary expiring download links
* Protected file access

## Future Improvements

* Background OCR processing
* File expiration scheduler
* Semantic search using embeddings
* Mobile-friendly UI improvements
* File versioning
* Share folders instead of individual files
* Cloud deployment support
* End-to-end encrypted sharing between devices

## Author

Harsh Shah