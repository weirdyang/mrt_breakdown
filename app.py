import pandas as pd
import json
import pygal
from flask import (Flask, jsonify, render_template, url_for, request)

app = Flask(__name__)
master_df = pd.read_json('static/master.json', orient='records')
jsonfile = open('static/master.json', mode='r', encoding='utf-8')
master_json = json.load(jsonfile)
genre_list = ['Action', 'Drama', 'Comedy', 'Animation', 'All']


@app.route('/', methods=['GET'])
def index():
    """
    Route that maps to the main index page.
    """
    return render_template('index.html')


@app.route('/generate/<search_term>', methods=['GET'])
def generate(search_term):
    """
    filters df based on genre choice
    """
    print(search_term)
    if search_term == 'all':
        results = master_df.to_json(orient='records')
    else:
        filtered = master_df[master_df['genre'].str.contains(
            search_term, case=False)]
        results = filtered.to_json(orient='records')

    return jsonify(results)

@app.route('/ratings', methods=['GET'])
def ratings():
    """
    Route that maps to ratings page
    """
    return render_template('ratings.html')

@app.route('/pygal_generate/', methods=['GET'])
def pygal_generate():
    """
    Route that generates pygal chart
    Attribution: http://biobits.org/bokeh-flask.html
    """
    search_term = request.args.get("genre")
    print(search_term)
    if (search_term == None) or (search_term=='All') :
        search_term = 'All'
        results = master_df.to_json(orient='records')
    else:
        filtered = master_df[master_df['genre'].str.contains(
            search_term, case=False)]
        results = filtered.to_json(orient='records')
    json_data = json.loads(results)
    xy_chart = pygal.XY(stroke=False, show_legend=False)
    xy_chart.title = "Movie's RT score vs IMDB Rating"
    xy_chart.x_title = "Rotten Tomatoes Score"
    xy_chart.y_title = "IMDB Rating"
    for item in json_data:
        xy_chart.add(item['Movie'], [{'value': (item['RT'],  float(str(item['IMDB'])[:4]))}])
    chart = xy_chart.render_data_uri()
    return render_template('comparison.html', chart=chart, genres=genre_list, selected_genre=search_term)



if __name__ == '__main__':
    app.run(debug=True)
