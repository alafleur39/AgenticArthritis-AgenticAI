export interface User {
  id: string;
  name: string;
  email: string;
  diagnosisDate: string;
  arthritisType: 'rheumatoid' | 'osteoarthritis' | 'psoriatic' | 'other';
  preferences: UserPreferences;
}

export interface UserPreferences {
  emailReminders: boolean;
  reminderFrequency: 'daily' | 'twice-daily' | 'weekly';
  preferredExerciseTime: string;
  difficultyLevel: 'beginner' | 'intermediate' | 'advanced';
  motivationalMessages: boolean;
}

export interface Exercise {
  id: string;
  name: string;
  description: string;
  instructions: string[];
  duration: number; // in seconds
  repetitions: number;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  targetAreas: string[];
  videoUrl?: string;
  imageUrl?: string;
}

export interface ExerciseSession {
  id: string;
  exerciseId: string;
  userId: string;
  date: string;
  completed: boolean;
  duration: number;
  repetitionsCompleted: number;
  painLevel: number; // 1-10 scale
  notes?: string;
}

export interface HandMovementData {
  id: string;
  userId: string;
  sessionId: string;
  timestamp: string;
  movementType: 'flexion' | 'extension' | 'grip' | 'pinch';
  accuracy: number; // percentage
  speed: number;
  range: number;
}

export interface ProgressData {
  date: string;
  exercisesCompleted: number;
  totalExercises: number;
  averagePainLevel: number;
  averageAccuracy: number;
  streakDays: number;
}

export interface MotivationalMessage {
  id: string;
  message: string;
  type: 'encouragement' | 'tip' | 'achievement' | 'reminder';
  date: string;
}

export interface EmailReminder {
  id: string;
  userId: string;
  type: 'exercise' | 'medication' | 'appointment';
  scheduledTime: string;
  message: string;
  sent: boolean;
}