import json
import os
from datetime import datetime
import hashlib

class StudentProgressTracker:
    def __init__(self):
        self.students_file = "students.json"
        self.progress_file = "progress.json"
        self.current_user = None
        self.load_data()
    
    def load_data(self):
        """Load student and progress data from files"""
        # Load students data
        if os.path.exists(self.students_file):
            try:
                with open(self.students_file, 'r') as f:
                    self.students = json.load(f)
            except:
                self.students = {}
        else:
            # Initialize with sample students
            self.students = {
                "faiza": {
                    "password": self.hash_password("faiza123"),
                    "full_name": "Faiza Rahman",
                    "email": "faiza@email.com"
                },
                "ratul": {
                    "password": self.hash_password("ratul123"),
                    "full_name": "Ratul Ahmed",
                    "email": "ratul@email.com"
                },
                "admin": {
                    "password": self.hash_password("admin123"),
                    "full_name": "Administrator",
                    "email": "admin@school.com",
                    "role": "admin"
                }
            }
            self.save_students()
        
        # Load progress data
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    self.progress = json.load(f)
            except:
                self.progress = {}
        else:
            # Initialize with sample progress data
            self.progress = {
                "faiza": [
                    {"subject": "Math", "score": 85, "max_score": 100, "date": "2024-01-15"},
                    {"subject": "English", "score": 78, "max_score": 100, "date": "2024-01-16"},
                    {"subject": "Science", "score": 92, "max_score": 100, "date": "2024-01-17"}
                ],
                "ratul": [
                    {"subject": "Math", "score": 72, "max_score": 100, "date": "2024-01-15"},
                    {"subject": "English", "score": 88, "max_score": 100, "date": "2024-01-16"},
                    {"subject": "Science", "score": 65, "max_score": 100, "date": "2024-01-17"}
                ]
            }
            self.save_progress()
    
    def hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def save_students(self):
        """Save students data to file"""
        with open(self.students_file, 'w') as f:
            json.dump(self.students, f, indent=4)
    
    def save_progress(self):
        """Save progress data to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=4)
    
    def login(self, username, password):
        """Handle user login"""
        if username in self.students:
            if self.students[username]["password"] == self.hash_password(password):
                self.current_user = username
                return True
        return False
    
    def register_student(self, username, password, full_name, email):
        """Register a new student"""
        if username in self.students:
            return False, "Username already exists"
        
        self.students[username] = {
            "password": self.hash_password(password),
            "full_name": full_name,
            "email": email
        }
        self.progress[username] = []
        self.save_students()
        self.save_progress()
        return True, "Student registered successfully"
    
    def add_progress(self, subject, score, max_score=100):
        """Add progress entry for current user"""
        if not self.current_user:
            return False, "Please login first"
        
        if self.current_user not in self.progress:
            self.progress[self.current_user] = []
        
        entry = {
            "subject": subject,
            "score": score,
            "max_score": max_score,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.progress[self.current_user].append(entry)
        self.save_progress()
        return True, "Progress added successfully"
    
    def get_personalized_message(self, username=None):
        """Generate personalized message based on student's performance"""
        if username is None:
            username = self.current_user
        
        if username not in self.progress or not self.progress[username]:
            return "Welcome! Start adding your progress to see personalized feedback."
        
        recent_scores = []
        total_scores = []
        
        for entry in self.progress[username]:
            percentage = (entry["score"] / entry["max_score"]) * 100
            recent_scores.append(percentage)
            total_scores.append(percentage)
        
        # Get recent performance (last 3 entries)
        recent_avg = sum(recent_scores[-3:]) / len(recent_scores[-3:]) if recent_scores else 0
        overall_avg = sum(total_scores) / len(total_scores) if total_scores else 0
        
        name = self.students[username]["full_name"].split()[0]
        
        # Determine trend
        if len(recent_scores) >= 2:
            recent_trend = recent_scores[-1] - recent_scores[-2]
        else:
            recent_trend = 0
        
        # Generate personalized message
        messages = []
        
        if recent_avg >= 90:
            messages.append(f"🌟 Excellent work, {name}! You're performing outstandingly!")
        elif recent_avg >= 80:
            messages.append(f"👍 Great job, {name}! You're doing really well!")
        elif recent_avg >= 70:
            messages.append(f"📚 Good effort, {name}! Keep working hard!")
        elif recent_avg >= 60:
            messages.append(f"💪 {name}, you need to put in more effort. You can do better!")
        else:
            messages.append(f"⚠️ {name}, your performance needs significant improvement. Work harder!")
        
        # Add trend-based message
        if recent_trend > 5:
            messages.append(f"📈 You're improving! Keep up the momentum, {name}!")
        elif recent_trend < -5:
            messages.append(f"📉 {name}, your recent performance is declining. Focus more on your studies!")
        
        # Add subject-specific advice
        if self.progress[username]:
            subject_scores = {}
            for entry in self.progress[username]:
                subject = entry["subject"]
                percentage = (entry["score"] / entry["max_score"]) * 100
                if subject not in subject_scores:
                    subject_scores[subject] = []
                subject_scores[subject].append(percentage)
            
            # Find weakest subject
            subject_averages = {}
            for subject, scores in subject_scores.items():
                subject_averages[subject] = sum(scores) / len(scores)
            
            weakest_subject = min(subject_averages, key=subject_averages.get)
            strongest_subject = max(subject_averages, key=subject_averages.get)
            
            if subject_averages[weakest_subject] < 75:
                messages.append(f"Focus more on {weakest_subject}, {name}!")
            
            if subject_averages[strongest_subject] > 85:
                messages.append(f"You're excelling in {strongest_subject}! 🏆")
        
        return " ".join(messages)
    
    def view_progress(self, username=None):
        """View progress for a student"""
        if username is None:
            username = self.current_user
        
        if username not in self.progress:
            return []
        
        return self.progress[username]
    
    def get_statistics(self, username=None):
        """Get detailed statistics for a student"""
        if username is None:
            username = self.current_user
        
        if username not in self.progress or not self.progress[username]:
            return None
        
        entries = self.progress[username]
        scores = [(entry["score"] / entry["max_score"]) * 100 for entry in entries]
        
        stats = {
            "total_entries": len(entries),
            "average_score": sum(scores) / len(scores),
            "highest_score": max(scores),
            "lowest_score": min(scores),
            "subjects": list(set([entry["subject"] for entry in entries]))
        }
        
        return stats
    
    def is_admin(self):
        """Check if current user is admin"""
        return (self.current_user and 
                self.current_user in self.students and 
                self.students[self.current_user].get("role") == "admin")

