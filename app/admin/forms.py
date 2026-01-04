"""
Admin Forms Module
Contains all form classes for admin panel operations including:
- User Management Forms
- Content Management Forms (Services, Projects, Materials, Videos, Blogs)
- Category Management Forms
- Home & About Page Content Forms
- Skills & Team Management Forms
"""

# =========================================
# IMPORTS
# =========================================
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, FloatField, SelectField, 
    SubmitField, PasswordField
)
from wtforms.validators import (
    Optional, NumberRange, DataRequired, Length, 
    Email, EqualTo
)


# =========================================
# USER MANAGEMENT FORMS
# =========================================

class UserForm(FlaskForm):
    """Form for creating and managing user accounts"""
    username = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Assign Role', choices=[('admin', 'Admin'), ('user', 'User/Freelancer')], default='admin')
    submit = SubmitField('Create User')


# =========================================
# SERVICE MANAGEMENT FORMS
# =========================================

class ServiceCategoryForm(FlaskForm):
    """Form for creating and editing service categories"""
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Save Category')


class ServiceForm(FlaskForm):
    """Form for creating and editing services"""
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price (Optional)', validators=[Optional(), NumberRange(min=0)])
    image = FileField('Service Hero Image', validators=[
        Optional(), 
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    is_active = SelectField('Status', choices=[('True', 'Active'), ('False', 'Inactive')], default='True')
    submit = SubmitField('Save Service')


# =========================================
# PROJECT MANAGEMENT FORMS
# =========================================

class ProjectCategoryForm(FlaskForm):
    """Form for creating and editing project categories"""
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Save Category')


class ProjectForm(FlaskForm):
    """Form for creating and editing projects"""
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    image = FileField('Project Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')])
    project_type = SelectField('Type', choices=[('free', 'Free'), ('demo', 'Demo')], default='free')
    file = FileField('Project File (ZIP)', validators=[Optional(), FileAllowed(['zip'], 'ZIP files only!')])
    google_drive_link = StringField('Google Drive Link (Optional)', validators=[Optional(), Length(max=500)])
    github_link = StringField('GitHub Link (Optional)', validators=[Optional(), Length(max=500)])
    is_active = SelectField('Status', choices=[('True', 'Active'), ('False', 'Inactive')], default='True')
    submit = SubmitField('Save Project')


# =========================================
# STUDY MATERIAL MANAGEMENT FORMS
# =========================================

class StudyMaterialCategoryForm(FlaskForm):
    """Form for creating and editing study material categories"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Save Category')


class StudyMaterialForm(FlaskForm):
    """Form for creating and editing study materials"""
    title = StringField('Title')
    description = TextAreaField('Description')
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    file = FileField('Material File', validators=[Optional(), FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx'], 'Only PDF, DOC, DOCX, PPT, PPTX files allowed!')])
    doc_url = StringField('Document URL (Optional)', validators=[Optional(), Length(max=500)])
    thumbnail = FileField('Thumbnail Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')])
    material_type = SelectField('Type', choices=[('free', 'Free'), ('paid', 'Paid')], default='free')
    is_active = SelectField('Status', choices=[('True', 'Active'), ('False', 'Inactive')], default='True')
    submit = SubmitField('Save')
    
    def validate(self, extra_validators=None):
        """Custom validation: either file or doc_url must be provided"""
        # First run default validation
        if not super().validate(extra_validators):
            return False
        
        # Custom validation
        if not self.file.data and not self.doc_url.data:
            self.file.errors.append('Either upload a file or provide a document URL.')
            self.doc_url.errors.append('Either upload a file or provide a document URL.')
            return False
        
        return True


# =========================================
# YOUTUBE VIDEO MANAGEMENT FORMS
# =========================================

class YouTubeCategoryForm(FlaskForm):
    """Form for creating and editing YouTube video categories"""
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Save Category')


class YouTubeVideoForm(FlaskForm):
    """Form for creating and editing YouTube videos"""
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    video_url = StringField('YouTube URL', validators=[DataRequired()])
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    is_active = SelectField('Status', choices=[('True', 'Active'), ('False', 'Inactive')], default='True')
    submit = SubmitField('Save')


# =========================================
# BLOG MANAGEMENT FORMS
# =========================================

class BlogCategoryForm(FlaskForm):
    """Form for creating and editing blog categories"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Save Category')


class BlogPostForm(FlaskForm):
    """Form for creating and editing blog posts"""
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[], validators=[DataRequired()])
    read_time = StringField('Read Time (e.g. 5 min read)', validators=[Optional()])
    thumbnail = FileField('Thumbnail Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')])
    is_active = SelectField('Status', choices=[('True', 'Active'), ('False', 'Inactive')], default='True')
    submit = SubmitField('Save Post')


# =========================================
# INQUIRY MANAGEMENT FORMS
# =========================================

