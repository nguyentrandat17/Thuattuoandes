from flask import Flask, render_template_string, request, send_file, redirect, flash, url_for
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib, os, webbrowser, threading

app = Flask(__name__)
app.secret_key = 'secretkey'
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>AES File Encrypt/Decrypt</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">
    <style>
      body {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        min-height: 100vh;
        font-family: 'Segoe UI', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #fff;
      }
      .glass-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 40px;
        max-width: 500px;
        width: 100%;
      }
      .form-control, .form-select {
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.1);
        border: none;
        color: #fff;
      }
      .form-control::placeholder {
        color: #ccc;
      }
      .form-control:focus, .form-select:focus {
        border: 2px solid #00e0ff;
        background-color: rgba(255, 255, 255, 0.15);
        color: #fff;
      }
      .btn-primary {
        background-color: #00e0ff;
        border: none;
        font-weight: bold;
      }
      .btn-primary:hover {
        background-color: #00b8d4;
      }
      .alert {
        background-color: rgba(255, 255, 255, 0.85);
        color: #000;
      }
      h2 {
        color: #00e0ff;
      }
      label.form-label {
        color: #ccc;
        font-weight: 500;
      }
    </style>
  </head>
  <body>
    <div class="glass-card">
      <h2 class="text-center mb-4"><i class="bi bi-shield-lock"></i> AES File Encrypt / Decrypt</h2>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          {% for category, message in messages %}
            <div class="alert alert-{{category}} alert-dismissible fade show" role="alert">
              {{ message }}
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
          {% endfor %}
        {% endif %}
      {% endwith %}
      <form method="POST" enctype="multipart/form-data">
        <div class="mb-3">
          <label class="form-label">📁 File cần xử lý:</label>
          <input class="form-control" type="file" name="file" required>
        </div>
        <div class="mb-3">
          <label class="form-label">🔑 Nhập khóa (tự do):</label>
          <input type="text" class="form-control" name="key" placeholder="Ví dụ: mysecretkey" required>
        </div>
        <div class="mb-3">
          <label class="form-label">⚙️ Chọn thao tác:</label>
          <select class="form-select" name="action" required>
            <option value="encrypt">🔐 Mã hóa</option>
            <option value="decrypt">🔓 Giải mã</option>
          </select>
        </div>
        <div class="d-grid">
          <button type="submit" class="btn btn-primary btn-lg"> Thực hiện</button>
        </div>
      </form>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
"""

def get_aes_cipher(key: str, mode=AES.MODE_ECB):
    hashed_key = hashlib.sha256(key.encode()).digest()[:16]  # AES-128
    return AES.new(hashed_key, mode)

def encrypt_file(data: bytes, key: str) -> bytes:
    cipher = get_aes_cipher(key)
    return cipher.encrypt(pad(data, AES.block_size))

def decrypt_file(data: bytes, key: str) -> bytes:
    cipher = get_aes_cipher(key)
    return unpad(cipher.decrypt(data), AES.block_size)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('file')
        key = request.form.get('key')
        action = request.form.get('action')

        if not file or file.filename == '':
            flash(('warning', 'Vui lòng chọn một file.'))
            return redirect(url_for('index'))

        if not key:
            flash(('warning', 'Vui lòng nhập khóa.'))
            return redirect(url_for('index'))

        data = file.read()

        try:
            if action == 'encrypt':
                result = encrypt_file(data, key)
                output_filename = 'encrypted_' + file.filename
            elif action == 'decrypt':
                result = decrypt_file(data, key)
                output_filename = 'decrypted_' + file.filename
            else:
                flash(('danger', 'Chức năng không hợp lệ.'))
                return redirect(url_for('index'))
        except Exception as e:
            flash(('danger', f'Lỗi xử lý: {str(e)}'))
            return redirect(url_for('index'))

        output_path = os.path.join(RESULT_FOLDER, output_filename)
        with open(output_path, 'wb') as f:
            f.write(result)

        return send_file(output_path, as_attachment=True, download_name=output_filename)

    return render_template_string(HTML_TEMPLATE)

# Tự động mở trình duyệt sau 1 giây
def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True)
