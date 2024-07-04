"""
Database bootstrap and initial seeding utilities for Coding Thunder.

Handles 3-tier self-healing startup:
1. Auto-creates MySQL database if it doesn't exist.
2. Auto-creates tables (Contacts, Posts) if they don't exist.
3. Seeds 5 default themed technical posts if posts table is empty.
"""

from datetime import datetime
import sqlalchemy
from sqlalchemy.engine.url import make_url


def ensure_database_exists(app):
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


def init_db(app, db, Posts):
    """
    Performs 3-tier emergency database initialization:
    - Creates database if missing.
    - Creates all tables.
    - Seeds 5 default themed technical posts if the posts table is empty.
    """
    with app.app_context():
        # 1. Emergency bootstrap: automatically creates the database itself if missing on MySQL.
        ensure_database_exists(app)

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
