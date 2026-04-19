import React, { useState, useEffect, useRef } from 'react';
import { Pause, Play, Square, Send, StepForward, Terminal, Brain, FileCode, User } from 'lucide-react';
import LandingPage from './components/LandingPage';
import './App.css';

type ActivityType = 'reasoning' | 'file_edit' | 'log' | 'thought' | 'user_input' | 'approval';
type AgentState = 'thinking' | 'acting' | 'paused' | 'idle' | 'pausing';

interface Activity {
  id: string;
  type: ActivityType;
  timestamp: string;
  content: any;
  status?: 'success' | 'failure' | 'active' | 'pending';
}

const App: React.FC = () => {
  const [view, setView] = useState<'landing' | 'dashboard'>('landing');

  if (view === 'landing') {
    return <LandingPage onLaunch={() => setView('dashboard')} />;
  }

  return <DashboardView />;
};

const DashboardView: React.FC = () => {
  const [activities, setActivities] = useState<Activity[]>([
    {
      id: '1',
      type: 'reasoning',
      timestamp: '12:45 PM',
      content: 'I need to investigate why the auth flow is failing in the production environment. Initial logs suggest a database timeout.'
    },
    {
      id: '2',
      type: 'file_edit',
      timestamp: '12:46 PM',
      content: {
        file: 'src/auth.py',
        diff: '- return False\n+ return user.is_authenticated'
      },
      status: 'success'
    }
  ]);
  const [agentState, setAgentState] = useState<AgentState>('acting');
  const [stepThrough, setStepThrough] = useState(false);
  const [inputValue, setInputValue] = useState('');
  const streamEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    streamEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [activities]);

  const togglePause = () => {
    if (agentState === 'paused') {
      setAgentState('acting');
    } else if (agentState === 'acting') {
      setAgentState('pausing');
      // Simulate transition to paused after current "tool call"
      setTimeout(() => {
        setAgentState('paused');
      }, 1500);
    }
  };

  const handleSendFeedback = () => {
    if (!inputValue.trim()) return;
    const newActivity: Activity = {
      id: Date.now().toString(),
      type: 'user_input',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      content: inputValue
    };
    setActivities(prev => [...prev, newActivity]);
    setInputValue('');
  };

  const handleApprove = (id: string) => {
    setActivities(prev => prev.map(a => a.id === id ? { ...a, status: 'success' } : a));
  };

  return (
    <div className="dashboard-container">
      <header className="nova-header">
        <div className="header-left">
          <div className="logo">
            <Square className="logo-icon" />
            <span className="logo-text">NOVA</span>
          </div>
          <div className="agent-info">
            <span className="agent-name">Gemma4-Super</span>
            <span className={`status-pill ${agentState}`}>
              {agentState === 'pausing' ? 'Pausing...' : agentState.charAt(0).toUpperCase() + agentState.slice(1)}
            </span>
          </div>
        </div>
        
        <div className="header-controls">
          <div className="step-toggle">
            <label className="toggle-label">
              <input 
                type="checkbox" 
                checked={stepThrough} 
                onChange={(e) => setStepThrough(e.target.checked)} 
              />
              <span className="toggle-text">STEP-THROUGH</span>
            </label>
          </div>
          
          <button 
            className={`control-btn pause-btn ${agentState === 'paused' ? 'resume' : ''} ${agentState === 'pausing' ? 'waiting' : ''}`} 
            onClick={togglePause}
            disabled={agentState === 'pausing'}
          >
            {agentState === 'paused' ? <Play size={18} /> : (agentState === 'pausing' ? <div className="spinner" /> : <Pause size={18} />)}
            <span>
              {agentState === 'paused' ? 'RESUME' : (agentState === 'pausing' ? 'WAITING...' : 'PAUSE')}
            </span>
          </button>
        </div>
      </header>

      <main className="code-stream">
        {activities.map((activity) => (
          <ActivityCard 
            key={activity.id} 
            activity={activity} 
            onApprove={() => handleApprove(activity.id)}
          />
        ))}
        {(agentState === 'acting' || agentState === 'thinking' || agentState === 'pausing') && (
          <ActivityCard 
            activity={{
              id: 'active',
              type: stepThrough ? 'approval' : (agentState === 'thinking' ? 'thought' : 'thought'),
              timestamp: 'Now',
              content: stepThrough 
                ? 'Should I proceed with the file edit?' 
                : (agentState === 'thinking' ? 'Agent is thinking...' : 'Applying the fix and running tests...'),
              status: stepThrough ? 'pending' : 'active'
            }} 
            onApprove={() => handleApprove('active')}
          />
        )}
        <div ref={streamEndRef} />
      </main>

      <footer className="feedback-footer">
        <div className="input-wrapper">
          <textarea 
            placeholder="Type feedback to the agent here..." 
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
                handleSendFeedback();
              }
            }}
          />
          <div className="input-actions">
            {(agentState === 'acting' || agentState === 'thinking') && (
              <span className="listening-indicator">
                <div className="dot" />
                LISTENING
              </span>
            )}
            <button className="send-btn" onClick={handleSendFeedback}>
              <Send size={18} />
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
};


const ActivityCard: React.FC<{ activity: Activity, onApprove?: () => void }> = ({ activity, onApprove }) => {
  const getIcon = () => {
    switch (activity.type) {
      case 'reasoning': return <Brain size={16} />;
      case 'file_edit': return <FileCode size={16} />;
      case 'log': return <Terminal size={16} />;
      case 'thought': return <Brain size={16} />;
      case 'user_input': return <User size={16} />;
      case 'approval': return <StepForward size={16} />;
    }
  };

  return (
    <div className={`activity-card ${activity.type} ${activity.status || ''}`}>
      <div className="card-header">
        <div className="type-indicator">
          {getIcon()}
          <span>{activity.type.replace('_', ' ').toUpperCase()}</span>
          {activity.status === 'active' && <div className="spinner mini" />}
        </div>
        <span className="timestamp">{activity.timestamp}</span>
      </div>
      <div className="card-content">
        {activity.type === 'file_edit' ? (
          <div className="file-edit-content">
            <div className="file-path">{activity.content.file}</div>
            <pre className="code-diff">
              {activity.content.diff.split('\n').map((line: string, i: number) => (
                <div key={i} className={`diff-line ${line.startsWith('+') ? 'add' : line.startsWith('-') ? 'remove' : ''}`}>
                  {line}
                </div>
              ))}
            </pre>
          </div>
        ) : (
          <p>{activity.content}</p>
        )}
      </div>
      
      {activity.status === 'pending' && (
        <div className="approval-actions">
          <button className="approve-btn" onClick={onApprove}>
            <Play size={14} />
            <span>PROCEED</span>
          </button>
          <button className="reject-btn">
            <Square size={14} />
            <span>CANCEL</span>
          </button>
        </div>
      )}

      {activity.status === 'active' && <div className="active-glow" />}
    </div>
  );
};

export default App;
