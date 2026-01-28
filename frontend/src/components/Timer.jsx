/**
 * Timer Component
 * 
 * 30-minute countdown timer for the challenge
 */
import { useState, useEffect } from 'react';

const Timer = ({ onTimeUp }) => {
  const [timeLeft, setTimeLeft] = useState(30 * 60); // 30 minutes in seconds
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (!isRunning) return;

    const interval = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          setIsRunning(false);
          if (onTimeUp) onTimeUp();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [isRunning, onTimeUp]);

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStart = () => setIsRunning(true);
  const handlePause = () => setIsRunning(false);
  const handleReset = () => {
    setIsRunning(false);
    setTimeLeft(30 * 60);
  };

  const getTimerColor = () => {
    if (timeLeft < 60) return '#ff4444'; // Red for last minute
    if (timeLeft < 5 * 60) return '#ff9944'; // Orange for last 5 minutes
    return '#44ff44'; // Green otherwise
  };

  return (
    <div style={styles.container}>
      <div style={{ ...styles.display, color: getTimerColor() }}>
        {formatTime(timeLeft)}
      </div>
      <div style={styles.controls}>
        {!isRunning ? (
          <button onClick={handleStart} style={styles.button}>
            Start
          </button>
        ) : (
          <button onClick={handlePause} style={styles.button}>
            Pause
          </button>
        )}
        <button onClick={handleReset} style={styles.button}>
          Reset
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '20px',
    border: '2px solid #333',
    borderRadius: '10px',
    textAlign: 'center',
    backgroundColor: '#1a1a1a',
    maxWidth: '300px',
    margin: '0 auto',
  },
  display: {
    fontSize: '48px',
    fontWeight: 'bold',
    fontFamily: 'monospace',
    marginBottom: '15px',
  },
  controls: {
    display: 'flex',
    gap: '10px',
    justifyContent: 'center',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    cursor: 'pointer',
    border: 'none',
    borderRadius: '5px',
    backgroundColor: '#4CAF50',
    color: 'white',
    transition: 'background-color 0.3s',
  },
};

export default Timer;
