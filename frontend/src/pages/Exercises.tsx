import React, { useState } from 'react'
import { Play, Clock, Target, CheckCircle, AlertCircle } from 'lucide-react'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import { mockExercises, mockSessions } from '../utils/mockData'
import { Exercise } from '../types'

const Exercises: React.FC = () => {
  const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null)
  const [isExercising, setIsExercising] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [timer, setTimer] = useState(0)

  const completedToday = mockSessions.filter(s => s.date === new Date().toISOString().split('T')[0])
  const completedExerciseIds = completedToday.map(s => s.exerciseId)

  const startExercise = (exercise: Exercise) => {
    setSelectedExercise(exercise)
    setIsExercising(true)
    setCurrentStep(0)
    setTimer(0)
  }

  const nextStep = () => {
    if (selectedExercise && currentStep < selectedExercise.instructions.length - 1) {
      setCurrentStep(currentStep + 1)
    } else {
      completeExercise()
    }
  }

  const completeExercise = () => {
    setIsExercising(false)
    setSelectedExercise(null)
    setCurrentStep(0)
    setTimer(0)
  }

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800'
      case 'intermediate': return 'bg-yellow-100 text-yellow-800'
      case 'advanced': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (isExercising && selectedExercise) {
    return (
      <div className="max-w-2xl mx-auto">
        <Card>
          <div className="text-center mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{selectedExercise.name}</h2>
            <p className="text-gray-600">{selectedExercise.description}</p>
          </div>

          <div className="mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">
                Step {currentStep + 1} of {selectedExercise.instructions.length}
              </span>
              <span className="text-sm text-gray-500">
                {Math.floor(timer / 60)}:{(timer % 60).toString().padStart(2, '0')}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentStep + 1) / selectedExercise.instructions.length) * 100}%` }}
              />
            </div>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
            <h3 className="font-medium text-blue-900 mb-2">Current Step:</h3>
            <p className="text-blue-800 text-lg">{selectedExercise.instructions[currentStep]}</p>
          </div>

          <div className="flex space-x-3">
            <Button variant="outline" onClick={completeExercise} className="flex-1">
              Stop Exercise
            </Button>
            <Button onClick={nextStep} className="flex-1">
              {currentStep < selectedExercise.instructions.length - 1 ? 'Next Step' : 'Complete'}
            </Button>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Hand Exercises</h1>
          <p className="text-gray-600 mt-1">
            Personalized exercises designed for your arthritis management
          </p>
        </div>
      </div>

      {/* Progress Summary */}
      <Card>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{completedToday.length}</div>
            <div className="text-sm text-gray-600">Completed Today</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">{mockExercises.length - completedToday.length}</div>
            <div className="text-sm text-gray-600">Remaining</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {completedToday.reduce((acc, s) => acc + s.duration, 0) / 60}m
            </div>
            <div className="text-sm text-gray-600">Time Exercised</div>
          </div>
        </div>
      </Card>

      {/* Exercise List */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {mockExercises.map((exercise) => {
          const isCompleted = completedExerciseIds.includes(exercise.id)
          
          return (
            <Card key={exercise.id} className={isCompleted ? 'bg-green-50 border-green-200' : ''}>
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="text-lg font-semibold text-gray-900">{exercise.name}</h3>
                    {isCompleted && <CheckCircle className="h-5 w-5 text-green-600" />}
                  </div>
                  <p className="text-gray-600 text-sm mb-3">{exercise.description}</p>
                  
                  <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                    <span className="flex items-center">
                      <Clock className="h-4 w-4 mr-1" />
                      {Math.floor(exercise.duration / 60)}m {exercise.duration % 60}s
                    </span>
                    <span className="flex items-center">
                      <Target className="h-4 w-4 mr-1" />
                      {exercise.repetitions} reps
                    </span>
                  </div>
                  
                  <div className="flex items-center space-x-2 mb-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(exercise.difficulty)}`}>
                      {exercise.difficulty}
                    </span>
                    <div className="flex space-x-1">
                      {exercise.targetAreas.map((area) => (
                        <span key={area} className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">
                          {area}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="space-y-2">
                <h4 className="font-medium text-gray-900 text-sm">Instructions:</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  {exercise.instructions.slice(0, 2).map((instruction, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-primary-600 mr-2">{index + 1}.</span>
                      {instruction}
                    </li>
                  ))}
                  {exercise.instructions.length > 2 && (
                    <li className="text-gray-400 italic">
                      +{exercise.instructions.length - 2} more steps...
                    </li>
                  )}
                </ul>
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <Button 
                  onClick={() => startExercise(exercise)}
                  className="w-full"
                  variant={isCompleted ? 'secondary' : 'primary'}
                >
                  <Play className="h-4 w-4 mr-2" />
                  {isCompleted ? 'Repeat Exercise' : 'Start Exercise'}
                </Button>
              </div>
            </Card>
          )
        })}
      </div>

      {/* Hand Movement Tracking Info */}
      <Card title="Hand Movement Tracking" className="bg-gradient-to-r from-purple-50 to-pink-50 border-purple-200">
        <div className="flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 text-purple-600 mt-1" />
          <div>
            <p className="text-purple-900 mb-2">
              Our AI tracks your hand movements during exercises to provide personalized feedback and progress insights.
            </p>
            <ul className="text-sm text-purple-800 space-y-1">
              <li>• Real-time movement accuracy analysis</li>
              <li>• Range of motion measurements</li>
              <li>• Speed and coordination tracking</li>
              <li>• Personalized improvement suggestions</li>
            </ul>
          </div>
        </div>
      </Card>
    </div>
  )
}

export default Exercises