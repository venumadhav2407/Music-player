from flask import Flask, render_template, request, redirect, url_for, session,flash, jsonify, send_from_directory
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import secrets
import os
import json

app = Flask(__name__)

# DB configuration
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "user_details"
# Extra configs, optional:
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_PATH'] = 50 * 1024 * 1024  # 50 MB max file size


# Create uploads directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Generate a random secret key
secret_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = secret_key

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('home.html')

# admin page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM userprofile WHERE username = %s', [username])
        admin = cursor.fetchone()
        if admin and admin['passwd'] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Admin Login successful', 'success')
            return redirect(url_for('adminpage'))
        else:
            error = 'Invalid username or password'
            return render_template('admin/adminlogin.html', error=error)
    return render_template('admin/adminlogin.html')
        
@app.route('/adminpage')
def adminpage():
    if 'logged_in' not in session:
        return redirect(url_for('admin'))
    return render_template('admin/admin.html')


# upload songs 
@app.route('/upload_songs', methods=['POST'])
def upload_songs():
    # Check if the request contains the required fields
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('adminpage'))

    # files = request.files.getlist('file')
    file = request.files['file']
    title = request.form['title']
    artist = request.form['artist']
    album = request.form['album']
    language = request.form['language'].upper()

    # Check if all fields are provided
    if not (file and title and artist and album and language):
        flash('All fields are required', 'danger')
        return redirect(url_for('adminpage'))

    # Save the file to the uploads folder
    # Iterate over each file and save it to the uploads folder
    # for file_ in files:
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # check if filename already exists
        if os.path.exists(file_path):
            flash('File already exists', 'danger')
            return redirect(url_for('adminpage'))
        file.save(file_path)
        
        # Insert the song details into the database
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO songs (title, artist, album, language, path) VALUES (%s, %s, %s, %s, %s)', [title, artist, album, language, file_path])
            mysql.connection.commit()
            flash('Song uploaded successfully', 'success')
        except Exception as e:
            flash(f'Error uploading song: {e}', 'danger')
                
    return redirect(url_for('adminpage'))



# login 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        useremail = request.form['email']
        password = request.form['password']
       
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM userprofile WHERE email = %s', [useremail])
        user = cursor.fetchone()
        if user and user['passwd'] == password:
            session['logged_in'] = True
            session['username'] = user['username']
            session['userid'] = user['id']
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM userprofile WHERE username = %s', [username])
        user = cursor.fetchone()
        if user:
            flash('Username already exists', 'danger')
        else:
            cursor.execute('INSERT INTO userprofile (username, email, passwd) VALUES (%s, %s, %s)', [username, email, password])
            mysql.connection.commit()
            flash('Registered successfully', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    # display in the  dashboard to add specific playlist name
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, playlistname FROM playlist WHERE username = %s', [session['username']])
    playlists = cursor.fetchall()
    
    # songs = getSongDetails()
    return render_template('dashboard.html', playlists=playlists)



#  playlist
@app.route('/playlist', methods=['GET'])
def playlist():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    result = []
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, playlistname FROM playlist WHERE username = %s', [session['username']])
    playlists = cursor.fetchall()
    
    result = []
    for playlist in playlists:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT a.playlist_id, c.* from playlist_song a  join songs c on a.song_id = c.id where a.playlist_id = %s', [playlist['id']])
        data = cursor.fetchall()
        
        for song in data:
            song['path'] = url_for('uploaded_file',filename=song['path'].split('\\')[1])
        result.extend(data) 
    print(result)

    return render_template('playlist.html', playlists=playlists, playlistsong=result)
    

@app.route('/createplaylist', methods=['POST'])
def createplaylist():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    playlist_name = request.form['playlistname']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM playlist WHERE username= %s and playlistname=%s', [session['username'], playlist_name])
    res = cursor.fetchone()
    if res:
        flash('Playlist already exists', 'danger')
        return redirect(url_for('playlist'))
    
    cursor.execute('INSERT INTO playlist (username, playlistname) VALUES (%s, %s)', [session['username'], playlist_name])
    mysql.connection.commit()
    flash('Playlist created successfully', 'success')
    return redirect(url_for('playlist'))

# load the playlist dynamically
@app.route('/api/playlists', methods=['GET'])
def api_get_playlists():
    if 'logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, playlistname FROM playlist WHERE username = %s', [session['username']])
    playlists = cursor.fetchall()
    
    return jsonify(playlists)



# delete playlist
@app.route('/deleteplaylist', methods=['POST'])
def deleteplaylist():
    if 'logged_in' not in session: 
        return redirect(url_for('login'))
    
    playlist_id = request.form['playlistId']
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM playlist WHERE id = %s', [playlist_id])
    mysql.connection.commit()
    flash('Playlist deleted successfully', 'success')
    return redirect(url_for('playlist'))


#  ----------------   add likes songs to playlist
@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    song_id = request.form['music_id']
    playlist_id = request.form['playlist_id']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO playlist_song (playlist_id, song_id) VALUES (%s, %s)', [playlist_id, song_id])
    mysql.connection.commit()
    flash('Song added to playlist', 'success')
    return redirect(url_for('dashboard'))

@app.route('/remove_from_playlist', methods=['POST'])
def remove_from_playlist():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    song_id = request.form['music_id']
    playlist_id = request.form['playlist_id']
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM playlist_song WHERE playlist_id = %s AND song_id = %s', [playlist_id, song_id])
    mysql.connection.commit()
    flash('Song removed from playlist', 'success')
    return redirect(url_for('dashboard'))
    


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    '''
        This route is commonly used to serve static files, such as images, documents, or media files, stored on the server.
    '''
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# load the songs in dashboard
@app.route('/songs')
def songs():
    # songs = getSongDetails()
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM songs')
    songs = cursor.fetchall()
    
    # Convert backslashes to forward slashes in file paths
    for song in songs:
        song['path'] = url_for('uploaded_file',filename=song['path'].split('\\')[1])
    
    return json.dumps(songs)
    
    
# song lists page
@app.route('/songslist')
def songslist():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('songslist.html')

@app.route('/api/songs', methods=['GET'])
def get_songs_by_language():
    language = request.args.get('language')
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM songs WHERE language = %s', [language])
    songs = cursor.fetchall()
    # Convert backslashes to forward slashes in file paths
    for song in songs:
        song['path'] = url_for('uploaded_file',filename=song['path'].split('\\')[1])
    return jsonify(songs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    



