from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
import json

app = Flask(__name__)


def load_blog_posts():
    """
    Load the blog posts from the JSON file.
    Returns:
        list: List of blog posts.
    """
    with open('blog_post.json', 'r') as file:
        return json.load(file)


def save_blog_posts(posts):
    """
    Save the blog posts to the JSON file.
    Args:
        posts (list): List of blog posts.
    """
    with open('blog_post.json', 'w') as file:
        json.dump(posts, file, indent=4)


@app.route('/')
def index():
    """
    Route for the home page.
    Returns:
        str: Rendered template for the home page.
    """
    blog_posts = load_blog_posts()
    return render_template('index.html', posts=blog_posts)


def generate_unique_id():
    """
    Generate a unique ID based on the current timestamp.
    Returns:
        str: Unique ID.
    """
    return datetime.now().strftime('%Y%m%d%H%M%S')


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Route for adding a new blog post.
    Returns:
        response: Response object.
    """
    blog_posts = load_blog_posts()
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        new_id = generate_unique_id()

        new_post = {'id': new_id, 'author': author, 'title': title, 'content': content,'likes':0}

        blog_posts.append(new_post)

        save_blog_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<post_id>')
def delete(post_id):
    """
    Route for deleting a blog post.
    Args:
        post_id (str): ID of the post to be deleted.
    Returns:
        response: Response object.
    """
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    save_blog_posts(blog_posts)

    return redirect(url_for('index'))


@app.route('/update/<string:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Route for updating a blog post.
    Args:
        post_id (str): ID of the post to be updated.
    Returns:
        response: Response object.
    """
    blog_posts = load_blog_posts()
    post = None
    for blog_post in blog_posts:
        if blog_post['id'] == post_id:
            post = blog_post
            break

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        post['author'] = author
        post['title'] = title
        post['content'] = content

        save_blog_posts(blog_posts)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


@app.route('/like/<string:post_id>', methods=['POST'])
def like(post_id):
    """
        Route for liking a blog post.
        Returns:
            response: Response object.
        """
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] += 1
            break
    save_blog_posts(blog_posts)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
