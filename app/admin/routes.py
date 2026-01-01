from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.admin import admin_bp
from app.admin.forms import ServiceForm, ProjectForm, StudyMaterialForm, YouTubeVideoForm, YouTubeCategoryForm, InquiryForm, HomeContentForm, AboutContentForm, SkillForm, TeamMemberForm
from app.models.user import User
from app.models.service import Service
from app.models.service_category import ServiceCategory
from app.models.project import Project
from app.models.project_category import ProjectCategory
from app.models.study_material import StudyMaterial
from app.models.study_material_category import StudyMaterialCategory
from app.models.youtube_video import YouTubeVideo
from app.models.youtube_category import YouTubeCategory
from app.models.inquiry import Inquiry
from app.models.home_content import HomeContent
from app.models.about_content import AboutContent
from app.models.home_page import Skill, TeamMember
from app.models.skill_category import SkillCategory
from app.models.blog_post import BlogPost
from app.models.blog_category import BlogCategory
from app.admin.forms import ServiceCategoryForm, ProjectCategoryForm, SkillCategoryForm, StudyMaterialCategoryForm, BlogPostForm, BlogCategoryForm
from app.utils.helpers import save_image
from app.utils.decorators import admin_required
from app.utils.constants import ROLE_ADMIN, ROLE_USER

@admin_bp.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    # Get counts for dashboard
    user_count = User.query.count()
    service_count = Service.query.count()
    project_count = Project.query.count()
    material_count = StudyMaterial.query.count()
    video_count = YouTubeVideo.query.count()
    inquiry_count = Inquiry.query.count()
    blog_count = BlogPost.query.count()
    skill_count = Skill.query.count()
    team_count = TeamMember.query.count()
    
    # Get recent inquiries
    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          title='Admin Dashboard',
                          user_count=user_count,
                          service_count=service_count,
                          project_count=project_count,
                          material_count=material_count,
                          video_count=video_count,
                          inquiry_count=inquiry_count,
                          blog_count=blog_count,
                          skill_count=skill_count,
                          team_count=team_count,
                          recent_inquiries=recent_inquiries)

# Users management
@admin_bp.route("/admin/users")
@login_required
@admin_required
def admin_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/users.html', title='Manage Users', users=users)

