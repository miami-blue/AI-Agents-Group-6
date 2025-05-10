import budgy_icon from '../../assets/budgy_icon.svg';

const ChatFloatingButton = ({
  onClick,
  ...props
}: React.DetailedHTMLProps<
  React.ButtonHTMLAttributes<HTMLButtonElement>,
  HTMLButtonElement
>) => {
  return (
    <button className="chat-floating-button" onClick={onClick}>
      <img src={budgy_icon} alt="Budgy Icon"></img>
    </button>
  );
};

export default ChatFloatingButton;
