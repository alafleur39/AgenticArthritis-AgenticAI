import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { Login } from './pages/Login';
import { Register } from './pages/Register';

// Enhanced Dashboard component for demo
const Dashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">🤖 Agent Arthritis</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">Demo Mode - All Features Active</span>
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Welcome Section */}
          <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                🎉 Welcome to Agent Arthritis!
              </h2>
              <p className="text-lg text-gray-600 mb-6">
                Your AI-powered arthritis management system is ready for demo.
              </p>
            </div>
          </div>

          {/* System Status Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-green-800 mb-2">🤖 AI Agent</h3>
              <p className="text-sm text-green-700 mb-2">Status: Active & Ready</p>
              <ul className="text-xs text-green-600 space-y-1">
                <li>• Personalized exercise generation</li>
                <li>• Progress analysis</li>
                <li>• Adaptive recommendations</li>
              </ul>
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-blue-800 mb-2">📧 Email Service</h3>
              <p className="text-sm text-blue-700 mb-2">Status: Configured</p>
              <ul className="text-xs text-blue-600 space-y-1">
                <li>• Daily exercise reminders</li>
                <li>• Weekly progress summaries</li>
                <li>• Motivational messages</li>
              </ul>
            </div>

            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-purple-800 mb-2">🔄 Automation</h3>
              <p className="text-sm text-purple-700 mb-2">Status: Running</p>
              <ul className="text-xs text-purple-600 space-y-1">
                <li>• Smart scheduling active</li>
                <li>• Background processing</li>
                <li>• Data synchronization</li>
              </ul>
            </div>
          </div>

          {/* Demo Features */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">🚀 Demo Features Available</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 mb-2">Backend API</h4>
                <p className="text-sm text-gray-600 mb-2">FastAPI server running on port 8000</p>
                <a 
                  href="http://localhost:8000/docs" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  → View API Documentation
                </a>
              </div>
              
              <div className="border border-gray-200 rounded-lg p-4">
                <h4 className="font-semibold text-gray-800 mb-2">Health Check</h4>
                <p className="text-sm text-gray-600 mb-2">System health and status</p>
                <a 
                  href="http://localhost:8000/health" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                >
                  → Check System Health
                </a>
              </div>
            </div>
          </div>

          {/* Technical Stack */}
          <div className="bg-gray-50 rounded-lg p-6 mt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">🛠 Technical Stack</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
              <div className="bg-white rounded-lg p-3">
                <div className="text-2xl mb-1">⚛️</div>
                <div className="text-sm font-medium">React 19</div>
              </div>
              <div className="bg-white rounded-lg p-3">
                <div className="text-2xl mb-1">🚀</div>
                <div className="text-sm font-medium">FastAPI</div>
              </div>
              <div className="bg-white rounded-lg p-3">
                <div className="text-2xl mb-1">🤖</div>
                <div className="text-sm font-medium">OpenAI</div>
              </div>
              <div className="bg-white rounded-lg p-3">
                <div className="text-2xl mb-1">📧</div>
                <div className="text-sm font-medium">SendGrid</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

// Simple wrapper for demo mode - no authentication required
const DemoRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return <>{children}</>;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Demo Routes - No authentication required */}
          <Route
            path="/"
            element={
              <DemoRoute>
                <Navigate to="/dashboard" replace />
              </DemoRoute>
            }
          />
          <Route
            path="/dashboard"
            element={
              <DemoRoute>
                <Dashboard />
              </DemoRoute>
            }
          />
          <Route
            path="/login"
            element={
              <DemoRoute>
                <Login />
              </DemoRoute>
            }
          />
          <Route
            path="/register"
            element={
              <DemoRoute>
                <Register />
              </DemoRoute>
            }
          />

          {/* Catch all route */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;