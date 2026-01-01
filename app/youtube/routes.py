from flask import render_template, request
from app.extensions import db
from app.youtube import youtube
from app.models.youtube_video import YouTubeVideo
from app.models.youtube_category import YouTubeCategory

@youtube.route("/videos")
def videos_list():
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category')
    
    query = YouTubeVideo.query.filter_by(is_active=True)
    
    if category_filter:
        query = query.filter_by(category=category_filter)
        
    videos_paginated = query.order_by(YouTubeVideo.created_at.desc()).paginate(page=page, per_page=9)
    
    # Fetch all categories from YouTubeCategory table
    categories = [cat.name for cat in YouTubeCategory.query.all()]
    
    # Fetch latest 3 videos for featured carousel
    featured_videos = YouTubeVideo.query.filter_by(is_active=True).order_by(YouTubeVideo.created_at.desc()).limit(3).all()
    
    return render_template('youtube/videos.html', 
                         title='YouTube Videos', 
                         videos=videos_paginated, 
                         categories=categories,
                         current_category=category_filter,
                         featured_videos=featured_videos)

@youtube.route("/video/<int:video_id>")
def video_detail(video_id):
    video = YouTubeVideo.query.get_or_404(video_id)
    if not video.is_active:
        return render_template('errors/404.html'), 404
    return render_template('youtube/video_detail.html', title=video.title, video=video)