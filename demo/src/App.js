import React, { useState } from 'react';
import { Box, Input, Button, theme, ThemeProvider, CSSReset } from '@chakra-ui/core';
import logo from './rocIcon.svg';
import './App.css';

function App() {
  const [data, setData] = useState('');
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [error, setError] = useState('');

  const fetchData = async url => {
    setError('');
    setIsError(false);
    setIsLoading(true);
    try {
      const result = await fetch(url)
        .then(res => res.json())
        .then(data => data);
      setData(result.prediction);
    } catch (error) {
      setError(error);
      setIsError(true);
    }
    setIsLoading(false);
  };

  return (
    <ThemeProvider theme={theme}>
      <CSSReset/>
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <Box d="flex" w="50%">
            <Input
              variant="flushed"
              placeholder="請輸入一句話"
              value={query}
              onChange={event => setQuery(event.target.value)}
              isDisabled={isLoading}
            />
            <Button
              ml="4"
              variantColor="blue"
              isDisabled={isLoading}
              onClick={() =>
                fetchData(`/predict?line=${query}`)
              }
            >
              送出
            </Button>
          </Box>
          { isLoading && <p>資料轉換中，請稍候(大概兩分鐘)...</p>}
          { isError && <p>{`${error}`}</p>}
          { data && <p>{`結果：${data}`}</p>}
        </header>
      </div>
    </ThemeProvider>
  );
}

export default App;
