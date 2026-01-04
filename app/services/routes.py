"""
Services Routes Module
Handles service listing, details, and data API:
- Service Browsing & Filtering
- Category-based Filtering
- Service Detail Pages
- JSON API for Client-side Filtering
"""

# =========================================
# THIRD-PARTY IMPORTS
# =========================================
from flask import render_template, request

# =========================================
# LOCAL APPLICATION IMPORTS
# =========================================
from app.extensions import db
from app.services import services
from app.models.service import Service
from app.models.service_category import ServiceCategory


# =========================================
# SERVICE LISTING ROUTES
# =========================================

@services.route("/services")
def services_list():
    """Display paginated list of services with category filtering"""
    page = request.args.get('page', 1, type=int)
    category_name = request.args.get('category', 'All')
    
    # Base query for active services
    services_query = Service.query.filter_by(is_active=True)
    
    # Filter by category if specified
    if category_name != 'All':
        services_query = services_query.join(Service.category).filter(ServiceCategory.name == category_name)
    
    services_query = services_query.order_by(Service.created_at.desc())
    services_paginated = services_query.paginate(page=page, per_page=6)
    
    # Get all active categories for the filters
    categories_obj = ServiceCategory.query.all()
    categories_list = [c.name for c in categories_obj]
    
    return render_template('services/services.html', 
                         title='Services', 
                         services=services_paginated, 
                         categories=categories_list, 
                         selected_category=category_name)


# =========================================
# SERVICE DATA API ROUTES
# =========================================

@services.route("/services-data")
def services_data():
    """API endpoint to return services data in JSON format for client-side filtering"""
    services_query = Service.query.filter_by(is_active=True).all()
    
    services_list = []
    for service in services_query:
        services_list.append({
            'id': service.id,
            'title': service.title,
            'description': service.description,
            'price': service.price,
            'image_url': service.image_url,
            'category': service.category.name if service.category else 'General',
            'category_id': service.category.id if service.category else None,
            'created_at': service.created_at.isoformat() if service.created_at else None
        })
    
    categories = ServiceCategory.query.all()
    categories_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
    
    return {
        'services': services_list,
        'categories': categories_list
    }


# =========================================
# SERVICE DETAIL ROUTES
# =========================================

@services.route("/services/service/<int:service_id>")
def service_detail(service_id):
    """Display individual service details"""
    service = Service.query.get_or_404(service_id)
    if not service.is_active:
        return render_template('errors/404.html'), 404
    return render_template('services/service_detail.html', title=service.title, service=service)