@admin_bp.route("/admin/user/<int:user_id>/toggle-status", methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == ROLE_ADMIN and user.id == current_user.id:
        flash('You cannot deactivate your own admin account!', 'danger')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        status = "activated" if user.is_active else "deactivated"
        flash(f'User {user.username} has been {status}.', 'success')
    return redirect(url_for('admin_bp.admin_users'))

from app.admin.forms import UserForm

@admin_bp.route("/admin/users/new", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_user_new():
    form = UserForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.', 'danger')
        elif User.query.filter_by(username=form.username.data).first():
            flash('Username already taken.', 'danger')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                role=form.role.data
            )
            db.session.add(user)
            db.session.commit()
            flash(f'New {form.role.data} account created for {user.username}!', 'success')
            return redirect(url_for('admin_bp.admin_users'))
            
    return render_template('admin/user_form.html', title='Add Admin User', form=form)

# Services management
@admin_bp.route("/admin/services", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_services():
    # Category Form Handling (Quick Add)
    cat_form = ServiceCategoryForm()
    if cat_form.validate_on_submit():
        category = ServiceCategory(name=cat_form.name.data, description=cat_form.description.data)
        db.session.add(category)
        db.session.commit()
        flash(f'Category "{category.name}" created successfully!', 'success')
        return redirect(url_for('admin_bp.admin_services'))

    page = request.args.get('page', 1, type=int)
    services = Service.query.order_by(Service.created_at.desc()).paginate(page=page, per_page=10)
    categories = ServiceCategory.query.all()
    
    return render_template('admin/services.html', 
                         title='Manage Services', 
                         services=services, 
                         categories=categories,
                         cat_form=cat_form)

@admin_bp.route("/admin/service/new", methods=['GET', 'POST'])
@admin_bp.route("/admin/service/<int:service_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_service_form(service_id=None):
    service = Service.query.get_or_404(service_id) if service_id else None
    form = ServiceForm(obj=service)
    
    # Populate category choices
    categories = ServiceCategory.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        if not service:
            service = Service()
            db.session.add(service)
            
        if form.image.data:
            image_file = save_image(form.image.data, folder='services')
            service.image_url = image_file
        else:
            # If editing and no new image, we keep the old one
            # populate_obj would set it to None if not handled
            pass
            
        form.populate_obj(service)
        # Note: form.populate_obj(service) might overwrite image_url with the FileField object if not careful
        # But our field name in form is 'image' and in model is 'image_url', so it should be fine.
        
        service.is_active = form.is_active.data == 'True'
        
        # Ensure we set the user_id if it's a new service
        if not service.user_id:
            service.user_id = current_user.id
            
        db.session.commit()
        flash('Service saved successfully!', 'success')
        return redirect(url_for('admin_bp.admin_services'))
        
    return render_template('admin/service_form.html', title='Edit Service' if service else 'New Service', form=form, service=service)

# Category management
@admin_bp.route("/admin/categories")
@login_required
@admin_required
def admin_categories():
    categories = ServiceCategory.query.all()
    return render_template('admin/categories.html', title='Manage Categories', categories=categories)

@admin_bp.route("/admin/category/new", methods=['GET', 'POST'])
@admin_bp.route("/admin/category/<int:category_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_category_form(category_id=None):
    category = ServiceCategory.query.get_or_404(category_id) if category_id else None
    form = ServiceCategoryForm(obj=category)
    
    if form.validate_on_submit():
        if not category:
            category = ServiceCategory()
            db.session.add(category)
        
        form.populate_obj(category)
        db.session.commit()
        flash('Category saved successfully!', 'success')
        return redirect(url_for('admin_bp.admin_categories'))
        
    return render_template('admin/category_form.html', title='Edit Category' if category else 'New Category', form=form, category=category)

@admin_bp.route("/admin/category/<int:category_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    category = ServiceCategory.query.get_or_404(category_id)
    # Check if category has services
    if category.services:
        flash(f'Cannot delete category "{category.name}" as it contains services. Move them first.', 'danger')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_categories'))

@admin_bp.route("/admin/service/<int:service_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Service deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_services'))

# Projects management
@admin_bp.route("/admin/projects", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_projects():
    # Category Form Handling (Quick Add)
    cat_form = ProjectCategoryForm()
    if cat_form.validate_on_submit():
        category = ProjectCategory(name=cat_form.name.data, description=cat_form.description.data)
        db.session.add(category)
        db.session.commit()
        flash(f'Category "{category.name}" created successfully!', 'success')
        return redirect(url_for('admin_bp.admin_projects'))

    page = request.args.get('page', 1, type=int)
    projects = Project.query.order_by(Project.created_at.desc()).paginate(page=page, per_page=10)
    categories = ProjectCategory.query.all()
    
    return render_template('admin/projects.html', 
                         title='Manage Projects', 
                         projects=projects, 
                         categories=categories,
                         cat_form=cat_form)

@admin_bp.route("/admin/project/new", methods=['GET', 'POST'])
@admin_bp.route("/admin/project/<int:project_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_project_form(project_id=None):
    project = Project.query.get_or_404(project_id) if project_id else None
    form = ProjectForm(obj=project)
    
    # Populate category choices
    categories = ProjectCategory.query.all()
    form.category_id.choices = [(0, 'Select Category')] + [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        if not project:
            project = Project()
            db.session.add(project)
        
        # Handle image upload
        if form.image.data:
            image_file = save_image(form.image.data, folder='projects')
            project.image_url = image_file
        
        # Handle project file upload
        if form.file.data:
            from werkzeug.utils import secure_filename
            import os
            filename = secure_filename(form.file.data.filename)
            upload_folder = os.path.join('app', 'static', 'uploads', 'project_files')
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join('uploads', 'project_files', filename)
            form.file.data.save(os.path.join('app', 'static', file_path))
            project.file_path = file_path
            
        form.populate_obj(project)
        
        # Handle category_id - set to None if 0 (which means 'Select Category')
        if form.category_id.data == 0:
            project.category_id = None
            
        project.is_active = form.is_active.data == 'True'
        db.session.commit()
        flash('Project saved successfully!', 'success')
        return redirect(url_for('admin_bp.admin_projects'))
        
    return render_template('admin/project_form.html', title='Edit Project' if project else 'New Project', form=form, project=project)

@admin_bp.route("/admin/project/<int:project_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_projects'))

# Project Category management
@admin_bp.route("/admin/project-category/<int:category_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_project_category_form(category_id):
    category = ProjectCategory.query.get_or_404(category_id)
    form = ProjectCategoryForm(obj=category)
    
    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_bp.admin_projects'))
        
    return render_template('admin/project_category_form.html', title='Edit Category', form=form, category=category)

@admin_bp.route("/admin/project-category/<int:category_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_project_category(category_id):
    category = ProjectCategory.query.get_or_404(category_id)
    # Check if category has projects
    if category.projects:
        flash(f'Cannot delete category "{category.name}" as it contains projects. Move them first.', 'danger')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_projects'))

# Study materials management
@admin_bp.route("/admin/materials")
@login_required
@admin_required
def admin_materials():
    page = request.args.get('page', 1, type=int)
    materials = StudyMaterial.query.order_by(StudyMaterial.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/study_material.html', title='Manage Study Materials', materials=materials)

@admin_bp.route("/admin/material/new", methods=['GET', 'POST'])
@admin_bp.route("/admin/material/<int:material_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_material_form(material_id=None):
    material = StudyMaterial.query.get_or_404(material_id) if material_id else None
    form = StudyMaterialForm(obj=material)
    
    # Populate category choices
    categories = StudyMaterialCategory.query.all()
    form.category.choices = [(c.name, c.name) for c in categories]
    
    if form.validate_on_submit():
        if not material:
            material = StudyMaterial()
            db.session.add(material)
            
        # Store existing thumbnail path to prevent overwrite by populate_obj
        current_thumbnail = material.thumbnail
        current_file_path = material.file_path
            
        form.populate_obj(material)
        
        # Restore paths (populate_obj might have put FileStorage objects or None)
        material.thumbnail = current_thumbnail
        material.file_path = current_file_path
        
        # Handle file upload (PDF)
        if form.file.data:
            import os
            from werkzeug.utils import secure_filename
            filename = secure_filename(form.file.data.filename)
            # Use timestamp to make unique? or safe_image helper?
            # Helper logic:
            upload_folder = os.path.join('app', 'static', 'uploads', 'materials')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Simple unique checking or overwrite?
            # Let's just prepend random hex to be safe like save_image
            import secrets
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(filename)
            new_filename = random_hex + f_ext
            
            file_path = os.path.join('uploads', 'materials', new_filename)
            form.file.data.save(os.path.join('app', 'static', file_path))
            material.file_path = file_path
            
        # Handle thumbnail upload
        if form.thumbnail.data:
            # save_image handles unique naming
            image_file = save_image(form.thumbnail.data, folder='materials_thumbs')
            material.thumbnail = image_file
            
        material.is_active = form.is_active.data == 'True'
        db.session.commit()
        flash('Study material saved successfully!', 'success')
        return redirect(url_for('admin_bp.admin_materials'))
        
    return render_template('admin/material_form.html', title='Edit Study Material' if material else 'New Study Material', form=form, material=material)

@admin_bp.route("/admin/material/<int:material_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_material(material_id):
    material = StudyMaterial.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash('Study material deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_materials'))

# Study Material Categories
@admin_bp.route("/admin/material-categories")
@login_required
@admin_required
def admin_material_categories():
    categories = StudyMaterialCategory.query.all()
    return render_template('admin/material_categories.html', title='Manage Categories', categories=categories)

@admin_bp.route("/admin/material-category/new", methods=['GET', 'POST'])
@admin_bp.route("/admin/material-category/<int:category_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_material_category_form(category_id=None):
    category = StudyMaterialCategory.query.get_or_404(category_id) if category_id else None
    form = StudyMaterialCategoryForm(obj=category)
    
    if form.validate_on_submit():
        if not category:
            category = StudyMaterialCategory()
            db.session.add(category)
            
        form.populate_obj(category)
        db.session.commit()
        flash('Category saved successfully!', 'success')
        return redirect(url_for('admin_bp.admin_material_categories'))
        
    return render_template('admin/material_category_form.html', title='Edit Category' if category else 'New Category', form=form, category=category)

@admin_bp.route("/admin/material-category/<int:category_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_material_category(category_id):
    category = StudyMaterialCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_material_categories'))

# YouTube videos management
@admin_bp.route("/admin/videos")
@login_required
@admin_required
def admin_videos():
    page = request.args.get('page', 1, type=int)
    videos = YouTubeVideo.query.order_by(YouTubeVideo.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/youtube_videos.html', title='Manage YouTube Videos', videos=videos)

@admin_bp.route("/admin/video/new", methods=['GET', 'POST'])
@admin_bp.route("/admin/video/<int:video_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_video_form(video_id=None):
    video = YouTubeVideo.query.get_or_404(video_id) if video_id else None
    form = YouTubeVideoForm(obj=video)
    
    # Populate category choices
    categories = YouTubeCategory.query.all()
    form.category.choices = [(c.name, c.name) for c in categories]
    
    # Pre-populate URL if editing
    if request.method == 'GET' and video and video.video_id:
        form.video_url.data = f"https://www.youtube.com/watch?v={video.video_id}"
    
    if form.validate_on_submit():
        if not video:
            video = YouTubeVideo()
            db.session.add(video)
            
        form.populate_obj(video)
        
        # Extract ID from URL
        import re
        url = form.video_url.data
        # Robust regex for different YouTube URL formats
        video_id_match = re.search(r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})', url)
        
        if video_id_match:
             video.video_id = video_id_match.group(1)
        elif len(url) == 11: # Assume raw ID if 11 chars
             video.video_id = url
        else:
             flash('Invalid YouTube URL. Please provide a valid link.', 'error')
             return render_template('admin/video_form.html', title='Edit YouTube Video' if video else 'New YouTube Video', form=form, video=video)

        video.is_active = form.is_active.data == 'True'
        db.session.commit()
        flash('YouTube video saved successfully!', 'success')
        return redirect(url_for('admin_bp.admin_videos'))
        
    return render_template('admin/video_form.html', title='Edit YouTube Video' if video else 'New YouTube Video', form=form, video=video)

@admin_bp.route("/admin/video/<int:video_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_video(video_id):
    video = YouTubeVideo.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    flash('YouTube video deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_videos'))

# YouTube Categories Management
@admin_bp.route("/admin/youtube-categories")
@login_required
@admin_required
def admin_youtube_categories():
    categories = YouTubeCategory.query.all()
    return render_template('admin/youtube_categories.html', title='Manage YouTube Categories', categories=categories)

@admin_bp.route("/admin/youtube-category/new", methods=['GET', 'POST'])
@admin_bp.route("/admin/youtube-category/<int:category_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_youtube_category_form(category_id=None):
    category = YouTubeCategory.query.get_or_404(category_id) if category_id else None
    form = YouTubeCategoryForm(obj=category)
    
    if form.validate_on_submit():
        if not category:
            category = YouTubeCategory()
            db.session.add(category)
        else:
            # If editing and name changed, update all associated videos
            if category.name != form.name.data:
                YouTubeVideo.query.filter_by(category=category.name).update({'category': form.name.data})
            
        form.populate_obj(category)
        db.session.commit()
        flash('Category saved successfully!', 'success')
        return redirect(url_for('admin_bp.admin_youtube_categories'))
        
    return render_template('admin/youtube_category_form.html', title='Edit Category' if category else 'New Category', form=form, category=category)

@admin_bp.route("/admin/youtube-category/<int:category_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_youtube_category(category_id):
    category = YouTubeCategory.query.get_or_404(category_id)
    if YouTubeVideo.query.filter_by(category=category.name).first():
        flash(f'Cannot delete category "{category.name}" as it is assigned to videos.', 'error')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_youtube_categories'))

# Inquiries management
@admin_bp.route("/admin/inquiries")
@login_required
@admin_required
def admin_inquiries():
    page = request.args.get('page', 1, type=int)
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/inquiries.html', title='Manage Inquiries', inquiries=inquiries)

@admin_bp.route("/admin/inquiry/<int:inquiry_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_inquiry_form(inquiry_id):
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    form = InquiryForm(obj=inquiry)
    
    if form.validate_on_submit():
        inquiry.status = form.status.data
        db.session.commit()
        flash('Inquiry updated successfully!', 'success')
        return redirect(url_for('admin_bp.admin_inquiries'))
        
    return render_template('admin/inquiry_form.html', title='Edit Inquiry', form=form, inquiry=inquiry)

@admin_bp.route("/admin/inquiry/<int:inquiry_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_inquiry(inquiry_id):
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    db.session.delete(inquiry)
    db.session.commit()
    flash('Inquiry deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_inquiries'))

# Content management - About Page View (Preview)
@admin_bp.route("/admin/content/home-about")
@login_required
@admin_required
def admin_content_home_about():
    content = AboutContent.get_content()
    return render_template('admin/about_page_content_view.html', 
                         title='About Page Content', 
                         content=content)

# Content management - About Page Edit
@admin_bp.route("/admin/content/home-about/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_content_about_edit():
    content = AboutContent.get_content()
    form = AboutContentForm(obj=content)
    
    if form.validate_on_submit():
        # Handle Hero Image Upload
        if form.hero_image.data:
            image_file = save_image(form.hero_image.data, folder='about')
            content.hero_image_url = image_file
        
        # Hero Section
        content.hero_title = form.hero_title.data
        content.hero_subtitle = form.hero_subtitle.data
        content.hero_stat_1_count = form.hero_stat_1_count.data
        content.hero_stat_1_label = form.hero_stat_1_label.data
        content.hero_stat_2_count = form.hero_stat_2_count.data
        content.hero_stat_2_label = form.hero_stat_2_label.data
        content.hero_stat_3_count = form.hero_stat_3_count.data
        content.hero_stat_3_label = form.hero_stat_3_label.data
        
        # Mission Section
        content.mission_title = form.mission_title.data
        content.mission_content = form.mission_content.data
        
        # Vision Section
        content.vision_title = form.vision_title.data
        content.vision_content = form.vision_content.data
        
        # Values Section
        content.values_title = form.values_title.data
        content.value1_title = form.value1_title.data
        content.value1_description = form.value1_description.data
        content.value2_title = form.value2_title.data
        content.value2_description = form.value2_description.data
        content.value3_title = form.value3_title.data
        content.value3_description = form.value3_description.data
        content.value4_title = form.value4_title.data
        content.value4_description = form.value4_description.data
        content.value5_title = form.value5_title.data
        content.value5_description = form.value5_description.data
        content.value6_title = form.value6_title.data
        content.value6_description = form.value6_description.data
        
        # Story Section
        content.story_title = form.story_title.data
        content.story_content = form.story_content.data
        
        # Timeline Section
        content.timeline_year_1 = form.timeline_year_1.data
        content.timeline_title_1 = form.timeline_title_1.data
        content.timeline_content_1 = form.timeline_content_1.data
        content.timeline_year_2 = form.timeline_year_2.data
        content.timeline_title_2 = form.timeline_title_2.data
        content.timeline_content_2 = form.timeline_content_2.data
        content.timeline_year_3 = form.timeline_year_3.data
        content.timeline_title_3 = form.timeline_title_3.data
        content.timeline_content_3 = form.timeline_content_3.data
        content.timeline_year_4 = form.timeline_year_4.data
        content.timeline_title_4 = form.timeline_title_4.data
        content.timeline_content_4 = form.timeline_content_4.data
        
        # Team Section
        content.team_title = form.team_title.data
        content.team_subtitle = form.team_subtitle.data
        
        # CTA Section
        content.cta_title = form.cta_title.data
        content.cta_subtitle = form.cta_subtitle.data
        content.cta_button_text = form.cta_button_text.data
        content.cta_button_link = form.cta_button_link.data
        content.cta_button_2_text = form.cta_button_2_text.data
        content.cta_button_2_link = form.cta_button_2_link.data
        
        db.session.commit()
        flash('About page content updated successfully!', 'success')
        return redirect(url_for('admin_bp.admin_content_home_about'))
        
    return render_template('admin/about_page_content.html', 
                         title='Edit About Page', 
                         form=form, 
                         content=content)

# Home Page Content Management - View (Preview)
@admin_bp.route("/admin/content/home-page")
@login_required
@admin_required
def admin_content_home_page():
    content = HomeContent.get_content()
    return render_template('admin/home_page_content_view.html', 
                         title='Home Page Content', 
                         content=content)

# Home Page Content Management - Edit
@admin_bp.route("/admin/content/home-page/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_home_page():
    content = HomeContent.get_content()
    form = HomeContentForm(obj=content)
    
    if form.validate_on_submit():
        # Handle profile image upload
        if form.profile_image.data and not isinstance(form.profile_image.data, str):
            image_file = save_image(form.profile_image.data, folder='profile')
            content.profile_image = image_file
        
        # Update all fields except profile_image (already handled above)
        content.hero_title_line1 = form.hero_title_line1.data
        content.hero_title_line2 = form.hero_title_line2.data
        content.hero_subtitle = form.hero_subtitle.data
        content.stat_projects = form.stat_projects.data
        content.stat_materials = form.stat_materials.data
        content.stat_team = form.stat_team.data
        content.stat_downloads = form.stat_downloads.data
        content.knowledge_hub_title = form.knowledge_hub_title.data
        content.knowledge_hub_subtitle = form.knowledge_hub_subtitle.data
        content.workflow_title = form.workflow_title.data
        content.workflow_subtitle = form.workflow_subtitle.data
        content.cv_button_text = form.cv_button_text.data
        content.cv_button_link = form.cv_button_link.data
        content.hire_button_text = form.hire_button_text.data
        
        db.session.commit()
        flash('Home page content updated successfully!', 'success')
        return redirect(url_for('admin_bp.admin_content_home_page'))
    
    return render_template('admin/home_page_content.html', 
                         title='Edit Home Page', 
                         form=form, 
                         content=content)

# Skills Management
@admin_bp.route("/admin/skills", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_skills():
    # Category Form Handling (Quick Add)
    cat_form = SkillCategoryForm()
    if cat_form.validate_on_submit():
        category = SkillCategory(name=cat_form.name.data, description=cat_form.description.data)
        db.session.add(category)
        db.session.commit()
        flash(f'Skill Category "{category.name}" created successfully!', 'success')
        return redirect(url_for('admin_bp.admin_skills'))
    
    skills = Skill.query.order_by(Skill.order, Skill.id).all()
    categories = SkillCategory.query.all()
    
    return render_template('admin/skills_list.html', 
                         title='Manage Skills', 
                         skills=skills,
                         categories=categories,
                         cat_form=cat_form)

@admin_bp.route("/admin/skills/create", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_skill_create():
    form = SkillForm()
    
    if form.validate_on_submit():
        skill = Skill(
            name=form.name.data,
            category=form.category.data,
            percentage=int(form.percentage.data),
            icon_text=form.icon_text.data,
            color=form.color.data,
            order=int(form.order.data) if form.order.data else 0,
            is_active=form.is_active.data == 'True'
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('admin_bp.admin_skills'))
    
    return render_template('admin/skill_form.html', 
                         title='Add Skill', 
                         form=form,
                         action='Create')

@admin_bp.route("/admin/skills/edit/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_skill_edit(id):
    skill = Skill.query.get_or_404(id)
    form = SkillForm(obj=skill)
    
    # Pre-populate form with current values
    if request.method == 'GET':
        form.percentage.data = str(skill.percentage)
        form.order.data = str(skill.order)
        form.is_active.data = 'True' if skill.is_active else 'False'
    
    if form.validate_on_submit():
        skill.name = form.name.data
        skill.category = form.category.data
        skill.percentage = int(form.percentage.data)
        skill.icon_text = form.icon_text.data
        skill.color = form.color.data
        skill.order = int(form.order.data) if form.order.data else 0
        skill.is_active = form.is_active.data == 'True'
        
        db.session.commit()
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('admin_bp.admin_skills'))
    
    return render_template('admin/skill_form.html', 
                         title='Edit Skill', 
                         form=form,
                         skill=skill,
                         action='Update')


@admin_bp.route("/admin/skills/delete/<int:id>", methods=['POST'])
@login_required
@admin_required
def admin_skill_delete(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_skills'))

# Skill Category Management
@admin_bp.route("/admin/skill-category/<int:category_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_skill_category_edit(category_id):
    category = SkillCategory.query.get_or_404(category_id)
    form = SkillCategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        db.session.commit()
        flash(f'Skill Category "{category.name}" updated successfully!', 'success')
        return redirect(url_for('admin_bp.admin_skills'))
    
    return render_template('admin/skill_category_form.html', 
                         title='Edit Skill Category', 
                         form=form, 
                         category=category)

@admin_bp.route("/admin/skill-category/<int:category_id>/delete", methods=['POST'])
@login_required
@admin_required
def admin_skill_category_delete(category_id):
    category = SkillCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash(f'Skill Category "{category.name}" deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_skills'))


# ============================================
# Team Members Management Routes
# ============================================

@admin_bp.route("/admin/team-members", methods=['GET'])
@login_required
@admin_required
def admin_team_members():
    team_members = TeamMember.query.order_by(TeamMember.order, TeamMember.id).all()
    return render_template('admin/team_members_list.html', 
                         title='Manage Team Members', 
                         team_members=team_members)

@admin_bp.route("/admin/team-members/create", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_team_member_create():
    form = TeamMemberForm()
    
    if form.validate_on_submit():
        # Handle image - priority to upload over URL
        image_url = form.image_url.data
        if form.image_upload.data:
            # Save uploaded image
            image_url = save_image(form.image_upload.data, folder='team')
        elif not image_url:
            flash('Please provide either an image upload or image URL', 'error')
            return render_template('admin/team_member_form.html', 
                                 title='Add Team Member', 
                                 form=form,
                                 action='Add')
        
        team_member = TeamMember(
            name=form.name.data,
            position=form.position.data,
            bio=form.bio.data,
            image_url=image_url,
            linkedin_url=form.linkedin_url.data,
            twitter_url=form.twitter_url.data,
            github_url=form.github_url.data,
            dribbble_url=form.dribbble_url.data,
            behance_url=form.behance_url.data,
            order=int(form.order.data) if form.order.data else 0,
            is_active=form.is_active.data == 'True'
        )
        db.session.add(team_member)
        db.session.commit()
        flash('Team member added successfully!', 'success')
        return redirect(url_for('admin_bp.admin_team_members'))
    
    return render_template('admin/team_member_form.html', 
                         title='Add Team Member', 
                         form=form,
                         action='Add')

@admin_bp.route("/admin/team-members/edit/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_team_member_edit(id):
    team_member = TeamMember.query.get_or_404(id)
    form = TeamMemberForm(obj=team_member)
    
    # Pre-populate form with current values
    if request.method == 'GET':
        form.order.data = str(team_member.order)
        form.is_active.data = 'True' if team_member.is_active else 'False'
    
    if form.validate_on_submit():
        # Handle image upload
        if form.image_upload.data:
            team_member.image_url = save_image(form.image_upload.data, folder='team')
        elif form.image_url.data:
            team_member.image_url = form.image_url.data
        
        team_member.name = form.name.data
        team_member.position = form.position.data
        team_member.bio = form.bio.data
        team_member.linkedin_url = form.linkedin_url.data
        team_member.twitter_url = form.twitter_url.data
        team_member.github_url = form.github_url.data
        team_member.dribbble_url = form.dribbble_url.data
        team_member.behance_url = form.behance_url.data
        team_member.order = int(form.order.data) if form.order.data else 0
        team_member.is_active = form.is_active.data == 'True'
        
        db.session.commit()
        flash('Team member updated successfully!', 'success')
        return redirect(url_for('admin_bp.admin_team_members'))
    
    return render_template('admin/team_member_form.html', 
                         title='Edit Team Member', 
                         form=form,
                         team_member=team_member,
                         action='Update')

@admin_bp.route("/admin/team-members/delete/<int:id>", methods=['POST'])
@login_required
@admin_required
def admin_team_member_delete(id):
    team_member = TeamMember.query.get_or_404(id)
    db.session.delete(team_member)
    db.session.commit()
    flash('Team member deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_team_members'))
# Team Member Management
@admin_bp.route("/admin/team", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_team():
    team_members = TeamMember.query.order_by(TeamMember.order, TeamMember.id).all()
    return render_template('admin/team_list.html', title='Manage Team', team_members=team_members)

@admin_bp.route("/admin/team/create", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_team_create():
    form = TeamMemberForm()
    if form.validate_on_submit():
        member = TeamMember(
            name=form.name.data,
            position=form.position.data,
            bio=form.bio.data,
            image_url=form.image_url.data,
            linkedin_url=form.linkedin_url.data,
            twitter_url=form.twitter_url.data,
            github_url=form.github_url.data,
            dribbble_url=form.dribbble_url.data,
            behance_url=form.behance_url.data,
            order=int(form.order.data) if form.order.data else 0,
            is_active=form.is_active.data == 'True'
        )
        
        if form.image_upload.data:
            image_file = save_image(form.image_upload.data, folder='team')
            member.image_url = image_file
            
        db.session.add(member)
        db.session.commit()
        flash('Team member added successfully!', 'success')
        return redirect(url_for('admin_bp.admin_team'))
        
    return render_template('admin/team_form.html', title='Add Team Member', form=form, action='Create')

@admin_bp.route("/admin/team/edit/<int:id>", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_team_edit(id):
    member = TeamMember.query.get_or_404(id)
    form = TeamMemberForm(obj=member)
    
    if request.method == 'GET':
        form.order.data = str(member.order)
        form.is_active.data = 'True' if member.is_active else 'False'
        
    if form.validate_on_submit():
        form.populate_obj(member)
        member.order = int(form.order.data) if form.order.data else 0
        member.is_active = form.is_active.data == 'True'
        
        if form.image_upload.data:
            image_file = save_image(form.image_upload.data, folder='team')
            member.image_url = image_file
            
        db.session.commit()
        flash('Team member updated successfully!', 'success')
        return redirect(url_for('admin_bp.admin_team'))
        
    return render_template('admin/team_form.html', title='Edit Team Member', form=form, member=member, action='Update')

@admin_bp.route("/admin/team/delete/<int:id>", methods=['POST'])
@login_required
@admin_required
def admin_team_delete(id):
    member = TeamMember.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Team member deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_team'))


# Blog Management
@admin_bp.route("/admin/blogs")
@login_required
@admin_required
def admin_blogs():
    page = request.args.get('page', 1, type=int)
    blogs = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('admin/blogs.html', title='Manage Blogs', blogs=blogs)

@admin_bp.route("/admin/blog/new", methods=['GET', 'POST'])
@admin_bp.route("/admin/blog/<int:blog_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_blog_form(blog_id=None):
    blog = BlogPost.query.get_or_404(blog_id) if blog_id else None
    form = BlogPostForm(obj=blog)
    
    # Populate category choices
    categories = BlogCategory.query.all()
    form.category.choices = [(c.name, c.name) for c in categories]
    
    if form.validate_on_submit():
        if not blog:
            blog = BlogPost()
            db.session.add(blog)
            
        current_thumbnail = blog.thumbnail
        form.populate_obj(blog)
        blog.thumbnail = current_thumbnail # Restore to handle file upload manually
        
        if form.thumbnail.data:
            image_file = save_image(form.thumbnail.data, folder='blog_thumbs')
            blog.thumbnail = image_file
            
        blog.is_active = form.is_active.data == 'True'
        db.session.commit()
        flash('Blog post saved successfully!', 'success')
        return redirect(url_for('admin_bp.admin_blogs'))
        
    return render_template('admin/blog_form.html', title='Edit Blog Post' if blog else 'New Blog Post', form=form, blog=blog)

@admin_bp.route("/admin/blog/<int:blog_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_blog(blog_id):
    blog = BlogPost.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    flash('Blog post deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_blogs'))


# Blog Categories Management
@admin_bp.route("/admin/blog-categories")
@login_required
@admin_required
def admin_blog_categories():
    categories = BlogCategory.query.all()
    return render_template('admin/blog_categories.html', title='Manage Blog Categories', categories=categories)

@admin_bp.route("/admin/blog-category/new", methods=['GET', 'POST'])
@admin_bp.route("/admin/blog-category/<int:category_id>/edit", methods=['GET', 'POST'])
@login_required
@admin_required
def admin_blog_category_form(category_id=None):
    category = BlogCategory.query.get_or_404(category_id) if category_id else None
    form = BlogCategoryForm(obj=category)
    
    if form.validate_on_submit():
        if not category:
            category = BlogCategory()
            db.session.add(category)
            
        form.populate_obj(category)
        db.session.commit()
        flash('Category saved successfully!', 'success')
        return redirect(url_for('admin_bp.admin_blog_categories'))
        
    return render_template('admin/blog_category_form.html', title='Edit Category' if category else 'New Category', form=form, category=category)

@admin_bp.route("/admin/blog-category/<int:category_id>/delete", methods=['POST'])
@login_required
@admin_required
def delete_blog_category(category_id):
    category = BlogCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_bp.admin_blog_categories'))
