# 🚀 Premium Freelancing & Service Showcase Platform

A modern, fully dynamic, and feature-rich web platform designed for freelancers, agencies, and service providers. This project features a stunning, premium UI/UX built with **Flask** and **Tailwind CSS**, allowing for complete content management through a secure admin dashboard.

---

## ✨ Key Features

### 🌐 Public Showcase
- **Dynamic Home Page**: High-impact hero section, real-time statistics, beautifully presented skills, and interactive workflow sections.
- **Professional About Page**: Detailed sections for Mission, Vision, Values, and an interactive Company Story/Timeline.
- **Service Catalog**: Categorized service listings with detailed descriptions and pricing, featuring instant client-side filtering.
- **Project Portfolio**: A premium showcase for projects with filtering by category, image galleries, and secure download links.
- **Knowledge Hub & Study Materials**: A dedicated area for sharing PDFs, documents, and resources with built-in search functionality.
- **YouTube Video Hub**: Seamlessly integrated YouTube videos categorized for easy navigation.
- **Blog System**: Comprehensive blog functionality with categories and detailed posts.
- **Responsive Design**: Fully optimized for mobile, tablet, and desktop views with a modern, clean aesthetic.

### 🔐 Secure Admin Dashboard
- **Content Management System (CMS)**: Edit every piece of text and image on the Home and About pages directly from the browser.
- **Full CRUD Operations**: Create, read, update, and delete Services, Projects, Skills, Team Members, Study Materials, YouTube Videos, and Blog Posts.
- **Category Management**: Organize content with dedicated category management for services, projects, study materials, YouTube videos, and blog posts.
- **Skill & Team Management**: Manage professional skills with visual progress bars and team member profiles with social links.
- **Inquiry Management**: View and track client inquiries submitted via the platform's contact forms.
- **Email Notifications**: Instant email alerts for new inquiries using SMTP.
- **User Management**: Secure admin login and the ability to manage other administrative accounts.
- **Security & Performance**: Built-in CSRF protection, rate limiting (Flask-Limiter), and secure password hashing (Bcrypt).

---

## 🛠️ Technology Stack

