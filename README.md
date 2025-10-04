# Agent Arthritis - AI-Powered Arthritis Management

A comprehensive React frontend application designed to help people diagnosed with arthritis manage their condition through personalized exercises, progress tracking, and AI-powered insights.

## Features

### 🏠 Dashboard
- Daily progress overview with completion rates
- Current exercise streak tracking
- Motivational messages and health tips
- Quick access to today's recommended exercises
- Real-time pain level and accuracy metrics

### 💪 Exercise Management
- Personalized hand exercises for arthritis
- Step-by-step exercise instructions
- Real-time hand movement tracking
- Progress monitoring and completion tracking
- Difficulty levels (Beginner, Intermediate, Advanced)

### 📊 Progress Analytics
- Interactive charts showing exercise completion trends
- Pain level tracking over time
- Movement accuracy analysis
- Weekly and monthly progress summaries
- Achievement badges and milestones

### ⚙️ Settings & Customization
- Email reminder configuration
- Exercise difficulty preferences
- Notification settings
- Profile management
- Privacy and security controls

### 🤖 AI Features
- **Hand Movement Tracking**: AI analyzes hand movements during exercises
- **Personalized Recommendations**: Exercises tailored to your arthritis type
- **Progress Insights**: AI-powered analysis of your improvement patterns
- **Motivational Messages**: Daily encouragement and tips
- **Email Reminders**: Automated exercise reminders via email

## Technology Stack

- **Frontend**: React 19 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **Routing**: React Router DOM

## Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone https://github.com/alafleur39/AgenticArthritis-AgenticAI.git
cd AgenticArthritis-AgenticAI/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:12000`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ui/             # Basic UI components (Button, Card, etc.)
│   │   └── layout/         # Layout components (Header, Sidebar, etc.)
│   ├── pages/              # Main application pages
│   │   ├── Dashboard.tsx   # Main dashboard
│   │   ├── Exercises.tsx   # Exercise management
│   │   ├── Progress.tsx    # Progress tracking
│   │   └── Settings.tsx    # User settings
│   ├── types/              # TypeScript type definitions
│   ├── utils/              # Utility functions and mock data
│   └── styles/             # Global styles and Tailwind config
├── public/                 # Static assets
└── package.json           # Project dependencies and scripts
```

## Key Components

### Exercise Types
- **Finger Flexion**: Gentle finger bending exercises
- **Wrist Circles**: Circular wrist movements for mobility
- **Thumb Opposition**: Dexterity improvement exercises
- **Grip Strengthening**: Resistance exercises for hand strength

### Data Tracking
- Exercise completion rates
- Pain levels (1-10 scale)
- Movement accuracy percentages
- Exercise streaks and consistency
- Time spent exercising

### AI Integration Points
- Hand movement analysis during exercises
- Personalized exercise recommendations
- Progress pattern recognition
- Automated email reminder system
- Motivational message generation

## Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones
- Various screen sizes and orientations

## Accessibility Features

- Keyboard navigation support
- Screen reader compatibility
- High contrast color schemes
- Large touch targets for mobile
- Clear visual hierarchy

## Future Enhancements

- Video exercise demonstrations
- Voice-guided exercise instructions
- Integration with wearable devices
- Telemedicine appointment scheduling
- Social features for community support
- Advanced AI coaching recommendations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@agentarthritis.com or create an issue in the GitHub repository.

---

**Agent Arthritis** - Empowering arthritis management through AI technology 🤖💙