from flask import Flask, request, render_template
from elastic import *
from charts import *
app = Flask(__name__)
elastic=ES()
@app.route('/')
def index():
    # return 'hello'
    return render_template('index.html')

@app.route('/show', methods=['GET'])
def show():
    # print 'ping',request.form['term']
    if request.method == 'GET':
        result=elastic.search(request.args['term'])
        try:
            sentiments=[hit['_source']['sentiment'] for hit in result['hits']['hits']]
        except:
            sentiments=[]
        if sentiments:
            freq=get_freq(sentiments)
            chart = get_chart(freq)
        else:
            chart='<p>No results found</p>'
        return(chart)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')