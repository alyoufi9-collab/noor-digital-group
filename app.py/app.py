from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Noor Digital Group - جديد</h1>
    <p>NoorBook - مدير اعلانات نور</p>
    <p>NoorSocial - تواصل</p>
    <p>NoorShot - فيديو</p>
    <p>NoorChat - دردشة</p>
    <p>NoorMarket - سوق</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
