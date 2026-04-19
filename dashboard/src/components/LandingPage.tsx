import React from 'react';
import { Download, BookOpen, Cpu, Brain, Shield, ChevronRight } from 'lucide-react';
import './LandingPage.css';

interface LandingPageProps {
  onLaunch: () => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onLaunch }) => {
  return (
    <div className="landing-container">
      <nav className="landing-nav">
        <div className="logo">
          <div className="logo-icon-container">
            <Cpu className="logo-icon" />
          </div>
          <span className="logo-text">SUPER AGENTS</span>
        </div>
        <button className="launch-btn" onClick={onLaunch}>
          LAUNCH DASHBOARD <ChevronRight size={16} />
        </button>
      </nav>

      <section className="hero-section">
        <h1 className="hero-title">The Specialist is Here.</h1>
        <p className="hero-subtitle">
          Introducing the <strong>Super Coding Agent</strong>: A fine-tuned, local-first vertical that outperforms general models in complex software engineering.
        </p>
        <div className="hero-actions">
          <button className="primary-cta">
            <Download size={20} />
            <span>Download Super Coding Agent</span>
          </button>
          <button className="secondary-cta">
            <BookOpen size={20} />
            <span>View Documentation</span>
          </button>
        </div>
      </section>

      <section className="features-grid">
        <div className="feature-card">
          <div className="feature-icon-wrapper">
            <Cpu className="feature-icon" />
          </div>
          <h3>Specialized Vertical DNA</h3>
          <p>
            Built for the "hard stuff." Master of TypeScript Generics, Python Asyncio, Metaprogramming, and complex DevOps pipelines. It’s not just a model; it’s your most senior peer.
          </p>
        </div>
        <div className="feature-card">
          <div className="feature-icon-wrapper">
            <Brain className="feature-icon" />
          </div>
          <h3>Reasoned Implementations</h3>
          <p>
            Every response follows our signature <strong>Plan-Act-Rationale</strong> workflow. Understand the <em>why</em> behind the <em>what</em> with built-in Chain-of-Thought reasoning.
          </p>
        </div>
        <div className="feature-card">
          <div className="feature-icon-wrapper">
            <Shield className="feature-icon" />
          </div>
          <h3>Local-First, Zero Latency</h3>
          <p>
            Runs comfortably on an 8GB VRAM consumer GPU. Keep your code private, eliminate cloud costs, and enjoy the speed of local execution.
          </p>
        </div>
      </section>

      <section className="performance-section">
        <h2>Performance Targets</h2>
        <div className="table-container">
          <table className="performance-table">
            <thead>
              <tr>
                <th>Metric</th>
                <th>Super Coding Agent (4B)</th>
                <th>SOTA Benchmark Goal</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>HumanEval Pass@1</strong></td>
                <td className="highlight"><strong>&gt;85% (Target)</strong></td>
                <td>~80-85%</td>
              </tr>
              <tr>
                <td><strong>MBPP</strong></td>
                <td className="highlight"><strong>&gt;70% (Target)</strong></td>
                <td>~65-70%</td>
              </tr>
              <tr>
                <td><strong>Local Deployment</strong></td>
                <td className="highlight"><strong>Yes (8GB VRAM)</strong></td>
                <td>No</td>
              </tr>
              <tr>
                <td><strong>Reasoning Pattern</strong></td>
                <td className="highlight"><strong>Plan-Act-Rationale</strong></td>
                <td>Direct Completion</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section className="modern-engineer-features">
        <h2>Features for the Modern Engineer</h2>
        <ul className="engineer-features-list">
          <li>
            <strong>Context-Aware Tool Use:</strong> Ace at complex multi-file edits and tool-calling scenarios.
          </li>
          <li>
            <strong>Skill Management:</strong> Learn and persist specialized engineering skills across sessions.
          </li>
          <li>
            <strong>Memory Integration:</strong> Remembers your project’s architecture and constraints.
          </li>
          <li>
            <strong>Dashboard Ready:</strong> Seamlessly integrates with the Super Agents Dashboard for step-through agentic control.
          </li>
        </ul>
      </section>

      <footer className="landing-footer">
        <p>© 2026 Paperclip. The future of agentic orchestration.</p>
      </footer>
    </div>
  );
};

export default LandingPage;
