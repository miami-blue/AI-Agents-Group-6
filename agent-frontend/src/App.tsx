import './App.css';
import budgy_icon from './assets/budgy_icon.svg';
import Chat from './components/chat/Chat';

const App = () => {
  return (
    <>
      <div className="app-root">
        <h1>Hello, I&apos;m Budgy!</h1>
        <img src={budgy_icon} alt="Budgy Icon"></img>

        <Chat />
      </div>
    </>
  );
};

export default App;