- **Backend**: Python / Flask
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: Tailwind CSS (PostCSS) / JavaScript / Jinja2 Templates
- **Auth**: Flask-Login / Flask-Bcrypt
- **Migrations**: Flask-Migrate
- **Forms**: Flask-WTF
- **Admin**: Flask-Admin

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13.9
- Virtual Environment (Recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "Freelancing Platform"
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory (refer to the `.env.example` if available) and add your configuration:
   ```env
   SECRET_KEY=your_secret_key_here
   DATABASE_URL=sqlite:///instance/app.db
   BRAND_NAME=YourBrand
   # ... add other contact details
   ```

5. **Initialize Database**:
   ```bash
   # Initialize migrations (creates migrations directory and files)
   flask db init
   # Create database tables from models
   flask db upgrade
   ```

6. **Create an Admin User**:
   ```bash
   python create_admin.py
   ```

7. **Run the application**:
   ```bash
   python run.py
   ```
   The application will be available at `http://localhost:5000`.

---

## 📧 Email Configuration Setup

To enable email notifications for contact form inquiries, follow these steps:

1. **Get an App Password**: If using Gmail, go to your Google Account settings, enable 2-Factor Authentication, and create an "App Password".
2. **Update `.env`**: Add the following details:
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   SUPPORT_EMAIL=your-receiving-email@gmail.com
   ```
3. **Restart the App**: Changes to `.env` require an app restart to take effect.

Note: For production, ensure `MAIL_USE_TLS` is set according to your provider's requirements.

---

## 📂 Project Structure

```
├── app/                          # Main application package
│   ├── __init__.py              # Application factory and initialization
│   ├── config.py                # Configuration settings and environment variables
│   ├── extensions.py            # Flask extensions initialization
│   ├── admin/                   # Admin dashboard module
│   │   ├── __init__.py          # Admin blueprint initialization
│   │   ├── forms.py             # Admin forms (services, projects, users)
│   │   └── routes.py            # Admin dashboard routes with CRUD operations
│   ├── auth/                    # Authentication module
│   │   ├── __init__.py          # Auth blueprint initialization
│   │   ├── forms.py             # Login forms
│   │   └── routes.py            # Authentication routes (login/logout)
│   ├── contact/                 # Contact form module
│   │   ├── __init__.py          # Contact blueprint initialization
│   │   ├── forms.py             # Contact form definition
│   │   └── routes.py            # Contact form processing with rate limiting
│   ├── models/                  # Database models
│   │   ├── __init__.py          # Model imports
│   │   ├── about_content.py     # About page content model
│   │   ├── base.py              # Base model with common fields and methods
│   │   ├── blog_category.py     # Blog category model
│   │   ├── blog_post.py         # Blog post model
│   │   ├── download.py          # Download tracking model for study materials
│   │   ├── home_content.py      # Home page content model
│   │   ├── home_page.py         # Home page models (skills, team members)
│   │   ├── inquiry.py           # Contact inquiry model
│   │   ├── project.py           # Project model with file uploads and links
│   │   ├── project_category.py  # Project category model
│   │   ├── service.py           # Service model
│   │   ├── service_category.py  # Service category model
│   │   ├── skill_category.py    # Skill category model
│   │   ├── study_material.py    # Study material model with PDF uploads
│   │   ├── study_material_category.py # Study material category model
│   │   ├── user.py              # User model with authentication
│   │   ├── youtube_category.py  # YouTube category model
│   │   └── youtube_video.py     # YouTube video model
│   ├── pages/                   # Public pages module
│   │   ├── __init__.py          # Pages blueprint initialization
│   │   └── routes.py            # Home, about, blog, and static page routes
│   ├── projects/                # Projects module
│   │   ├── __init__.py          # Projects blueprint initialization
│   │   └── routes.py            # Project listing and detail routes
│   ├── services/                # Services module
│   │   ├── __init__.py          # Services blueprint initialization
│   │   └── routes.py            # Service listing, detail and API routes
│   ├── static/                  # Static assets
│   │   ├── css/                 # Stylesheet files
│   │   │   ├── about.css        # About page specific styles
│   │   │   ├── contact.css      # Contact page specific styles
│   │   │   ├── custom.css       # Custom global styles
│   │   │   ├── home.css         # Home page specific styles
│   │   │   ├── main.css         # Main styles
│   │   │   ├── materials.css    # Study materials specific styles
│   │   │   ├── projects.css     # Projects specific styles
│   │   │   ├── services.css     # Services specific styles
│   │   │   ├── video_detail.css # Video detail specific styles
│   │   │   └── videos.css       # Videos specific styles
│   │   ├── js/                  # JavaScript files
│   │   │   ├── about.js         # About page specific JavaScript
│   │   │   ├── contact.js       # Contact page specific JavaScript
│   │   │   ├── custom.js        # General JavaScript functionality
│   │   │   ├── home.js          # Home page specific JavaScript
│   │   │   ├── materials.js     # Study materials specific JavaScript
│   │   │   ├── projects.js      # Projects specific JavaScript
│   │   │   ├── services.js      # Services specific JavaScript
│   │   │   └── videos.js        # Videos specific JavaScript
│   │   └── uploads/             # Uploaded files (images, documents) - created at runtime
│   ├── study_material/          # Study materials module
│   │   ├── __init__.py          # Study material blueprint initialization
│   │   └── routes.py            # Study material listing and detail routes
│   ├── templates/               # HTML templates organized by module
│   │   ├── admin/               # Admin dashboard templates
│   │   │   ├── about_page_content.html        # About page content editor
│   │   │   ├── about_page_content_view.html   # About page preview
│   │   │   ├── blog_categories.html           # Blog category management
│   │   │   ├── blog_category_form.html        # Blog category form
│   │   │   ├── blog_form.html                 # Blog post form
│   │   │   ├── blogs.html                     # Blog listing
│   │   │   ├── categories.html                # General category management
│   │   │   ├── category_form.html             # Category form
│   │   │   ├── dashboard.html                 # Admin dashboard
│   │   │   ├── home_about_content.html        # Home/about content editor
│   │   │   ├── home_page_content.html         # Home page content editor
│   │   │   ├── home_page_content_view.html    # Home page preview
│   │   │   ├── inquiries.html                 # Inquiry management
│   │   │   ├── inquiry_form.html              # Inquiry form
│   │   │   ├── material_categories.html       # Material category management
│   │   │   ├── material_category_form.html    # Material category form
│   │   │   ├── material_form.html             # Material form
│   │   │   ├── project_category_form.html     # Project category form
│   │   │   ├── project_form.html              # Project form
│   │   │   ├── projects.html                  # Project management
│   │   │   ├── service_form.html              # Service form
│   │   │   ├── services.html                  # Service management
│   │   │   ├── skill_category_form.html       # Skill category form
│   │   │   ├── skill_form.html                # Skill form
│   │   │   ├── skills_list.html               # Skills listing
│   │   │   ├── study_material.html            # Study material management
│   │   │   ├── team_member_form.html          # Team member form
│   │   │   ├── team_members_list.html         # Team members listing
│   │   │   ├── user_form.html                 # User form
│   │   │   ├── users.html                     # User management
│   │   │   ├── video_form.html                # Video form
│   │   │   ├── youtube_categories.html        # YouTube category management
│   │   │   ├── youtube_category_form.html     # YouTube category form
│   │   │   └── youtube_videos.html            # YouTube video management
│   │   ├── auth/                # Authentication templates
│   │   │   └── admin_login.html   # Admin login page
│   │   ├── base/                # Base templates
│   │   │   ├── admin_base.html    # Admin base template
│   │   │   ├── base.html          # Main base template
│   │   │   ├── footer.html        # Footer component
│   │   │   └── header.html        # Header component
│   │   ├── contact/               # Contact page templates
│   │   │   └── contact.html       # Contact form page
│   │   ├── errors/                # Error page templates
│   │   │   ├── 404.html           # Page not found
│   │   │   └── 500.html           # Server error
│   │   ├── materials/             # Material templates
│   │   │   ├── material_detail.html # Material detail page
│   │   │   └── materials.html     # Material listing
│   │   ├── pages/                 # Static page templates
│   │   │   ├── about.html         # About page
│   │   │   ├── blog.html          # Blog listing page
│   │   │   ├── blog_detail.html   # Blog post detail
│   │   │   ├── contact.html       # Contact page
│   │   │   ├── cookies.html       # Cookies policy
│   │   │   ├── home.html          # Home page
│   │   │   ├── privacy.html       # Privacy policy
│   │   │   └── terms.html         # Terms of service
│   │   ├── projects/              # Project templates
│   │   │   ├── project_detail.html # Project detail page
│   │   │   └── projects.html      # Project listing page
│   │   ├── services/              # Service templates
│   │   │   ├── service_detail.html # Service detail page
│   │   │   └── services.html      # Service listing with client-side filtering
│   │   ├── study_material/        # Study material templates
│   │   │   ├── material_detail.html # Study material detail
│   │   │   └── materials.html     # Study material listing
│   │   └── youtube/               # YouTube templates
│   │       ├── video_detail.html  # YouTube video detail
│   │       └── videos.html        # YouTube video listing
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py          # Utility imports
│   │   ├── constants.py         # Application constants and enums
│   │   ├── decorators.py        # Custom decorators (admin_required, etc.)
│   │   └── helpers.py           # Helper functions (image upload, etc.)
│   └── youtube/                 # YouTube module
│       ├── __init__.py          # YouTube blueprint initialization
│       └── routes.py            # YouTube video routes
│   └── dashboard/               # Dashboard module (currently empty)
│       ├── __init__.py          # Dashboard blueprint initialization (empty)
│       └── routes.py            # Dashboard routes (empty)
├── create_admin.py              # Script to create admin user
├── instance/                    # Instance folder (contains database files)
│   ├── database.db              # Database file (if using default config)
│   └── site.db                  # Main application database
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
├── .env.example                 # Environment variables example
├── .gitignore                   # Files to ignore in Git
└── README.md                    # Project documentation
```

---

## 📚 Project Overview

### Core Architecture
The application follows the Flask application factory pattern with blueprints for modular organization. It uses SQLAlchemy ORM for database operations and implements a secure authentication system with role-based access control.

### Database Models
The application includes 19 different models that support:
- **Content Management**: Home page, about page, blog posts
- **Service Management**: Services and service categories
- **Project Management**: Projects and project categories
- **User Management**: Admin users and authentication
- **Media Management**: Study materials and YouTube videos
- **Contact Management**: Inquiries and contact forms with rate limiting and automated email notifications
- **Additional Features**: Skills, team members, and download tracking

### Frontend Features
- **Modern UI/UX**: Premium design with glass morphism, gradients, and smooth animations
- **Client-Side Filtering**: Instant filtering of services without page refreshes
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Interactive Elements**: Hover effects, animations, and smooth transitions

### Contact & Communication Features
- **Contact Form**: User-friendly contact form with validation and rate limiting
- **Email Notifications**: Automated email alerts for new inquiries via SMTP
- **Inquiry Management**: Admin dashboard for tracking and managing client inquiries
- **Rate Limiting**: Protection against spam (2 requests per minute)

### Content Management Features
- **Dynamic Content**: Editable content sections on home and about pages
- **File Uploads**: Image and document upload capabilities for services, projects, and materials
- **Category Management**: Organize content with dedicated category systems
- **User Management**: Admin user creation and role management

### Security Features
- **CSRF Protection**: Cross-site request forgery protection
- **Rate Limiting**: Protection against brute-force attacks (e.g., 2 requests per minute for contact form)
- **Secure Headers**: XSS protection, clickjacking prevention, HSTS, and other security headers
- **Password Hashing**: Bcrypt for secure password storage
- **Input Validation**: Server-side validation for all forms
- **Role-Based Access Control**: Admin-specific routes and functionality
- **User Authentication**: Secure login/logout with session management

### Admin Dashboard
The admin dashboard provides comprehensive content management capabilities:
- **Real-time Editing**: Edit content without code changes
- **CRUD Operations**: Full create, read, update, delete functionality
- **File Uploads**: Image and document upload capabilities
- **User Management**: Secure admin user management
- **Inquiry Tracking**: Monitor client inquiries and messages

---

## 🛡️ Security Features

- **RBAC**: Role-Based Access Control for admin routes.
- **Rate Limiting**: Protection against brute-force attacks on sensitive endpoints.
- **Secure Headers**: Implemented security headers (X-Frame-Options, HSTS, etc.).
- **Data Validation**: Strict server-side validation for all forms.
- **CSRF Protection**: Cross-site request forgery protection for all forms.
- **Password Security**: Bcrypt for secure password hashing.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Developed with ❤️ by the Freelancing Platform Team.
