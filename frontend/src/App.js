import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// You might want to store this securely or get it from user input
const AUTH_TOKEN = "secret-token-1";

function App() {
  const [analysisData, setAnalysisData] = useState('');
  const [analysisResult, setAnalysisResult] = useState('');
  const [recommendationData, setRecommendationData] = useState('');
  const [recommendationResult, setRecommendationResult] = useState('');
  const [sentimentText, setSentimentText] = useState('');
  const [sentimentResult, setSentimentResult] = useState('');
  const [contentTopic, setContentTopic] = useState('');
  const [contentType, setContentType] = useState('');
  const [generatedContent, setGeneratedContent] = useState('');

  const apiClient = axios.create({
    baseURL: '/api',
    headers: {
      'Authorization': `Bearer ${AUTH_TOKEN}`,
      'Content-Type': 'application/json',
    }
  });

  const analyzeData = async () => {
    try {
      const response = await apiClient.post('/analyze', { data: analysisData });
      setAnalysisResult(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error('Error analyzing data:', error);
      setAnalysisResult('Error analyzing data');
    }
  };

  const getRecommendation = async () => {
    try {
      const response = await apiClient.post('/recommend', { user: recommendationData });
      setRecommendationResult(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error('Error getting recommendation:', error);
      setRecommendationResult('Error getting recommendation');
    }
  };

  const analyzeSentiment = async () => {
    try {
      const response = await apiClient.post('/sentiment', { text: sentimentText });
      setSentimentResult(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error('Error analyzing sentiment:', error);
      setSentimentResult('Error analyzing sentiment');
    }
  };

  const generateContent = async () => {
    try {
      const response = await apiClient.post('/generate-content', { topic: contentTopic, content_type: contentType });
      setGeneratedContent(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error('Error generating content:', error);
      setGeneratedContent('Error generating content');
    }
  };



  return (
    <div className="App">
      <h1>AI Web App</h1>
      
      <div className="section">
        <h2>Data Analysis</h2>
        <textarea
          value={analysisData}
          onChange={(e) => setAnalysisData(e.target.value)}
          placeholder="Enter data for analysis"
        />
        <button onClick={analyzeData}>Analyze</button>
        <pre>{analysisResult}</pre>
      </div>

      <div className="section">
        <h2>Get Recommendation</h2>
        <textarea
          value={recommendationData}
          onChange={(e) => setRecommendationData(e.target.value)}
          placeholder="Enter user data for recommendation"
        />
        <button onClick={getRecommendation}>Get Recommendation</button>
        <pre>{recommendationResult}</pre>
      </div>

      <div className="section">
        <h2>Sentiment Analysis</h2>
        <textarea
          value={sentimentText}
          onChange={(e) => setSentimentText(e.target.value)}
          placeholder="Enter text for sentiment analysis"
        />
        <button onClick={analyzeSentiment}>Analyze Sentiment</button>
        <pre>{sentimentResult}</pre>
      </div>

      <div className="section">
        <h2>Generate Content</h2>
        <input
          type="text"
          value={contentTopic}
          onChange={(e) => setContentTopic(e.target.value)}
          placeholder="Enter content topic"
        />
        <input
          type="text"
          value={contentType}
          onChange={(e) => setContentType(e.target.value)}
          placeholder="Enter content type"
        />
        <button onClick={generateContent}>Generate Content</button>
        <pre>{generatedContent}</pre>
      </div>
    </div>
  );
}

export default App;