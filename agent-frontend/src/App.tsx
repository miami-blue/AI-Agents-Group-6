import { DataProvider } from './api/DataContext';
import './App.css';
import Chat from './components/chat/Chat';
import Dashboard from './components/dashboard/Dashboard';
import Summary from './components/summary/Summary';

const App = () => {
  return (
    <>
      <DataProvider>
        <div className="app-container">
          <div className="app-content">
            <h1>Welcome back Bob! </h1>
            <Dashboard />
            <Chat />

            <Summary />
          </div>
        </div>
      </DataProvider>
    </>
  );
};

export default App;