class InquiryForm(FlaskForm):
    """Form for managing inquiry status"""
    status = SelectField('Status', 
                        choices=[('new', 'New'), ('contacted', 'Contacted'), ('closed', 'Closed')], 
                        default='new')
    submit = SubmitField('Update')


# =========================================
# HOME PAGE CONTENT FORMS
# =========================================

class HomeContentForm(FlaskForm):
    """Form for editing home page content"""
    # Hero Section
    hero_title_line1 = StringField('Hero Title Line 1', validators=[DataRequired(), Length(max=100)])
    hero_title_line2 = StringField('Hero Title Line 2', validators=[DataRequired(), Length(max=100)])
    hero_subtitle = TextAreaField('Hero Subtitle', validators=[DataRequired()])
    
    # Profile Section
    profile_image = FileField('Profile Image', validators=[
        Optional(), 
        FileAllowed(['jpg', 'png', 'jpeg', 'webp'], 'Images only!')
    ])
    
    # Stats
    stat_projects = StringField('Projects Count', validators=[DataRequired(), Length(max=20)])
    stat_materials = StringField('Materials Count', validators=[DataRequired(), Length(max=20)])
    stat_team = StringField('Team Count', validators=[DataRequired(), Length(max=20)])
    stat_downloads = StringField('Downloads Count', validators=[DataRequired(), Length(max=20)])
    
    # Knowledge Hub
    knowledge_hub_title = StringField('Knowledge Hub Title', validators=[DataRequired(), Length(max=100)])
    knowledge_hub_subtitle = TextAreaField('Knowledge Hub Subtitle', validators=[DataRequired()])
    
    # Workflow Section
    workflow_title = StringField('Workflow Title', validators=[DataRequired(), Length(max=100)])
    workflow_subtitle = TextAreaField('Workflow Subtitle', validators=[DataRequired()])
    
    # CTA Buttons
    cv_button_text = StringField('CV Button Text', validators=[DataRequired(), Length(max=50)])
    cv_button_link = StringField('CV File URL/Link', validators=[Optional(), Length(max=300)])
    hire_button_text = StringField('Hire Button Text', validators=[DataRequired(), Length(max=50)])
    
    submit = SubmitField('Update Home Page')


# =========================================
# ABOUT PAGE CONTENT FORMS
# =========================================

