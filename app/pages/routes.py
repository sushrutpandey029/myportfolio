from flask import render_template
from app.pages import pages
from app.models.home_content import HomeContent
from app.models.about_content import AboutContent
from app.models.home_page import Skill, TeamMember

@pages.route("/")
def home():
    content = HomeContent.get_content()
    skills = Skill.query.filter_by(is_active=True).order_by(Skill.order, Skill.id).all()
    team_members = TeamMember.query.filter_by(is_active=True).order_by(TeamMember.order, TeamMember.id).all()
    return render_template('pages/home.html', title='Home', content=content, skills=skills, team_members=team_members)

@pages.route("/about")
def about():
    content = AboutContent.get_content()
    return render_template('pages/about.html', title='About', content=content)

@pages.route("/contact")
def contact():
    return render_template('pages/contact.html', title='Contact Us')

from app.models.blog_post import BlogPost

@pages.route("/blog")
def blog():
    posts = BlogPost.query.filter_by(is_active=True).order_by(BlogPost.created_at.desc()).all()
    return render_template('pages/blog.html', title='Blog', posts=posts)


@pages.route("/blog/<int:blog_id>")
def blog_detail(blog_id):
    post = BlogPost.query.get_or_404(blog_id)
    if not post.is_active:
        from flask import abort
        abort(404)
    return render_template('pages/blog_detail.html', title=post.title, post=post)

@pages.route("/privacy")
def privacy():
    return render_template('pages/privacy.html', title='Privacy Policy')

@pages.route("/terms")
def terms():
    return render_template('pages/terms.html', title='Terms of Service')

@pages.route("/cookies")
def cookies():
    return render_template('pages/cookies.html', title='Cookie Policy')