from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

@app.route('/')
def index():
    
    data = pd.read_csv('../New_Grad_Listings.csv')
    data_html = data.to_html(index=False, header=False, border=0)
    return render_template('index.html', data_html= data_html)

if __name__ == '__main__':
    app.run(debug=True)