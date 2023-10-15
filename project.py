from app import app, db
from app.models import User, Post, Hashtag, post_hashtag

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


@app.shell_context_processors
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'post_hashtag': post_hashtag, 'Hashtag': Hashtag}
