import React, { useState } from 'react'
import { Mail, Clock, Bell, User, Shield, Palette } from 'lucide-react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { mockUser } from '../utils/mockData'

const Settings: React.FC = () => {
  const [preferences, setPreferences] = useState(mockUser.preferences)
  const [profile, setProfile] = useState({
    name: mockUser.name,
    email: mockUser.email,
    arthritisType: mockUser.arthritisType
  })

  const handlePreferenceChange = (key: string, value: any) => {
    setPreferences(prev => ({ ...prev, [key]: value }))
  }

  const handleProfileChange = (key: string, value: string) => {
    setProfile(prev => ({ ...prev, [key]: value }))
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-1">
          Customize your Agent Arthritis experience and manage your preferences
        </p>
      </div>

      {/* Profile Settings */}
      <Card title="Profile Information" className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <input
              type="text"
              value={profile.name}
              onChange={(e) => handleProfileChange('name', e.target.value)}
              className="input w-full"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <input
              type="email"
              value={profile.email}
              onChange={(e) => handleProfileChange('email', e.target.value)}
              className="input w-full"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Arthritis Type
            </label>
            <select
              value={profile.arthritisType}
              onChange={(e) => handleProfileChange('arthritisType', e.target.value)}
              className="input w-full"
            >
              <option value="rheumatoid">Rheumatoid Arthritis</option>
              <option value="osteoarthritis">Osteoarthritis</option>
              <option value="psoriatic">Psoriatic Arthritis</option>
              <option value="other">Other</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Diagnosis Date
            </label>
            <input
              type="date"
              defaultValue={mockUser.diagnosisDate}
              className="input w-full"
            />
          </div>
        </div>
        
        <div className="pt-4 border-t border-gray-200">
          <Button>Save Profile Changes</Button>
        </div>
      </Card>

      {/* Email Reminder Settings */}
      <Card title="Email Reminders" subtitle="Configure when and how often you receive exercise reminders">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Mail className="h-5 w-5 text-gray-400" />
              <div>
                <h4 className="font-medium text-gray-900">Enable Email Reminders</h4>
                <p className="text-sm text-gray-600">Receive automated exercise reminders via email</p>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={preferences.emailReminders}
                onChange={(e) => handlePreferenceChange('emailReminders', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>

          {preferences.emailReminders && (
            <div className="ml-8 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Reminder Frequency
                </label>
                <select
                  value={preferences.reminderFrequency}
                  onChange={(e) => handlePreferenceChange('reminderFrequency', e.target.value)}
                  className="input w-full max-w-xs"
                >
                  <option value="daily">Daily</option>
                  <option value="twice-daily">Twice Daily</option>
                  <option value="weekly">Weekly</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Preferred Exercise Time
                </label>
                <input
                  type="time"
                  value={preferences.preferredExerciseTime}
                  onChange={(e) => handlePreferenceChange('preferredExerciseTime', e.target.value)}
                  className="input w-full max-w-xs"
                />
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* Exercise Preferences */}
      <Card title="Exercise Preferences" subtitle="Customize your exercise experience">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty Level
            </label>
            <select
              value={preferences.difficultyLevel}
              onChange={(e) => handlePreferenceChange('difficultyLevel', e.target.value)}
              className="input w-full max-w-xs"
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
            <p className="text-sm text-gray-600 mt-1">
              This affects which exercises are recommended to you
            </p>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Bell className="h-5 w-5 text-gray-400" />
              <div>
                <h4 className="font-medium text-gray-900">Motivational Messages</h4>
                <p className="text-sm text-gray-600">Receive daily encouragement and tips</p>
              </div>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={preferences.motivationalMessages}
                onChange={(e) => handlePreferenceChange('motivationalMessages', e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>
        </div>
      </Card>

      {/* Notification Settings */}
      <Card title="Notification Settings" subtitle="Control how you receive updates and alerts">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">Exercise Reminders</h4>
              <p className="text-sm text-gray-600">Get notified when it's time to exercise</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" defaultChecked className="sr-only peer" />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">Progress Updates</h4>
              <p className="text-sm text-gray-600">Weekly progress summaries and achievements</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" defaultChecked className="sr-only peer" />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">Health Tips</h4>
              <p className="text-sm text-gray-600">Receive helpful arthritis management tips</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" defaultChecked className="sr-only peer" />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>
        </div>
      </Card>

      {/* Privacy & Security */}
      <Card title="Privacy & Security" subtitle="Manage your data and privacy settings">
        <div className="space-y-4">
          <div className="flex items-center space-x-3">
            <Shield className="h-5 w-5 text-green-600" />
            <div>
              <h4 className="font-medium text-gray-900">Data Encryption</h4>
              <p className="text-sm text-gray-600">Your health data is encrypted and secure</p>
            </div>
          </div>

          <div className="space-y-2">
            <Button variant="outline" className="w-full justify-start">
              <User className="h-4 w-4 mr-2" />
              Download My Data
            </Button>
            <Button variant="outline" className="w-full justify-start">
              <Shield className="h-4 w-4 mr-2" />
              Privacy Policy
            </Button>
            <Button variant="outline" className="w-full justify-start text-red-600 hover:text-red-700">
              Delete Account
            </Button>
          </div>
        </div>
      </Card>

      {/* Save Changes */}
      <div className="flex justify-end space-x-3">
        <Button variant="outline">Reset to Defaults</Button>
        <Button>Save All Changes</Button>
      </div>
    </div>
  )
}

export default Settings