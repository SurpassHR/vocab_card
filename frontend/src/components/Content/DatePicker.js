import React, { useState } from "react";
import "react-datepicker/dist/react-datepicker.css";
import DatePicker from "react-datepicker";

function DateRangePicker({ onDateChange }) {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const handleChange = (dates) => {
    const [start, end] = dates;

    // 检查两个日期是否都已选择
    if (start && end) {
      // 检查日期是否发生了变化
      if (start.getTime() !== (startDate ? startDate.getTime() : null) ||
        end.getTime() !== (endDate ? endDate.getTime() : null)) {
        setStartDate(start);
        setEndDate(end);
        if (onDateChange) {
          onDateChange(start, end);
        }
      }
    } else {
      // 如果其中一个日期被清除，也更新状态
      setStartDate(start);
      setEndDate(end);
    }
  };

  return (
    <DatePicker
      selectsRange={true}
      startDate={startDate}
      endDate={endDate}
      onChange={handleChange}
    />
  );
}

export default DateRangePicker;