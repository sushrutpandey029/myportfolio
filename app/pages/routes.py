"""
Pages Routes Module
Handles public-facing page routes:
- Home Page
- About Page
- Blog Listing & Details
- Policy Pages (Privacy, Terms, Cookies)
"""

# =========================================
# THIRD-PARTY IMPORTS
# =========================================
from flask import render_template, abort

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.pages import pages
from app.models.home_content import HomeContent
from app.models.about_content import AboutContent
from app.models.home_page import Skill, TeamMember
from app.models.blog_post import BlogPost


# =========================================
# HOME PAGE ROUTE
# =========================================

@pages.route("/")
def home():
    """Render home page with dynamic content, skills, and team members"""
    content = HomeContent.get_content()
    skills = Skill.query.filter_by(is_active=True).order_by(Skill.order, Skill.id).all()
    team_members = TeamMember.query.filter_by(is_active=True).order_by(TeamMember.order, TeamMember.id).all()
    return render_template('pages/home.html', title='Home', content=content, skills=skills, team_members=team_members)


# =========================================
# ABOUT PAGE ROUTE
# =========================================

@pages.route("/about")
def about():
    """Render about page with dynamic content"""
    content = AboutContent.get_content()
    return render_template('pages/about.html', title='About', content=content)


# =========================================
# CONTACT PAGE ROUTE
# =========================================

@pages.route("/contact")
def contact():
    """Render contact page"""
    return render_template('pages/contact.html', title='Contact Us')


# =========================================
# BLOG ROUTES
# =========================================

@pages.route("/blog")
def blog():
    """Render blog listing page with all active posts"""
    posts = BlogPost.query.filter_by(is_active=True).order_by(BlogPost.created_at.desc()).all()
    return render_template('pages/blog.html', title='Blog', posts=posts)


@pages.route("/blog/<int:blog_id>")
def blog_detail(blog_id):
    """Render individual blog post detail page"""
    post = BlogPost.query.get_or_404(blog_id)
    if not post.is_active:
        abort(404)
    return render_template('pages/blog_detail.html', title=post.title, post=post)


# =========================================
# POLICY PAGES ROUTES
# =========================================

@pages.route("/privacy")
def privacy():
    """Render privacy policy page"""
    return render_template('pages/privacy.html', title='Privacy Policy')


@pages.route("/terms")
def terms():
    """Render terms of service page"""
    return render_template('pages/terms.html', title='Terms of Service')


@pages.route("/cookies")
def cookies():
    """Render cookie policy page"""
    return render_template('pages/cookies.html', title='Cookie Policy')