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

  const fetchRangeData = async (startDate, endDate) => {
    const url = 'http://127.0.0.1:8000';
    const api = '/form';
    const target_api = url + api;
    const method = 'POST';

    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
      "startDate": `${startDate}`,
      "endDate": `${endDate}`
    });

    var requestOptions = {
      method: method,
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };

    try {
      const response = await fetch(target_api, requestOptions);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch data');
      }
      const data = await response.json();
      setWords(data);
      setLoading(false);
      setCurrentWordIndex(0);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleNextWord = useCallback(() => {
    if (currentWordIndex < words.length - 1) {
      setCurrentWordIndex(currentWordIndex + 1);
    } else {
      setCurrentWordIndex(0);
    }
  }, [currentWordIndex, words.length]);

  const handlePrevWord = useCallback(() => {
    if (currentWordIndex > 0) {
      setCurrentWordIndex(currentWordIndex - 1);
    } else {
      setCurrentWordIndex(words.length - 1);
    }
  }, [currentWordIndex]);

  function formatDate(date) {
    if (!date) return "";
    const localDate = new Date(date.getTime() - date.getTimezoneOffset() * 60000); // 修正时区
    const [year, month, day] = localDate.toISOString().split("T")[0].split("-");
    return `${year.slice(2)}-${month}-${day}`;
  }

  const handleDateChange = (start, end) => {
    fetchRangeData(formatDate(start), formatDate(end));
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
