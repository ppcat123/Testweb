from flask import Flask, render_template, request
from scraper.gogo import search_anime, get_episodes, get_stream_url

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    results = search_anime(query)
    return render_template('search.html', results=results)

@app.route('/anime/<slug>')
def anime(slug):
    episodes = get_episodes(slug)
    return render_template('anime.html', slug=slug, episodes=episodes)

@app.route('/watch/<slug>/<episode_id>')
def watch(slug, episode_id):
    video_url = get_stream_url(episode_id)
    return render_template('watch.html', video_url=video_url)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
