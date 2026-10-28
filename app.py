from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Clean Tableau Public views URL
    tableau_url = "https://public.tableau.com/views/hansrajdashboard/Dashboard1"
    return render_template('index.html', tableau_url=tableau_url)

if __name__ == '__main__':
    app.run(debug=True, port=5000)