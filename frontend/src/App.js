import React, { useState, useEffect } from 'react';
import Card from './components/Card';
import Navigation from './components/Navigation';
import './App.css';
import './index.css';

const App = () => {
  const [words, setWords] = useState([]);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const today = new Date();
    const year = String(today.getFullYear()).slice(-2); // Get last two digits of year
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const dateStr = `${year}-${month}-${day} 23:59:59`;

    const fetchData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/collections/${dateStr}`);
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to fetch data');
        }
        const data = await response.json();
        setWords(data); // No longer wrap in an array
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleNextWord = () => {
    if (currentWordIndex < words.length - 1) {
      setCurrentWordIndex(currentWordIndex + 1);
    }
  };

  const handlePrevWord = () => {
    if (currentWordIndex > 0) {
      setCurrentWordIndex(currentWordIndex - 1);
    }
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'ArrowRight') {
        handleNextWord();
      } else if (event.key === 'ArrowLeft') {
        handlePrevWord();
      }
    };

    window.addEventListener('keydown', handleKeyDown);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleNextWord, handlePrevWord]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="app">
      <Card wordData={words[currentWordIndex]} />
      <Navigation onClick={handlePrevWord} buttonText='<' />
      <Navigation onClick={handleNextWord} buttonText='>' />
    </div>
  );
};

export default App;
