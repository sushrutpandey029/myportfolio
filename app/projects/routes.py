from flask import render_template, request, send_file, redirect, url_for, flash
from flask_login import current_user
from app.extensions import db
from app.projects import projects
from app.models.project import Project
from app.models.project_category import ProjectCategory
from app.models.download import Download
from app.utils.constants import ITEM_TYPE_PROJECT
import os

@projects.route("/projects")
def projects_list():
    page = request.args.get('page', 1, type=int)
    category_name = request.args.get('category', 'All')
    
    # Base query for active projects
    projects_query = Project.query.filter_by(is_active=True)
    
    # Filter by category if specified
    if category_name != 'All':
        projects_query = projects_query.join(Project.project_category).filter(ProjectCategory.name == category_name)
    
    projects_query = projects_query.order_by(Project.created_at.desc())
    projects_paginated = projects_query.paginate(page=page, per_page=6)
    
    # Get all active categories for the filters
    categories_obj = ProjectCategory.query.all()
    categories_list = [c.name for c in categories_obj]
    
    return render_template('projects/projects.html', 
                         title='Projects', 
                         projects=projects_paginated,
                         categories=categories_list,
                         selected_category=category_name)

@projects.route("/project/<int:project_id>")
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    if not project.is_active:
        return render_template('errors/404.html'), 404
    return render_template('projects/project_detail.html', title=project.title, project=project)

@projects.route("/project/download/<int:project_id>")
def download_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if not project.is_active:
        flash('This project is not available for download.', 'warning')
        return redirect(url_for('projects.projects_list'))
    
    # Record download only if user is logged in
    if current_user.is_authenticated:
        download = Download(
            user_id=current_user.id,
            item_type=ITEM_TYPE_PROJECT,
            item_id=project.id,
            filename=project.title
        )
        db.session.add(download)
    
    # Increment download count
    project.download_count += 1
    db.session.commit()
    
    # Priority: GitHub > Google Drive > Uploaded File
    # If GitHub link is provided, redirect to it (highest priority)
    if project.github_link:
        return redirect(project.github_link)
    
    # If Google Drive link is provided, redirect to it
    if project.google_drive_link:
        return redirect(project.google_drive_link)
    
    # Otherwise, check if file exists and send it
    if not project.file_path:
        flash('No download link or file available for this project.', 'danger')
        return redirect(url_for('projects.projects_list'))
    
    file_path = os.path.join('app', 'static', project.file_path)
    if not os.path.exists(file_path):
        flash('Project file not found.', 'danger')
        return redirect(url_for('projects.projects_list'))
    
    # Send file for download
    return send_file(file_path, as_attachment=True)