# student-progress-tracker
A Python-based student progress tracker with a login system and personalized feedback for every student.
#  Student Progress Tracker

A comprehensive Python application for tracking student academic progress with personalized feedback and an admin dashboard.

##  Features

- ** Secure Login System** - Password hashing with SHA256
- ** Multi-user Support** - Students and admin roles
- ** Progress Tracking** - Track scores across multiple subjects
- ** Personalized Messages** - AI-like feedback based on performance
- ** Performance Analytics** - Trends, statistics, and insights
- ** Data Persistence** - JSON file storage
- ** Admin Dashboard** - View all students' progress

##  Getting Started

### Prerequisites
- Python 3.8 or higher
- No external libraries required (uses built-in modules)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/UmmeyHabiba123/student-progress-tracker.git
cd student-progress-tracker
```

2. Run the application:
```bash
python student_tracker.py
```

##  Test Accounts

### Students
- **Username:** `faiza` | **Password:** `faiza123`
- **Username:** `ratul` | **Password:** `ratul123`

### Admin
- **Username:** `admin` | **Password:** `admin123`

## 📖 How to Use

1. **Login** with existing credentials or **register** a new student
2. **Add Progress Entries** for different subjects
3. **View Statistics** and personalized feedback
4. **Admin users** can view all students' progress

##  Sample Personalized Messages

-  "Excellent work, Faiza! You're performing outstandingly!"
-  "Ratul, you need to put in more effort. You can do better!"
-  "You're improving! Keep up the momentum!"

##  File Structure

```
student-progress-tracker/
├── student_tracker.py      # Main application file
├── students.json          # Student credentials (auto-generated)
├── progress.json          # Progress data (auto-generated)
└── README.md             # This file
```

## 🛠 Technical Details

- **Language:** Python 3.8+
- **Data Storage:** JSON files
- **Security:** SHA256 password hashing
- **Architecture:** Object-oriented design
- **UI:** Command-line interface

##  Contributing

Feel free to fork this project and submit pull requests for improvements!

##  License

This project is open source and available under the MIT License.

##  Author

Created as a medium-level Python learning project.
