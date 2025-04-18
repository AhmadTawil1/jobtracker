# JobTracker - Your Job Search Companion

![JobTracker Logo](https://via.placeholder.com/150x50?text=JobTracker)

A modern, user-friendly web application to help job seekers track and manage their job applications throughout their career journey.

## 🚀 Features

### Core Functionality
- **Job Application Tracking**: Record and monitor all your job applications in one place
- **Resume Management**: Upload and attach resumes to specific job applications
- **Status Monitoring**: Track application status (Applied, Interview, Offer, Rejected, Accepted)
- **Dashboard Analytics**: Visualize your job search progress with statistics
- **Multi-user Support**: Secure, isolated data for each user

### User Experience
- **Modern UI**: Clean, responsive design built with Tailwind CSS
- **Intuitive Navigation**: Easy-to-use interface for all skill levels
- **Mobile Responsive**: Works seamlessly on all devices
- **Visual Feedback**: Status indicators and progress tracking

### Security & Privacy
- **User Authentication**: Secure login and registration
- **Data Isolation**: Each user can only access their own data
- **Protected Routes**: Authentication required for all job-related actions

## 🛠️ Technology Stack

- **Backend**: Django
- **Frontend**: HTML, Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Authentication**: Django's built-in authentication system
- **File Storage**: Django's FileField for resume storage

## 📋 Project Structure

```
applications/
├── templates/
│   ├── base.html
│   └── applications/
│       ├── list.html
│       ├── form.html
│       ├── login.html
│       ├── register.html
│       └── confirm_delete.html
├── templatetags/
│   └── job_filters.py
├── models.py
├── views.py
├── forms.py
├── admin.py
└── urls.py
```

## 🎯 Target Users

- University students or recent graduates seeking internships or jobs
- Young professionals managing multiple applications
- Anyone wanting to stay organized during their job search

## 💡 Problem Solved

Job seekers often struggle with:
- Losing track of applications
- Forgetting deadlines or follow-ups
- Relying on spreadsheets or scattered notes
- Feeling overwhelmed from lack of visibility or control

JobTracker provides a centralized, user-friendly platform to address these challenges.

## 🔒 Security Features

- User authentication required for all job-related actions
- Data isolation between users
- CSRF protection
- Secure file upload handling

## 🧩 Future Enhancements

- AI resume feedback
- Email reminders for deadlines
- Export options (CSV/PDF)
- Tags and priority labels
- Chrome extension for quick adds

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 4.0+

### Installation

1. Clone the repository
```bash
git clone https://github.com/AhmadTawil1/jobtracker.git
cd jobtracker
```

2. Create and activate a virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

6. Run the development server
```bash
python manage.py runserver
```

7. Visit `http://127.0.0.1:8000` in your browser

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Ahmad Tawil**
- GitHub: [@AhmadTawil1](https://github.com/AhmadTawil1)

## 🙏 Acknowledgments

- Design inspiration from modern job application platforms
- Tailwind CSS for the beautiful UI components
- Font Awesome for the icons 