def main():
    tracker = StudentProgressTracker()
    
    print("=" * 50)
    print("   📚 STUDENT PROGRESS TRACKER 📚")
    print("=" * 50)
    
    while True:
        if not tracker.current_user:
            print("\n🔐 LOGIN PORTAL")
            print("-" * 20)
            print("1. Login")
            print("2. Register New Student")
            print("3. Exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\n📝 LOGIN")
                username = input("Username: ").strip().lower()
                password = input("Password: ").strip()
                
                if tracker.login(username, password):
                    print(f"\n✅ Welcome back, {tracker.students[username]['full_name']}!")
                    print("\n" + "🎉 " + tracker.get_personalized_message())
                else:
                    print("\n❌ Invalid username or password!")
            
            elif choice == "2":
                print("\n📋 REGISTER NEW STUDENT")
                username = input("Choose a username: ").strip().lower()
                password = input("Choose a password: ").strip()
                full_name = input("Full Name: ").strip()
                email = input("Email: ").strip()
                
                success, message = tracker.register_student(username, password, full_name, email)
                if success:
                    print(f"\n✅ {message}")
                else:
                    print(f"\n❌ {message}")
            
            elif choice == "3":
                print("\n👋 Goodbye!")
                break
            
            else:
                print("\n❌ Invalid choice!")
        
        else:
            # Main menu for logged-in users
            print(f"\n👤 Logged in as: {tracker.students[tracker.current_user]['full_name']}")
            print("\n📊 MAIN MENU")
            print("-" * 20)
            print("1. Add New Progress Entry")
            print("2. View My Progress")
            print("3. View My Statistics")
            print("4. Get Personalized Message")
            
            if tracker.is_admin():
                print("5. View All Students (Admin)")
                print("6. View Any Student's Progress (Admin)")
            
            print("0. Logout")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                print("\n📝 ADD PROGRESS ENTRY")
                subject = input("Subject: ").strip()
                try:
                    score = int(input("Score obtained: "))
                    max_score = int(input("Maximum score (default 100): ") or "100")
                    
                    success, message = tracker.add_progress(subject, score, max_score)
                    if success:
                        print(f"\n✅ {message}")
                        print("\n💌 Updated Message:")
                        print(tracker.get_personalized_message())
                    else:
                        print(f"\n❌ {message}")
                except ValueError:
                    print("\n❌ Please enter valid numbers for scores!")
            
            elif choice == "2":
                print("\n📈 YOUR PROGRESS")
                print("-" * 30)
                progress = tracker.view_progress()
                
                if progress:
                    for i, entry in enumerate(progress, 1):
                        percentage = (entry["score"] / entry["max_score"]) * 100
                        print(f"{i}. {entry['subject']}: {entry['score']}/{entry['max_score']} ({percentage:.1f}%) - {entry['date']}")
                else:
                    print("No progress entries found.")
            
            elif choice == "3":
                print("\n📊 YOUR STATISTICS")
                print("-" * 30)
                stats = tracker.get_statistics()
                
                if stats:
                    print(f"Total Entries: {stats['total_entries']}")
                    print(f"Average Score: {stats['average_score']:.1f}%")
                    print(f"Highest Score: {stats['highest_score']:.1f}%")
                    print(f"Lowest Score: {stats['lowest_score']:.1f}%")
                    print(f"Subjects: {', '.join(stats['subjects'])}")
                else:
                    print("No statistics available yet.")
            
            elif choice == "4":
                print("\n💌 PERSONALIZED MESSAGE")
                print("-" * 40)
                print(tracker.get_personalized_message())
            
            elif choice == "5" and tracker.is_admin():
                print("\n👥 ALL STUDENTS")
                print("-" * 30)
                for username, info in tracker.students.items():
                    if info.get("role") != "admin":
                        print(f"• {info['full_name']} ({username}) - {info['email']}")
            
            elif choice == "6" and tracker.is_admin():
                print("\n🔍 VIEW STUDENT PROGRESS")
                student_username = input("Enter student username: ").strip().lower()
                
                if student_username in tracker.students:
                    print(f"\n📈 PROGRESS FOR {tracker.students[student_username]['full_name']}")
                    print("-" * 40)
                    progress = tracker.view_progress(student_username)
                    
                    if progress:
                        for i, entry in enumerate(progress, 1):
                            percentage = (entry["score"] / entry["max_score"]) * 100
                            print(f"{i}. {entry['subject']}: {entry['score']}/{entry['max_score']} ({percentage:.1f}%) - {entry['date']}")
                        
                        print("\n💌 Personalized Message for this student:")
                        print(tracker.get_personalized_message(student_username))
                    else:
                        print("No progress entries found for this student.")
                else:
                    print("❌ Student not found!")
            
            elif choice == "0":
                print(f"\n👋 Goodbye, {tracker.students[tracker.current_user]['full_name']}!")
                tracker.current_user = None
            
            else:
                print("\n❌ Invalid choice!")

if __name__ == "__main__":
    main()