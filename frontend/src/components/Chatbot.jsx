import React, { useState, useEffect, useRef } from 'react';
import clsx from 'clsx';
import styles from './Chatbot.module.css';

function Chatbot() {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your AI assistant for the Unified AI/Spec-Driven Book. How can I help you with the content?", sender: 'bot' }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // In a real implementation, this would call the backend API
      // For now, we'll simulate a response
      setTimeout(async () => {
        try {
          // This is a placeholder - in real implementation, call your backend API
          const response = await fetch('/api/v1/query', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              query: inputText,
              session_id: '123e4567-e89b-12d3-a456-426614174000' // Placeholder session ID
            })
          });

          const data = await response.json();

          const botMessage = {
            id: Date.now() + 1,
            text: data.response || "This is a simulated response. In the full implementation, this would be a response from the RAG system based on the book content.",
            sender: 'bot',
            sources: data.sources || []
          };

          setMessages(prev => [...prev, botMessage]);
        } catch (error) {
          console.error('Error getting response:', error);
          const errorMessage = {
            id: Date.now() + 1,
            text: "Sorry, I encountered an error processing your request. Please try again.",
            sender: 'bot'
          };
          setMessages(prev => [...prev, errorMessage]);
        } finally {
          setIsLoading(false);
        }
      }, 1000); // Simulate network delay
    } catch (error) {
      console.error('Error sending message:', error);
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      <div className={styles.chatHeader}>
        <h3>AI Assistant</h3>
        <p>Ask questions about the book content</p>
      </div>

      <div className={styles.chatMessages}>
        {messages.map((message) => (
          <div
            key={message.id}
            className={clsx(
              styles.message,
              styles[message.sender]
            )}
          >
            <div className={styles.messageText}>{message.text}</div>
            {message.sources && message.sources.length > 0 && (
              <div className={styles.sources}>
                <strong>Sources:</strong>
                <ul>
                  {message.sources.map((source, idx) => (
                    <li key={idx}>{source.title || 'Source'}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className={clsx(styles.message, styles.bot)}>
            <div className={styles.typingIndicator}>
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className={styles.chatInputForm}>
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Ask a question about the book content..."
          className={styles.chatInput}
          disabled={isLoading}
        />
        <button
          type="submit"
          className={styles.sendButton}
          disabled={isLoading || !inputText.trim()}
        >
          Send
        </button>
      </form>
    </div>
  );
}

export default Chatbot;