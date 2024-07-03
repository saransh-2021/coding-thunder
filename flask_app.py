from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url
import sqlalchemy

# Get the directory of the current script
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super_secret_key")

app.config["UPLOAD_FOLDER"] = basedir

# Parameters loaded from environment variables
params = {
    "local_server": os.getenv("LOCAL_SERVER", "True"),
    "local_uri": os.getenv("LOCAL_URI", "mysql://root:saransh@localhost/codingthunder"),
    "prod_uri": os.getenv("PROD_URI", "mysql+mysqldb://trying768:my-code-thun@trying768.mysql.pythonanywhere-services.com/trying768$codingthunder"),
    "gmail-username": os.getenv("GMAIL_USERNAME", "wonderfulemail@gmail.com"),
    "gmail-password": os.getenv("GMAIL_PASSWORD", "a-sUperSEcuR!TYp@SSw0rd"),
    "mail-reply-to": os.getenv("MAIL_REPLY_TO", "otherwonderfullemail@gmail.com"),
    "no_of_posts": int(os.getenv("NO_OF_POSTS", "3")),
    "admin_user": os.getenv("ADMIN_USER", "saransh"),
    "admin_password": os.getenv("ADMIN_PASSWORD", "slimshady")
}

# Site configuration loaded from environment variables
site_config = {
    "fb_url": os.getenv("FB_URL", "https://www.facebook.com/"),
    "tw_url": os.getenv("TW_URL", "https://www.twitter.com/"),
    "gthb_url": os.getenv("GTHB_URL", "https://www.github.com/"),
    "blog_name": os.getenv("BLOG_NAME", "Coding Thunder"),
    "tag_line": os.getenv("TAG_LINE", "Heaven for Programmers"),
    "about_text": os.getenv("ABOUT_TEXT", "")
}

app.config.update(
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com'),
    MAIL_PORT = int(os.getenv('MAIL_PORT', 465)),
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'True').lower() in ('true', '1', 't', 'yes'),
    MAIL_USERNAME = params["gmail-username"],
    MAIL_PASSWORD = params["gmail-password"],
    MAIL_DEFAULT_SENDER = params["gmail-username"]
)
mail = Mail(app)

if str(params['local_server']).lower() in ("true", "1", "yes"):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['prod_uri']

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle' : 280}

db = SQLAlchemy(app)

class Contacts(db.Model):
    """Database model for storing user contact inquiries."""
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    phone_num = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(120), nullable=False)

class Posts(db.Model):
    """Database model for storing blog posts."""
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=False, nullable=False)
    slug = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sub_heading = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    img_file = db.Column(db.String(500), nullable=True)


@app.route('/')
def home():
    """
    Renders the public home page with paginated blog posts.

    Query Params:
        page (int, optional): The page number for pagination. Defaults to 1.
    """
    page = request.args.get('page', 1, type=int)

    # Fetch posts for the current page using SQLAlchemy's .paginate() method
    posts = Posts.query.order_by(Posts.sno.desc()).paginate(page=page, per_page=params["no_of_posts"], error_out=False)
    return render_template('index.html', params=site_config, posts=posts)


@app.route('/about')
def about():
    """Renders the public About Us page with site information."""
    return render_template('about.html', params=site_config)


