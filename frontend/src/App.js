import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import Popup from './Popup';

function App() {
  const [jobTitle, setJobTitle] = useState('Senior Software Engineer');
  const [location, setLocation] = useState('Seattle, WA');
  //const [postDate, setPostDate] = useState('');
  //const [applyLink, setApplyLink] = useState('');
  const [jobItems, setJobItems] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [serverLogs, setServerLogs] = useState([]);
  const [activeTab, setActiveTab] = useState('');

  const [showModal, setShowModal] = useState(false);
  const [modalMessage, setModalMessage] = useState('');

  const handleJobTitleChange = (e) => {
    setJobTitle(e.target.value);
  }

  const handleLocationChange = (e) => {
    setLocation(e.target.value);
  }

  const handleSearchClick = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/searchjobs`, {
        jobTitle,
        location
      });
      //setMessage(`Response: Status=${response.status}, Message="${response.data}"`);
      //setShowMessage(true);
      setShowModal(true);
      setModalMessage(`Response: Status=${response.status}, Message="${response.data}"`);
    } catch (error) {
      //setMessage(error.response.data.message);
      //setShowMessage(true);
      setShowModal(true);
      setModalMessage(`Response: Status=${error.response.status}, Message="${error.response.data.message}"`);
    }
  }

  const handleDismissModal = () => {
    setShowModal(false);
    setModalMessage('');
  };

  const handleTabClick = async (tabName) => {
    setActiveTab(tabName);
    if (tabName === 'Search Results') {
      try {
        const response = await axios.get(`http://localhost:8000/getjobs?location=${location}`);
        // handle response and display job items
        setJobItems(response.data);
      } catch (error) {
        setShowModal(true);
        setModalMessage(error.response.data.message);
      }
    } else if (tabName === 'Server Logs') {
      try {
        const response = await axios.get(`http://localhost:8000/getlogs?location=${location}`);
        // handle response and display logs
        setServerLogs(response.data);
      } catch (error) {
        setShowModal(true);
        setModalMessage(error.response.data.message);
      }
    }
  }

  const handleJobItemClick = (item) => {
    // display jobDescription
    setSelectedItem(item);
  }

  return (
    <div className="App">

      { /* Top Pane */}
      <div className="top-pane">
        <div className='text-input-div'>
          <label><b>Job Title:</b></label>&nbsp;&nbsp;
          <input className='text-input-field' type="text" value={jobTitle} onChange={handleJobTitleChange} placeholder="JobTitle" />
        </div>
        <div className='text-input-div'>
        <label><b>Location:</b></label>&nbsp;&nbsp;
          <input className='text-input-field' type="text" value={location} onChange={handleLocationChange} placeholder="Location" />
        </div>
        <div className='button-div'>
          <button className='button-style' onClick={handleSearchClick}>Search</button>
        </div>

        <div className='tab-button-div'>
          {/*<div style={{ position: 'absolute', bottom: 0, left: 0, right: 0 }}>*/}
          <button className='button-style' onClick={() => handleTabClick('Search Results')}>
            Search Results
          </button>
          &nbsp;&nbsp;
          <button className='button-style' onClick={() => handleTabClick('Server Logs')}>
            Server Logs
          </button>
        </div>
      </div>

      { /* Bottom Pane */}
      <div className='bottom-pane'>
        <div style={{ display: activeTab === 'Search Results' ? 'flex' : 'none' }}>
          <div className='bottom-left-subpane'>
            {/* display jobTitle and companyName */}
            <ol>
              {jobItems.map(job => (
                <li key={job.jobId} style={{ margin: '5px 0' }}>
                  <a href="#" onClick={e => {
                        e.preventDefault();
                        handleJobItemClick(job);
                    }}
                  >
                    {`${job.jobTitle}`}
                  </a>
                  <br/>
                  {`${job.companyName}`}
                  <br/>
                  {`Posted on: ${job.postDate}`}
                </li>
              ))}
            </ol>
          </div>
          <div className='bottom-right-subpane'>
            {/* display jobDescription */}
            {selectedItem && (
              <div className='job-description-div'>
                <a href={selectedItem.applyLink} target='_blank'>
                  <h3>{`${selectedItem.jobTitle}, ${selectedItem.companyName}`}
                  &nbsp;&nbsp;(Click to Apply)</h3>
                </a>
                <div dangerouslySetInnerHTML={{ __html: selectedItem.jobDescription }} />
              </div>
            )}
          </div>
        </div>
        <div style={{ display: activeTab === 'Server Logs' ? 'flex' : 'none' }}>
          <div className='server-logs-div'>
            {serverLogs.map((log, index) => (
              <div key={index}>{log}</div>
            ))}
          </div>
        </div>
      </div>

      {/* ... */}
      {/*<div className="modal-popup" onClick={handleDismissModal}>
          <div onClick={(event) => event.stopPropagation()}>
            <p>{modalMessage}</p>
            <button onClick={handleDismissModal}>OK</button>
          </div>
      </div>*/}
      {showModal && (
        <Popup message={modalMessage} handleClose={handleDismissModal} />
      )}
    </div>
  );
}

export default App;
