import React, { useState, useEffect, useCallback } from 'react';
import './Content.css';
import Card from './Card/Card.js';
import debounce from 'lodash.debounce';
import DateRangePicker from './DatePicker.js';

const Content = () => {
  const [words, setWords] = useState([]);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [loading, setLoading] = useState(false); // 初始设为true
  const [error, setError] = useState(null);

  // 获取最近7天的数据作为初始数据
  const getDefaultDateRange = () => {
    const end = new Date();
    const start = new Date();
    start.setDate(end.getDate() - 7);
    return { start, end };
  };

  // 缓存键生成函数
  const getCacheKey = (startDate, endDate) => `vocab_data_${startDate}_${endDate}`;

  // 检查缓存是否有效（1小时有效期）
  const isCacheValid = (cachedData) => {
    return cachedData &&
      Date.now() - cachedData.timestamp < 3600000; // 1小时
  };

  const fetchRangeData = async (startDate, endDate) => {
    // 先尝试从缓存读取
    const cacheKey = getCacheKey(startDate, endDate);
    const cachedData = JSON.parse(localStorage.getItem(cacheKey));
    if (isCacheValid(cachedData)) {
      setWords(cachedData.data);
      setLoading(false);
      return;
    }
    const url = 'http://127.0.0.1:8000';
    const api = '/form';
    const targetApi = url + api;
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
      redirect: 'follow',
      mode: 'cors',
    };

    try {
      const response = await fetch(targetApi, requestOptions);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to fetch data');
      }
      const data = await response.json();
      setWords(data);
      setLoading(false);
      setCurrentWordIndex(0);

      // 保存到缓存
      localStorage.setItem(cacheKey, JSON.stringify({
        data,
        timestamp: Date.now()
      }));
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

  const handleDateChange = useCallback(
    debounce((start, end) => {
      fetchRangeData(formatDate(start), formatDate(end));
    }, 500),
    []
  );

  // 添加初始数据加载
  useEffect(() => {
    const { start, end } = getDefaultDateRange();
    fetchRangeData(formatDate(start), formatDate(end));
  }, []);

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

  return (
    loading ? (
      <div className="content">
        <div className="skeleton-loader">加载数据中...</div>
      </div>
    ) : (error ? (
      <div className="content">错误: {error}</div>
    ) : (
      <div className="content">
        <DateRangePicker onDateChange={handleDateChange} />
        <Card wordData={words[currentWordIndex]} currIdx={currentWordIndex + 1} totalNum={words.length} />
      </div>
    ))
  );
};

export default Content;
