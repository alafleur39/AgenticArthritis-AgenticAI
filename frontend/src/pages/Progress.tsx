import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { TrendingUp, TrendingDown, Calendar, Award } from 'lucide-react'
import Card from '../components/ui/Card'
import { mockProgressData } from '../utils/mockData'

const Progress: React.FC = () => {
  const latestData = mockProgressData[mockProgressData.length - 1]
  const previousData = mockProgressData[mockProgressData.length - 2]
  
  const painTrend = latestData.averagePainLevel - previousData.averagePainLevel
  const accuracyTrend = latestData.averageAccuracy - previousData.averageAccuracy
  
  const chartData = mockProgressData.map(data => ({
    ...data,
    completionRate: (data.exercisesCompleted / data.totalExercises) * 100
  }))

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Progress Tracking</h1>
        <p className="text-gray-600 mt-1">
          Monitor your arthritis management journey and celebrate your achievements
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Current Streak</p>
              <p className="text-2xl font-bold text-gray-900">{latestData.streakDays} days</p>
            </div>
            <Award className="h-8 w-8 text-yellow-500" />
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Pain Level</p>
              <div className="flex items-center space-x-2">
                <p className="text-2xl font-bold text-gray-900">{latestData.averagePainLevel}/10</p>
                {painTrend < 0 ? (
                  <TrendingDown className="h-4 w-4 text-green-600" />
                ) : painTrend > 0 ? (
                  <TrendingUp className="h-4 w-4 text-red-600" />
                ) : null}
              </div>
            </div>
            <div className={`h-8 w-8 rounded-full flex items-center justify-center ${
              latestData.averagePainLevel <= 3 ? 'bg-green-100 text-green-600' :
              latestData.averagePainLevel <= 6 ? 'bg-yellow-100 text-yellow-600' :
              'bg-red-100 text-red-600'
            }`}>
              <span className="text-sm font-bold">{latestData.averagePainLevel}</span>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Exercise Accuracy</p>
              <div className="flex items-center space-x-2">
                <p className="text-2xl font-bold text-gray-900">{latestData.averageAccuracy}%</p>
                {accuracyTrend > 0 ? (
                  <TrendingUp className="h-4 w-4 text-green-600" />
                ) : accuracyTrend < 0 ? (
                  <TrendingDown className="h-4 w-4 text-red-600" />
                ) : null}
              </div>
            </div>
            <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
              <span className="text-sm font-bold text-primary-600">{latestData.averageAccuracy}%</span>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Weekly Average</p>
              <p className="text-2xl font-bold text-gray-900">
                {Math.round(mockProgressData.slice(-7).reduce((acc, d) => acc + (d.exercisesCompleted / d.totalExercises), 0) / 7 * 100)}%
              </p>
            </div>
            <Calendar className="h-8 w-8 text-primary-600" />
          </div>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Exercise Completion Rate" subtitle="Daily completion percentage over time">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                />
                <YAxis domain={[0, 100]} />
                <Tooltip 
                  labelFormatter={(value) => new Date(value).toLocaleDateString()}
                  formatter={(value: number) => [`${value.toFixed(1)}%`, 'Completion Rate']}
                />
                <Line 
                  type="monotone" 
                  dataKey="completionRate" 
                  stroke="#0ea5e9" 
                  strokeWidth={2}
                  dot={{ fill: '#0ea5e9', strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card title="Pain Level Tracking" subtitle="Average daily pain levels">
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockProgressData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="date" 
                  tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                />
                <YAxis domain={[0, 10]} />
                <Tooltip 
                  labelFormatter={(value) => new Date(value).toLocaleDateString()}
                  formatter={(value: number) => [`${value}/10`, 'Pain Level']}
                />
                <Bar 
                  dataKey="averagePainLevel" 
                  fill="#f59e0b"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      <Card title="Movement Accuracy Trends" subtitle="Hand movement precision over time">
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={mockProgressData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="date" 
                tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              />
              <YAxis domain={[70, 100]} />
              <Tooltip 
                labelFormatter={(value) => new Date(value).toLocaleDateString()}
                formatter={(value: number) => [`${value}%`, 'Accuracy']}
              />
              <Line 
                type="monotone" 
                dataKey="averageAccuracy" 
                stroke="#10b981" 
                strokeWidth={2}
                dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Achievements */}
      <Card title="Recent Achievements" subtitle="Celebrate your progress milestones">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div className="flex items-center space-x-3 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
            <Award className="h-8 w-8 text-yellow-600" />
            <div>
              <h4 className="font-medium text-yellow-900">4-Day Streak</h4>
              <p className="text-sm text-yellow-700">Consistent daily exercises</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg border border-green-200">
            <TrendingUp className="h-8 w-8 text-green-600" />
            <div>
              <h4 className="font-medium text-green-900">Improved Accuracy</h4>
              <p className="text-sm text-green-700">92% movement precision</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
            <TrendingDown className="h-8 w-8 text-blue-600" />
            <div>
              <h4 className="font-medium text-blue-900">Reduced Pain</h4>
              <p className="text-sm text-blue-700">Lower average pain level</p>
            </div>
          </div>
        </div>
      </Card>

      {/* Weekly Summary */}
      <Card title="This Week's Summary">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Exercise Statistics</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Total exercises completed:</span>
                <span className="font-medium">
                  {mockProgressData.slice(-7).reduce((acc, d) => acc + d.exercisesCompleted, 0)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Average completion rate:</span>
                <span className="font-medium">
                  {Math.round(mockProgressData.slice(-7).reduce((acc, d) => acc + (d.exercisesCompleted / d.totalExercises), 0) / 7 * 100)}%
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Best day:</span>
                <span className="font-medium">
                  {new Date(mockProgressData.slice(-7).reduce((best, current) => 
                    (current.exercisesCompleted / current.totalExercises) > (best.exercisesCompleted / best.totalExercises) ? current : best
                  ).date).toLocaleDateString('en-US', { weekday: 'long' })}
                </span>
              </div>
            </div>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Health Metrics</h4>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Average pain level:</span>
                <span className="font-medium">
                  {(mockProgressData.slice(-7).reduce((acc, d) => acc + d.averagePainLevel, 0) / 7).toFixed(1)}/10
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Average accuracy:</span>
                <span className="font-medium">
                  {Math.round(mockProgressData.slice(-7).reduce((acc, d) => acc + d.averageAccuracy, 0) / 7)}%
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Current streak:</span>
                <span className="font-medium">{latestData.streakDays} days</span>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}

export default Progress