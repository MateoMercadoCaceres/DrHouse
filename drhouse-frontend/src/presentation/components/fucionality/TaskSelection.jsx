import React, { useState } from 'react';
import DiagnosticChat from '../chats/DiagnosticChat';
import MedicationsChat from '../chats/MedicationsChat';
import ImageGenerationsChat from '../chats/ImageGenerationsChat';
import '../styles/ModelsPage.css';

const TaskSelection = () => {
  const [selectedTask, setSelectedTask] = useState(null);

  const tasks = [
    { id: 'models', name: 'Models' },
    { id: 'medications', name: 'Medications' },
    { id: 'diagnostic', name: 'Diagnostic' },
    { id: 'creator-image', name: 'Creator Image' }
  ];

  const renderSelectedChat = () => {
    switch (selectedTask) {
      case 'diagnostic':
        return <DiagnosticChat />;
      case 'medications':
        return <MedicationsChat />;
      case 'creator-image':
        return <ImageGenerationsChat />;
      default:
        return null;
    }
  };

  if (selectedTask) {
    return renderSelectedChat();
  }

  return (
    <div className="task-selection-container">
      <div className="background-grid">
        <div className="grid">
          {Array.from({ length: 144 }).map((_, index) => (
            <div key={index} className="grid-cell" />
          ))}
        </div>
      </div>
      <div className="task-options">
        {tasks.map((task) => (
          <div
            key={task.id}
            className="task-option"
            onClick={() => setSelectedTask(task.id)}
          >
            <h3>{task.name}</h3>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskSelection; 