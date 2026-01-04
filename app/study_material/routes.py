"""
Study Material Routes Module
Handles study material listing, details, and downloads:
- Material Browsing & Filtering
- Category-based Filtering
- Material Detail Pages
- Download Management
- External Document Links
"""

# =========================================
# STANDARD LIBRARY IMPORTS
# =========================================
import os

# =========================================
# THIRD-PARTY IMPORTS
# =========================================
from flask import render_template, request, send_file, redirect, url_for, flash
from flask_login import login_required, current_user

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.study_material import study_material
from app.models.study_material import StudyMaterial
from app.models.study_material_category import StudyMaterialCategory
from app.models.download import Download
from app.utils.constants import ITEM_TYPE_STUDY_MATERIAL


# =========================================
# MATERIAL LISTING ROUTES
# =========================================

@study_material.route("/study-materials")
def materials_list():
    """Display paginated list of study materials with category filtering"""
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category', None)
    
    query = StudyMaterial.query.filter_by(is_active=True)
        
    materials_paginated = query.order_by(StudyMaterial.created_at.desc()).paginate(page=page, per_page=100)
    
    # Get all unique categories for sidebar
    categories = [c.name for c in StudyMaterialCategory.query.order_by(StudyMaterialCategory.name).all()]
    
    return render_template('study_material/materials.html', 
                         title='Study Materials', 
                         materials=materials_paginated,
                         categories=categories,
                         current_category=category_filter)


# =========================================
# MATERIAL DETAIL ROUTES
# =========================================

@study_material.route("/study-material/<int:material_id>")
def material_detail(material_id):
    """Display individual study material details"""
    material = StudyMaterial.query.get_or_404(material_id)
    if not material.is_active:
        return render_template('errors/404.html'), 404
    return render_template('study_material/material_detail.html', title=material.title, material=material)


# =========================================
# MATERIAL DOWNLOAD ROUTES
# =========================================

@study_material.route("/study-material/download/<int:material_id>")
def download_material(material_id):
    """Handle study material downloads with tracking and payment verification"""
    material = StudyMaterial.query.get_or_404(material_id)
    
    if not material.is_active:
        flash('This study material is not available for download.', 'warning')
        return redirect(url_for('study_material.material_detail', material_id=material.id))
    
    # Check if material is free or if user has purchased it
    if material.material_type != 'free':
        flash('This is a paid study material. Purchase functionality coming soon!', 'info')
        return redirect(url_for('study_material.material_detail', material_id=material.id))
    
    # Check if external document URL is provided
    if material.doc_url:
        material.download_count += 1
        db.session.commit()
        return redirect(material.doc_url)
    
    # Check if file exists
    if not material.file_path or not os.path.exists(material.file_path):
        flash('Study material file not found.', 'danger')
        return redirect(url_for('study_material.material_detail', material_id=material.id))
    
    # Record download only if user is logged in
    if current_user.is_authenticated:
        download = Download(
            user_id=current_user.id,
            item_type=ITEM_TYPE_STUDY_MATERIAL,
            item_id=material.id,
            filename=os.path.basename(material.file_path)
        )
        db.session.add(download)
    
    # Increment download count
    material.download_count += 1
    db.session.commit()
    
    # Send file for download
    return send_file(material.file_path, as_attachment=True)