from flask import make_response
import uuid
from flask import render_template, abort
from Model.LocalTrack import *
from Model.Track import *
from Global import db, app

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/import')
def importation():
    db.create_all()
    failed_tracks = []
    succeeded_tracks = 0
    path = '/home/treisska/Music/ble'
    try:
        os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/static/library/', )
    except OSError:
        pass
    new_path = os.path.dirname(os.path.realpath(__file__)) + '/static/library/' + uuid.uuid1().__str__()
    os.symlink(path, new_path)
    for (dirpath, dirnames, filenames) in os.walk(new_path):
        for name in filenames:
            try:
                tmp = LocalTrack(os.path.join(dirpath, name))
                succeeded_tracks+=1
                db.session.add(tmp)
                db.session.commit()
            except:
                failed_tracks.append(name)
    return render_template('import_finished.html', succeeded_tracks=succeeded_tracks, failed_tracks=failed_tracks)

@app.route('/track/<int:track_id>')
def track(track_id):
    track = Track.query.filter(Track.id== track_id).first()
    if track == None:
       abort(404)
    else:
        response = make_response(render_template('track.html', track=track))
        response.headers['X-PJAX-Title'] = 'La radio du local - ' + track.name
        return response


@app.route('/artist/<int:artist_id>')
def artist(artist_id):
    artist = Artist.query.filter(Artist.id== artist_id).first()
    if artist == None:
       abort(404)
    else:
        response = make_response(render_template('artist.html', artist=artist))
        response.headers['X-PJAX-Title'] = 'La radio du local - ' + artist.name
        return response

@app.route('/album/<int:album_id>')
def album(album_id):
    album = Album.query.filter(Album.id==album_id).first()
    if album == None:
        abort(404)
    else:
        response = make_response(render_template('album.html', album=album))
        response.headers['X-PJAX-Title'] = 'La radio du local - ' + album.name
        return response


@app.route('/fulllist')
def list():
    tracks = Track.query.filter()
    response = make_response(render_template('search.html', tracks=tracks))
    response.headers['X-PJAX-Title'] = 'La radio du local - ' + 'query'
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
