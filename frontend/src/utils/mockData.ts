import { User, Exercise, ExerciseSession, ProgressData, MotivationalMessage } from '../types';

export const mockUser: User = {
  id: '1',
  name: 'Sarah Johnson',
  email: 'sarah.johnson@email.com',
  diagnosisDate: '2023-03-15',
  arthritisType: 'rheumatoid',
  preferences: {
    emailReminders: true,
    reminderFrequency: 'daily',
    preferredExerciseTime: '09:00',
    difficultyLevel: 'intermediate',
    motivationalMessages: true,
  },
};

export const mockExercises: Exercise[] = [
  {
    id: '1',
    name: 'Finger Flexion',
    description: 'Gentle finger bending exercise to improve flexibility',
    instructions: [
      'Start with your hand flat on a table',
      'Slowly curl your fingers into a fist',
      'Hold for 5 seconds',
      'Slowly straighten your fingers',
      'Repeat 10 times'
    ],
    duration: 300,
    repetitions: 10,
    difficulty: 'beginner',
    targetAreas: ['fingers', 'knuckles'],
  },
  {
    id: '2',
    name: 'Wrist Circles',
    description: 'Circular wrist movements to maintain joint mobility',
    instructions: [
      'Extend your arm in front of you',
      'Make slow circles with your wrist',
      'Complete 10 circles clockwise',
      'Complete 10 circles counterclockwise',
      'Switch hands and repeat'
    ],
    duration: 240,
    repetitions: 20,
    difficulty: 'beginner',
    targetAreas: ['wrist'],
  },
  {
    id: '3',
    name: 'Thumb Opposition',
    description: 'Touch thumb to each fingertip to improve dexterity',
    instructions: [
      'Hold your hand up with palm facing you',
      'Touch your thumb to your index finger',
      'Hold for 2 seconds',
      'Move to middle finger, then ring finger, then pinky',
      'Repeat sequence 5 times'
    ],
    duration: 180,
    repetitions: 5,
    difficulty: 'intermediate',
    targetAreas: ['thumb', 'fingers'],
  },
  {
    id: '4',
    name: 'Grip Strengthening',
    description: 'Squeeze a soft ball to build grip strength',
    instructions: [
      'Hold a stress ball or tennis ball',
      'Squeeze firmly but not painfully',
      'Hold for 5 seconds',
      'Release slowly',
      'Repeat 15 times'
    ],
    duration: 420,
    repetitions: 15,
    difficulty: 'intermediate',
    targetAreas: ['fingers', 'palm', 'wrist'],
  },
];

export const mockSessions: ExerciseSession[] = [
  {
    id: '1',
    exerciseId: '1',
    userId: '1',
    date: '2024-10-04',
    completed: true,
    duration: 280,
    repetitionsCompleted: 10,
    painLevel: 3,
    notes: 'Felt good today, less stiffness than yesterday',
  },
  {
    id: '2',
    exerciseId: '2',
    userId: '1',
    date: '2024-10-04',
    completed: true,
    duration: 240,
    repetitionsCompleted: 20,
    painLevel: 2,
  },
  {
    id: '3',
    exerciseId: '3',
    userId: '1',
    date: '2024-10-03',
    completed: true,
    duration: 180,
    repetitionsCompleted: 5,
    painLevel: 4,
  },
];

export const mockProgressData: ProgressData[] = [
  { date: '2024-09-28', exercisesCompleted: 3, totalExercises: 4, averagePainLevel: 3.5, averageAccuracy: 85, streakDays: 1 },
  { date: '2024-09-29', exercisesCompleted: 4, totalExercises: 4, averagePainLevel: 3.2, averageAccuracy: 87, streakDays: 2 },
  { date: '2024-09-30', exercisesCompleted: 2, totalExercises: 4, averagePainLevel: 4.1, averageAccuracy: 82, streakDays: 0 },
  { date: '2024-10-01', exercisesCompleted: 4, totalExercises: 4, averagePainLevel: 2.8, averageAccuracy: 90, streakDays: 1 },
  { date: '2024-10-02', exercisesCompleted: 3, totalExercises: 4, averagePainLevel: 3.0, averageAccuracy: 88, streakDays: 2 },
  { date: '2024-10-03', exercisesCompleted: 4, totalExercises: 4, averagePainLevel: 2.5, averageAccuracy: 92, streakDays: 3 },
  { date: '2024-10-04', exercisesCompleted: 2, totalExercises: 4, averagePainLevel: 2.5, averageAccuracy: 89, streakDays: 4 },
];

export const mockMotivationalMessages: MotivationalMessage[] = [
  {
    id: '1',
    message: "Great job completing your exercises yesterday! Consistency is key to managing arthritis effectively.",
    type: 'encouragement',
    date: '2024-10-04',
  },
  {
    id: '2',
    message: "Tip: Try doing your hand exercises in warm water to help reduce stiffness and pain.",
    type: 'tip',
    date: '2024-10-03',
  },
  {
    id: '3',
    message: "🎉 Congratulations! You've maintained a 4-day exercise streak. Keep up the excellent work!",
    type: 'achievement',
    date: '2024-10-04',
  },
  {
    id: '4',
    message: "Remember: It's time for your morning hand exercises. Your joints will thank you!",
    type: 'reminder',
    date: '2024-10-04',
  },
];