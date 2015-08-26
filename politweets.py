from flask import Flask, request, render_template, url_for
from elastic import *
from charts import *
app = Flask(__name__)
elastic=ES()
@app.route('/',methods=['GET'])
def index():
    # return 'hello'
    if request.method=='GET':
        term=request.args.get('term')
        chartmarkup=process_term(term)
    count=str(elastic.get_count())
    return render_template('index.html',count=count,chart=chartmarkup)

@app.route('/show', methods=['GET'])
def show():
    # print 'ping',request.form['term']
    if request.method == 'GET':
        term = request.args.get('term')
        chartmarkup=process_term(term)
        return(chartmarkup)
    else:
        return ''

def process_term(term):
    if term:
        try:
            result=elastic.search(term)
            sentiments=[hit['_source']['sentiment'] for hit in result['hits']['hits']]
        except:
            sentiments=[]
        if sentiments:
            freq=get_freq(sentiments)
            chart = get_chart(freq)
        else:
            chart=''
        return(render_template('chart.html',chart=chart,result_count=str(len(sentiments)),term=term,permalink=url_for('index',term=term)))
    else:
        return('')





if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')