class AboutContentForm(FlaskForm):
    """Form for editing about page content"""
    # Hero Section
    hero_title = StringField('Hero Title', validators=[DataRequired(), Length(max=200)])
    hero_subtitle = TextAreaField('Hero Subtitle', validators=[DataRequired()])
    hero_image = FileField('Hero Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    hero_stat_1_count = StringField('Stat 1 Count', validators=[DataRequired(), Length(max=50)])
    hero_stat_1_label = StringField('Stat 1 Label', validators=[DataRequired(), Length(max=100)])
    hero_stat_2_count = StringField('Stat 2 Count', validators=[DataRequired(), Length(max=50)])
    hero_stat_2_label = StringField('Stat 2 Label', validators=[DataRequired(), Length(max=100)])
    hero_stat_3_count = StringField('Stat 3 Count', validators=[DataRequired(), Length(max=50)])
    hero_stat_3_label = StringField('Stat 3 Label', validators=[DataRequired(), Length(max=100)])
    
    # Mission Section
    mission_title = StringField('Mission Title', validators=[DataRequired(), Length(max=100)])
    mission_content = TextAreaField('Mission Content', validators=[DataRequired()])
    
    # Vision Section
    vision_title = StringField('Vision Title', validators=[DataRequired(), Length(max=100)])
    vision_content = TextAreaField('Vision Content', validators=[DataRequired()])
    
    # Values Section
    values_title = StringField('Values Section Title', validators=[DataRequired(), Length(max=100)])
    value1_title = StringField('Value 1 Title', validators=[DataRequired(), Length(max=100)])
    value1_description = TextAreaField('Value 1 Description', validators=[DataRequired()])
    value2_title = StringField('Value 2 Title', validators=[DataRequired(), Length(max=100)])
    value2_description = TextAreaField('Value 2 Description', validators=[DataRequired()])
    value3_title = StringField('Value 3 Title', validators=[DataRequired(), Length(max=100)])
    value3_description = TextAreaField('Value 3 Description', validators=[DataRequired()])
    value4_title = StringField('Value 4 Title', validators=[DataRequired(), Length(max=100)])
    value4_description = TextAreaField('Value 4 Description', validators=[DataRequired()])
    value5_title = StringField('Value 5 Title', validators=[DataRequired(), Length(max=100)])
    value5_description = TextAreaField('Value 5 Description', validators=[DataRequired()])
    value6_title = StringField('Value 6 Title', validators=[DataRequired(), Length(max=100)])
    value6_description = TextAreaField('Value 6 Description', validators=[DataRequired()])
    
    # Story Section
    story_title = StringField('Story Title', validators=[DataRequired(), Length(max=100)])
    story_content = TextAreaField('Story Content', validators=[DataRequired()])
    
    # Timeline Section
    timeline_year_1 = StringField('Timeline 1 Year', validators=[DataRequired(), Length(max=20)])
    timeline_title_1 = StringField('Timeline 1 Title', validators=[DataRequired(), Length(max=100)])
    timeline_content_1 = TextAreaField('Timeline 1 Content', validators=[DataRequired()])
    
    timeline_year_2 = StringField('Timeline 2 Year', validators=[DataRequired(), Length(max=20)])
    timeline_title_2 = StringField('Timeline 2 Title', validators=[DataRequired(), Length(max=100)])
    timeline_content_2 = TextAreaField('Timeline 2 Content', validators=[DataRequired()])
    
    timeline_year_3 = StringField('Timeline 3 Year', validators=[DataRequired(), Length(max=20)])
    timeline_title_3 = StringField('Timeline 3 Title', validators=[DataRequired(), Length(max=100)])
    timeline_content_3 = TextAreaField('Timeline 3 Content', validators=[DataRequired()])
    
    timeline_year_4 = StringField('Timeline 4 Year', validators=[DataRequired(), Length(max=20)])
    timeline_title_4 = StringField('Timeline 4 Title', validators=[DataRequired(), Length(max=100)])
    timeline_content_4 = TextAreaField('Timeline 4 Content', validators=[DataRequired()])
    
    # Team Section
    team_title = StringField('Team Section Title', validators=[DataRequired(), Length(max=100)])
    team_subtitle = TextAreaField('Team Subtitle', validators=[DataRequired()])
    
    # CTA Section
    cta_title = StringField('CTA Title', validators=[DataRequired(), Length(max=100)])
    cta_subtitle = TextAreaField('CTA Subtitle', validators=[DataRequired()])
    cta_button_text = StringField('CTA Button 1 Text', validators=[DataRequired(), Length(max=50)])
    cta_button_link = StringField('CTA Button 1 Link Route', validators=[DataRequired(), Length(max=100)])
    cta_button_2_text = StringField('CTA Button 2 Text', validators=[DataRequired(), Length(max=50)])
    cta_button_2_link = StringField('CTA Button 2 Link Route', validators=[DataRequired(), Length(max=100)])
    
    submit = SubmitField('Update About Page')


# =========================================
# SKILLS MANAGEMENT FORMS
# =========================================

class SkillCategoryForm(FlaskForm):
    """Form for creating and editing skill categories"""
    name = StringField('Category Name', validators=[DataRequired(), Length(max=50)])
    description = StringField('Description', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Save Category')


class SkillForm(FlaskForm):
    """Form for creating and editing skills"""
    name = StringField('Skill Name', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', 
                          choices=[('Frontend', 'Frontend Development'), 
                                   ('Backend', 'Backend Development'), 
                                   ('Tools', 'Tools & DevOps'), 
                                   ('Design', 'Design & Others')],
                          validators=[DataRequired()])
    percentage = StringField('Proficiency Level (%)', validators=[DataRequired(), Length(max=3)])
    icon_text = StringField('Icon Text (2-3 chars)', validators=[DataRequired(), Length(max=10)])
    color = SelectField('Color Theme', 
                       choices=[('blue', 'Blue'), ('green', 'Green'), ('purple', 'Purple'), 
                               ('pink', 'Pink'), ('orange', 'Orange'), ('red', 'Red'), 
                               ('yellow', 'Yellow'), ('cyan', 'Cyan'), ('indigo', 'Indigo')],
                       default='blue')
    order = StringField('Display Order', validators=[Optional()])
    is_active = SelectField('Status', choices=[('True', 'Active'), ('False', 'Inactive')], default='True')
    submit = SubmitField('Save Skill')


# =========================================
# TEAM MEMBERS MANAGEMENT FORMS
# =========================================

class TeamMemberForm(FlaskForm):
    """Form for creating and editing team members"""
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    position = StringField('Position/Role', validators=[DataRequired(), Length(max=100)])
    bio = TextAreaField('Short Bio', validators=[Optional()])
    image_upload = FileField('Upload Profile Image', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')
    ])
    image_url = StringField('Or Image URL', validators=[Optional(), Length(max=500)])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), Length(max=500)])
    twitter_url = StringField('Twitter URL', validators=[Optional(), Length(max=500)])
    github_url = StringField('GitHub URL', validators=[Optional(), Length(max=500)])
    dribbble_url = StringField('Dribbble URL', validators=[Optional(), Length(max=500)])
    behance_url = StringField('Behance URL', validators=[Optional(), Length(max=500)])
    order = StringField('Display Order', validators=[Optional()])
    is_active = SelectField('Status', choices=[('True', 'Active'), ('False', 'Inactive')], default='True')
    submit = SubmitField('Save Team Member')
