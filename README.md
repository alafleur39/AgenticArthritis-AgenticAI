# Agent Arthritis - AI-Powered Arthritis Management System

🏆 **Hackathon Project** - Complete AI-powered arthritis management system with personalized exercise recommendations, automated email reminders, and progress tracking.

## 🎯 Project Overview

Agent Arthritis is a comprehensive full-stack application that helps people diagnosed with arthritis manage their condition through:

- **AI-Generated Personalized Exercises** - Custom hand exercises based on arthritis type and severity
- **Automated Email Reminders** - Smart scheduling for exercise reminders and motivational messages  
- **Progress Tracking** - Monitor hand movement improvements and exercise completion
- **User-Friendly Interface** - Beautiful React frontend with authentication and dashboard

## 🚀 Features

### Backend (FastAPI)
- ✅ **AI Agent** - OpenAI-powered exercise generation and progress analysis
- ✅ **Email Automation** - SendGrid integration for reminders and motivation
- ✅ **Smart Scheduling** - APScheduler for automated daily/weekly tasks
- ✅ **Database Models** - SQLAlchemy with User, Exercise, Progress, Reminder entities
- ✅ **REST API** - Complete endpoints for authentication, exercises, progress tracking
- ✅ **Authentication** - JWT-based secure user authentication

### Frontend (React + TypeScript)
- ✅ **Modern UI** - Responsive design with custom CSS utilities
- ✅ **Authentication System** - Login/register with protected routes
- ✅ **Dashboard** - Clean interface showing system status
- ✅ **API Integration** - Full backend connectivity
- ✅ **TypeScript** - Type-safe development with proper interfaces

## 🛠 Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (Database ORM)
- OpenAI API (AI exercise generation)
- SendGrid (Email service)
- APScheduler (Task automation)
- JWT (Authentication)
- SQLite (Database)

**Frontend:**
- React 19.2.0
- TypeScript
- Vite (Build tool)
- React Router (Navigation)
- Custom CSS utilities

## 🏃‍♂️ Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python create_demo_user.py
python run.py
```
Backend runs on: `http://localhost:8000`

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: `http://localhost:12001`

### Demo Account
- **Email:** demo@agentarthritis.com
- **Password:** demo123

## 📁 Project Structure

```
AgenticArthritis-AgenticAI/
├── backend/
│   ├── app/
│   │   ├── api/          # REST API endpoints
│   │   ├── models/       # Database models
│   │   ├── services/     # AI agent, email, scheduler
│   │   ├── core/         # Configuration
│   │   └── db/           # Database setup
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── contexts/     # React contexts
│   │   ├── pages/        # Login, Register, Dashboard
│   │   └── services/     # API client
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 🎯 API Endpoints

- `POST /auth/token` - User authentication
- `GET /auth/me` - Get current user
- `GET /exercises/` - List user exercises
- `POST /exercises/generate` - Generate AI exercises
- `GET /progress/` - Get user progress
- `POST /progress/` - Record exercise progress
- `GET /reminders/` - List user reminders
- `POST /reminders/` - Create reminder

## 🤖 AI Features

The AI agent provides:
- **Personalized Exercise Generation** - Based on arthritis type, severity, and user preferences
- **Progress Analysis** - AI-powered insights on improvement trends
- **Motivational Content** - Personalized encouragement messages
- **Adaptive Recommendations** - Exercises adjust based on user progress

## 📧 Email Automation

Automated email system includes:
- **Daily Exercise Reminders** - Customizable timing
- **Weekly Progress Summaries** - AI-generated progress reports
- **Motivational Messages** - Encouraging content to maintain engagement
- **Exercise Notifications** - New exercise recommendations

## 🎨 UI/UX Highlights

- **Responsive Design** - Works on desktop and mobile
- **Clean Interface** - Intuitive navigation and clear information hierarchy
- **Authentication Flow** - Secure login/register with protected routes
- **Loading States** - Smooth user experience with proper feedback
- **Error Handling** - User-friendly error messages

## 🔧 Configuration

### Environment Variables
Create `.env` files in backend directory:
```
OPENAI_API_KEY=your_openai_key
SENDGRID_API_KEY=your_sendgrid_key
SENDGRID_FROM_EMAIL=your_email@domain.com
SECRET_KEY=your_secret_key
```

## 🚀 Deployment Ready

The application is structured for easy deployment:
- **Backend** - FastAPI with uvicorn server
- **Frontend** - Vite build system for production
- **Database** - SQLite for development, easily switchable to PostgreSQL
- **Environment** - Configurable settings for different environments

## 🏆 Hackathon Highlights

This project demonstrates:
- **Full-Stack Development** - Complete frontend and backend integration
- **AI Integration** - Practical use of OpenAI for healthcare applications
- **Real-World Problem Solving** - Addresses genuine needs of arthritis patients
- **Modern Tech Stack** - Current best practices and technologies
- **Production Ready** - Proper authentication, error handling, and structure

## 📈 Future Enhancements

- Hand movement tracking with computer vision
- Mobile app development
- Integration with wearable devices
- Advanced analytics dashboard
- Telemedicine integration
- Multi-language support

---

**Built for Hackathon** - A complete AI-powered healthcare solution ready for demo and further development.