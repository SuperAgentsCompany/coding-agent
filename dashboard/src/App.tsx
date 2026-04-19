import React, { useState, useEffect, useRef } from 'react';
import { Pause, Play, Square, Send, StepForward, Terminal, Brain, FileCode, User, BarChart3, Activity as ActivityIcon, MessageSquare, ChevronRight, Info } from 'lucide-react';
import LandingPage from './components/LandingPage';
import { benchmarkData, Evaluation } from './data/benchmarkData';
import './App.css';

type ActivityType = 'reasoning' | 'file_edit' | 'log' | 'thought' | 'user_input' | 'approval';
type AgentState = 'thinking' | 'acting' | 'paused' | 'idle' | 'pausing';
type SubView = 'stream' | 'benchmarks';

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

  return <DashboardController onLogout={() => setView('landing')} />;
};

const DashboardController: React.FC<{ onLogout: () => void }> = ({ onLogout }) => {
  const [subView, setSubView] = useState<SubView>('stream');

  return (
    <div className="dashboard-container">
      <header className="nova-header">
        <div className="header-left">
          <div className="logo" onClick={onLogout} style={{ cursor: 'pointer' }}>
            <Square className="logo-icon" />
            <span className="logo-text">NOVA</span>
          </div>
          <nav className="header-nav">
            <button 
              className={`nav-item ${subView === 'stream' ? 'active' : ''}`} 
              onClick={() => setSubView('stream')}
            >
              <ActivityIcon size={18} />
              <span>LIVE STREAM</span>
            </button>
            <button 
              className={`nav-item ${subView === 'benchmarks' ? 'active' : ''}`} 
              onClick={() => setSubView('benchmarks')}
            >
              <BarChart3 size={18} />
              <span>BENCHMARKS</span>
            </button>
          </nav>
        </div>
        
        <div className="header-right">
          <div className="agent-info">
            <span className="agent-name">Gemma4-Super</span>
            <span className="status-pill acting">ONLINE</span>
          </div>
        </div>
      </header>

      {subView === 'stream' ? <CodeStreamView /> : <BenchmarkView />}
    </div>
  );
};

const CodeStreamView: React.FC = () => {
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
    <>
      <div className="stream-controls-bar">
        <div className="control-group">
          <label className="toggle-label">
            <input 
              type="checkbox" 
              checked={stepThrough} 
              onChange={(e) => setStepThrough(e.target.checked)} 
            />
            <span className="toggle-text">STEP-THROUGH MODE</span>
          </label>
        </div>
        
        <button 
          className={`control-btn pause-btn ${agentState === 'paused' ? 'resume' : ''} ${agentState === 'pausing' ? 'waiting' : ''}`} 
          onClick={togglePause}
          disabled={agentState === 'pausing'}
        >
          {agentState === 'paused' ? <Play size={16} /> : (agentState === 'pausing' ? <div className="spinner" /> : <Pause size={16} />)}
          <span>
            {agentState === 'paused' ? 'RESUME AGENT' : (agentState === 'pausing' ? 'WAITING...' : 'PAUSE EXECUTION')}
          </span>
        </button>
      </div>

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
    </>
  );
};

const BenchmarkView: React.FC = () => {
  const { summary, evaluations } = benchmarkData;

  return (
    <main className="benchmark-container">
      <section className="benchmark-header">
        <h2>Performance Benchmarks</h2>
        <p>Comprehensive evaluation of Gemma4-Super across multiple coding and architectural dimensions.</p>
      </section>

      <div className="stats-grid">
        {Object.entries(summary.average_scores).map(([key, value]) => {
          if (key === 'total_weighted') return null;
          return (
            <div key={key} className="stat-card">
              <span className="stat-label">{key.replace('_', ' ').toUpperCase()}</span>
              <div className="stat-value-container">
                <span className="stat-value">{value.toFixed(1)}</span>
                <span className="stat-max">/ 5.0</span>
              </div>
              <div className="progress-bar-bg">
                <div className="progress-bar-fill" style={{ width: `${(value / 5) * 100}%` }} />
              </div>
            </div>
          );
        })}
        <div className="stat-card total-weighted">
          <span className="stat-label">TOTAL WEIGHTED</span>
          <div className="stat-value-container">
            <span className="stat-value">{summary.average_scores.total_weighted.toFixed(1)}</span>
            <span className="stat-max">/ 5.0</span>
          </div>
          <div className="progress-bar-bg">
            <div className="progress-bar-fill gold" style={{ width: `${(summary.average_scores.total_weighted / 5) * 100}%` }} />
          </div>
        </div>
      </div>

      <section className="evaluations-list">
        <h3>Individual Test Cases</h3>
        {evaluations.map((evaluation, idx) => (
          <EvaluationCard key={idx} evaluation={evaluation} />
        ))}
      </section>
    </main>
  );
};

const EvaluationCard: React.FC<{ evaluation: Evaluation }> = ({ evaluation }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="eval-card">
      <div className="eval-card-summary" onClick={() => setIsExpanded(!isExpanded)}>
        <div className="eval-info">
          <span className="eval-topic">{evaluation.topic}</span>
          <div className="eval-metrics">
            <span>{evaluation.tokens} tokens</span>
            <span>{evaluation.tps.toFixed(1)} t/s</span>
            <span>{evaluation.duration.toFixed(2)}s</span>
          </div>
        </div>
        <div className="eval-score-pill">
          SCORE: {evaluation.weighted_score.toFixed(1)}
          <ChevronRight size={16} className={`arrow ${isExpanded ? 'expanded' : ''}`} />
        </div>
      </div>
      
      {isExpanded && (
        <div className="eval-card-details">
          <div className="detail-section">
            <h4><MessageSquare size={14} /> PROMPT</h4>
            <div className="code-block">{evaluation.prompt}</div>
          </div>
          <div className="detail-section">
            <h4><Brain size={14} /> AGENT RESPONSE</h4>
            <pre className="code-block response">{evaluation.response}</pre>
          </div>
          <div className="detail-section">
            <h4><Info size={14} /> EVALUATION JUSTIFICATION</h4>
            <p className="justification-text">{evaluation.evaluation.justification}</p>
            <div className="detailed-scores">
              {Object.entries(evaluation.evaluation.scores).map(([key, value]) => (
                <div key={key} className="score-item">
                  <span>{key.replace('_', ' ').toUpperCase()}</span>
                  <div className="score-dots">
                    {[1, 2, 3, 4, 5].map(d => (
                      <div key={d} className={`dot ${d <= value ? 'filled' : ''}`} />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
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