@app.route("/hello")
def hello():
    """Health check / test endpoint to verify server connectivity."""
    return "hello, you have successfully test connected with the coding thunders website"


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """
    Handles the contact form.

    GET: Renders the contact form page.
    POST: Processes submitted contact inquiry, saves it to the database,
          and sends an email notification.
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']

        entry = Contacts(name=name, phone_num=phone, msg=message, email=email, date=datetime.now().strftime("%Y-%m-%d"))
        db.session.add(entry)
        db.session.commit()
        try:
            mail.send_message(
                subject=f"New Message from {name}",
                recipients=[email],
                body=f"Message: {message}\n\nPhone: {phone}"
            )
        except Exception as e:
            app.logger.warning(f"Mail sending failed: {e}")

    return render_template('contact.html', params=site_config)


@app.route('/post/<string:post_slug>', methods=["GET"])
def post_route(post_slug):
    """
    Renders a single blog post identified by its unique URL slug.

    Args:
        post_slug (str): The slug identifier for the post.
    """
    post = Posts.query.filter_by(slug=post_slug).first()
    return render_template('post.html', params=site_config, post=post)


@app.route('/dashboard')
def dashboard():
    """
    Renders the admin dashboard with a list of all posts.
    Requires active admin session; otherwise redirects to login.
    """
    if "user" in session and session["user"] == params["admin_user"]:
        posts = Posts.query.order_by(Posts.sno.desc()).all()
        return render_template('dashboard.html', params=site_config, posts=posts)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=["GET", "POST"])
def login():
    """
    Admin authentication endpoint.

    GET: Renders the login page.
    POST: Authenticates admin credentials and initializes session.
    """
    if request.method == "POST":
        username = request.form["uname"]
        userpass = request.form["pass"]
        if username == params["admin_user"] and userpass == params["admin_password"]:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', params=site_config, message="Invalid credentials. Please try again.")
    else:
        return render_template('login.html', params=site_config)


@app.route('/logout')
def logout():
    """Logs out the admin by clearing session and redirects to home page."""
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/uploader', methods=["GET", "POST"])
def uploader():
    """
    File upload endpoint for authenticated admin.
    Saves temporary file and removes it once processed.
    """
    if "user" in session and session["user"] == params["admin_user"]:
        if request.method == "POST":
            f = request.files.get('file1')
            if not f or not f.filename:
                return "No file selected"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            f.save(file_path)
            os.remove(file_path)
            return "Uploaded successfully"
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route('/edit/<string:sno>', methods=["GET", "POST"])
def edit_route(sno):
    """
    Admin endpoint to create or edit a blog post.
    Requires active admin session.

    Args:
        sno (str): Serial number of the post ("0" creates a new post).

    GET: Renders the post creation/edit form.
    POST: Handles form submission and saves/updates post in database.
    """
    if "user" in session and session["user"] == params["admin_user"]:
        if request.method == "POST":
            title = request.form["title"]
            sub_heading = request.form["sub_heading"]
            slug = request.form["slug"]
            content = request.form["content"]
            img_file = request.form.get("img_file", "").strip()
            date = datetime.now().strftime("%Y-%m-%d")

            if sno == "0":
                post = Posts(title=title, sub_heading=sub_heading, slug=slug, content=content, img_file=img_file, date=date)
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                if post is None:
                    return redirect(url_for("dashboard"))
                post.title = title
                post.sub_heading = sub_heading
                post.slug = slug
                post.content = content
                post.img_file = img_file
                post.date = date
                db.session.commit()

            return redirect(url_for("dashboard"))
        else:
            post = Posts.query.filter_by(sno=sno).first()
            return render_template("edit.html", params=site_config, post=post)
    else:
        return redirect(url_for("login"))


@app.route('/delete/<string:sno>')
def delete(sno):
    """
    Admin endpoint to delete a blog post by serial number.
    Requires active admin session.

    Args:
        sno (str): Serial number of the post to delete.
    """
    if "user" in session and session["user"] == params["admin_user"]:
        post = Posts.query.filter_by(sno=sno).first()

        if post is None:
            return redirect(url_for("dashboard"))

        db.session.delete(post)
        db.session.commit()

        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

def ensure_database_exists():
    """
    Ensures that the MySQL database itself exists on the server before connecting.
    If the database is missing, it connects to the MySQL server instance
    and executes 'CREATE DATABASE IF NOT EXISTS <dbname>'.
    """
    db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    try:
        url = make_url(db_uri)
        if url.database and "mysql" in url.drivername:
            server_url = url.set(database="")
            engine = sqlalchemy.create_engine(server_url)
            with engine.connect() as conn:
                conn.execute(sqlalchemy.text(f"CREATE DATABASE IF NOT EXISTS `{url.database}` CHARACTER SET utf8mb4"))
                conn.commit()
            engine.dispose()
    except Exception as e:
        app.logger.warning(f"Database auto-creation check skipped or failed: {e}")


with app.app_context():
    # 1. Emergency bootstrap: automatically creates the database itself if missing on MySQL.
    ensure_database_exists()

    # 2. Creates all database tables (Contacts, Posts) if they don't exist.
    db.create_all()

    # 3. Seeds default sample posts if the posts table is empty.
    if Posts.query.count() == 0:
        today_str = datetime.now().strftime("%Y-%m-%d")

        default_posts = [
            Posts(
                title="The Rise of AI and Machine Learning",
                sub_heading="How artificial intelligence is transforming industries worldwide",
                slug="rise-of-ai-machine-learning",
                img_file="ai_machine_learning",
                date=today_str,
                content=(
                    "Artificial Intelligence and Machine Learning have moved far beyond academic "
                    "research labs. Today, they power everything from the recommendations you see "
                    "on streaming platforms to the fraud detection systems that protect your bank "
                    "account. Companies across healthcare, finance, transportation, and retail are "
                    "racing to integrate AI into their workflows.\n\n"
                    "In this post, we explore the key concepts behind AI and ML, the difference "
                    "between supervised and unsupervised learning, and real-world use cases that "
                    "are already reshaping how we live and work. Whether you're a developer looking "
                    "to get started or simply curious about the hype, this is your starting point."
                )
            ),
            Posts(
                title="Climate Change: Understanding the Crisis",
                sub_heading="The science, the impact, and what we can do about it",
                slug="climate-change-understanding-crisis",
                img_file="climate_change",
                date=today_str,
                content=(
                    "Climate change is no longer a distant threat — it's happening now. Rising "
                    "global temperatures, melting ice caps, intensifying storms, and shifting weather "
                    "patterns are affecting communities around the world. The scientific consensus "
                    "is clear: human activity, particularly the burning of fossil fuels, is the "
                    "primary driver.\n\n"
                    "This post breaks down the science behind climate change, examines its impact "
                    "on ecosystems and economies, and discusses actionable steps — from individual "
                    "lifestyle changes to global policy shifts — that can help mitigate the damage "
                    "before it becomes irreversible."
                )
            ),
            Posts(
                title="Renewable Energy: Powering the Future",
                sub_heading="Why solar, wind, and hydro are the key to a sustainable planet",
                slug="renewable-energy-powering-future",
                img_file="renewable_energy",
                date=today_str,
                content=(
                    "The global energy landscape is undergoing a massive transformation. Solar panels "
                    "are cheaper than ever, wind farms are springing up across coastlines, and countries "
                    "are setting ambitious targets to phase out fossil fuels entirely. Renewable energy "
                    "isn't just an environmental choice anymore — it's becoming the economically "
                    "smart one.\n\n"
                    "In this post, we take a closer look at the major renewable energy sources, "
                    "compare their efficiency and scalability, and explore the technological "
                    "breakthroughs that are making clean energy a viable replacement for coal, "
                    "oil, and natural gas."
                )
            ),
            Posts(
                title="Stock Market Basics: A Beginner's Roadmap",
                sub_heading="Demystifying stocks, indices, and investment strategies",
                slug="stock-market-basics-beginners-roadmap",
                img_file="stock-bg",
                date=today_str,
                content=(
                    "The stock market can seem intimidating at first — ticker symbols, candlestick "
                    "charts, bull and bear markets. But at its core, investing in stocks is simply "
                    "buying a small piece of ownership in a company. Understanding the fundamentals "
                    "can help you make informed decisions and grow your wealth over time.\n\n"
                    "This post covers the essentials: what stocks are, how exchanges work, the "
                    "difference between growth and value investing, and practical tips for "
                    "beginners looking to start their investment journey without getting burned."
                )
            ),
            Posts(
                title="Life on Mars: The Dream of a Multi-Planetary Species",
                sub_heading="Exploring the challenges and possibilities of colonizing the Red Planet",
                slug="life-on-mars-multi-planetary-species",
                img_file="mars_colony",
                date=today_str,
                content=(
                    "For decades, Mars has captivated the human imagination. From science fiction "
                    "novels to NASA's rovers and SpaceX's ambitious Starship program, the idea of "
                    "establishing a human presence on the Red Planet is closer to reality than ever "
                    "before. But the challenges are enormous — radiation, thin atmosphere, freezing "
                    "temperatures, and a journey that takes months.\n\n"
                    "In this post, we dive into the current state of Mars exploration, the "
                    "technologies being developed to sustain human life there, and the philosophical "
                    "question of why becoming a multi-planetary species might be humanity's most "
                    "important endeavor."
                )
            ),
        ]
        db.session.bulk_save_objects(default_posts)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)