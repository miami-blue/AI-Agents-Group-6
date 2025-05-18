import './App.css';
import Chat from './components/chat/Chat';
import Dashboard from './components/dashboard/Dashboard';

const App = () => {
  return (
    <>
      <div className="app-container">
        <div className="app-content">
          <h1>Hello, I&apos;m Budgy!</h1>
          <Dashboard />
          <Chat />
        </div>
      </div>
    </>
  );
};

export default App;
