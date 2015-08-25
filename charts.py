from __future__ import division
from nvd3 import pieChart
from collections import defaultdict

def get_freq(sentiments):
    fq= defaultdict( int )
    for w in sentiments:
        fq[w] += 1
    total=sum(fq.values())
    fq={k:100*(v/total) for k,v in fq.iteritems()}
    return fq


def get_chart(freq):
    chart_type = 'pieChart'
    chart = pieChart(name=chart_type, color_category='category20c', height=450, width=450)
    extra_serie = {"tooltip": {"y_start": "", "y_end": " %"}}
    xdata,ydata=zip(*freq.items())
    chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
    # text_white="d3.selectAll('#pieChart text').style('fill', 'white');"
    # chart.add_chart_extras(text_white)
    chart.buildcontent()
    return chart.htmlcontent

