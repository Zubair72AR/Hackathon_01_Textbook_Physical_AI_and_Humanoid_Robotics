import React from 'react';
import Chatbot from '../Chatbot';

export default function DocPageLayout({children}) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <main style={{ flex: 1 }}>
        {children}
      </main>
      <div style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        width: '400px',
        height: '500px',
        zIndex: 1000
      }}>
        <Chatbot />
      </div>
    </div>
  );
}