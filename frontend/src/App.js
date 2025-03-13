import React, { useState, useEffect, useCallback } from 'react';
import Card from './components/Card';
import './App.css';
import './index.css';
import DateRangePicker from './components/DatePicker';

const App = () => {
  const [words, setWords] = useState([]);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  let startDateStr = '1999-12-10';

  const fetchData = async () => {
    console.log("fetch ", startDateStr);
    console.log(`http://127.0.0.1:8000/collections/${startDateStr}`);
    try {
      const response = await fetch(`http://127.0.0.1:8000/collections/${startDateStr}`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch data');
      }
      const data = await response.json();
      setWords(data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleNextWord = useCallback(() => {
    if (currentWordIndex < words.length - 1) {
      setCurrentWordIndex(currentWordIndex + 1);
    }
  }, [currentWordIndex, words.length]);

  const handlePrevWord = useCallback(() => {
    if (currentWordIndex > 0) {
      setCurrentWordIndex(currentWordIndex - 1);
    }
  }, [currentWordIndex]);

  function formatDate(date) {
    if (!date) return "";
    const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000); // 修正时区
    const [year, month, day] = localDate.toISOString().split("T")[0].split("-");
    return `${year.slice(2)}-${month}-${day}`;
  }

  const handleDateChange = (start, end) => {
    console.log(start);
    startDateStr = formatDate(start);
    fetchData();
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
      <DateRangePicker onDateChange={handleDateChange} />
      <Card wordData={words[currentWordIndex]} currIdx={currentWordIndex + 1} totalNum={words.length} />
    </div>
  );
};

export default App;
