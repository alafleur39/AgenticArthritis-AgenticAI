import React from 'react'
import { Calendar, Clock, Target, Zap, MessageCircle } from 'lucide-react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import ProgressBar from '../components/ui/ProgressBar'
import { mockProgressData, mockMotivationalMessages, mockExercises } from '../utils/mockData'

const Dashboard: React.FC = () => {
  const today = new Date().toISOString().split('T')[0]
  const todayProgress = mockProgressData.find(p => p.date === today) || mockProgressData[mockProgressData.length - 1]
  const todayMessage = mockMotivationalMessages[0]
  
  const upcomingExercises = mockExercises.slice(0, 3)
  
  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg p-6 text-white">
        <h2 className="text-2xl font-bold mb-2">Good morning! Ready for today's exercises?</h2>
        <p className="text-primary-100">
          You're on a {todayProgress.streakDays}-day streak! Keep up the great work.
        </p>
      </div>

      {/* Motivational Message */}
      <Card className="bg-blue-50 border-blue-200">
        <div className="flex items-start space-x-3">
          <MessageCircle className="h-5 w-5 text-blue-600 mt-1" />
          <div>
            <h3 className="font-medium text-blue-900">Daily Motivation</h3>
            <p className="text-blue-800 mt-1">{todayMessage.message}</p>
          </div>
        </div>
      </Card>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Today's Progress</p>
              <p className="text-2xl font-bold text-gray-900">
                {todayProgress.exercisesCompleted}/{todayProgress.totalExercises}
              </p>
            </div>
            <Target className="h-8 w-8 text-primary-600" />
          </div>
          <ProgressBar 
            value={todayProgress.exercisesCompleted} 
            max={todayProgress.totalExercises} 
            className="mt-3"
          />
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Streak Days</p>
              <p className="text-2xl font-bold text-gray-900">{todayProgress.streakDays}</p>
            </div>
            <Zap className="h-8 w-8 text-yellow-500" />
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Pain Level</p>
              <p className="text-2xl font-bold text-gray-900">{todayProgress.averagePainLevel}/10</p>
            </div>
            <div className={`h-8 w-8 rounded-full flex items-center justify-center ${
              todayProgress.averagePainLevel <= 3 ? 'bg-green-100 text-green-600' :
              todayProgress.averagePainLevel <= 6 ? 'bg-yellow-100 text-yellow-600' :
              'bg-red-100 text-red-600'
            }`}>
              <span className="text-sm font-bold">{todayProgress.averagePainLevel}</span>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Accuracy</p>
              <p className="text-2xl font-bold text-gray-900">{todayProgress.averageAccuracy}%</p>
            </div>
            <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
              <span className="text-sm font-bold text-primary-600">{todayProgress.averageAccuracy}%</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Today's Exercises */}
      <Card title="Today's Recommended Exercises" subtitle="Complete these exercises to maintain your progress">
        <div className="space-y-4">
          {upcomingExercises.map((exercise) => (
            <div key={exercise.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex-1">
                <h4 className="font-medium text-gray-900">{exercise.name}</h4>
                <p className="text-sm text-gray-600 mt-1">{exercise.description}</p>
                <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                  <span className="flex items-center">
                    <Clock className="h-3 w-3 mr-1" />
                    {Math.floor(exercise.duration / 60)}m {exercise.duration % 60}s
                  </span>
                  <span className="capitalize">{exercise.difficulty}</span>
                </div>
              </div>
              <Button size="sm">Start</Button>
            </div>
          ))}
        </div>
        <div className="mt-6 text-center">
          <Button variant="outline" className="w-full">View All Exercises</Button>
        </div>
      </Card>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card title="Quick Actions">
          <div className="space-y-3">
            <Button className="w-full justify-start" variant="outline">
              <Calendar className="h-4 w-4 mr-2" />
              Schedule Exercise Reminder
            </Button>
            <Button className="w-full justify-start" variant="outline">
              <MessageCircle className="h-4 w-4 mr-2" />
              Log Pain Level
            </Button>
            <Button className="w-full justify-start" variant="outline">
              <Target className="h-4 w-4 mr-2" />
              View Progress Report
            </Button>
          </div>
        </Card>

        <Card title="Recent Activity">
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <div className="h-2 w-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Completed Finger Flexion exercise</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="h-2 w-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Completed Wrist Circles exercise</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="h-2 w-2 bg-blue-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Received motivational message</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="h-2 w-2 bg-yellow-500 rounded-full"></div>
              <span className="text-sm text-gray-600">Email reminder sent</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}

export default Dashboard