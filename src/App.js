import React, { useState, useEffect }from 'react';
import axios from 'axios';
import CustomButton from './CustomButton';
import './Banner.css';
import StreakDisplay from './StreakDisplay';
import ProgressBar from './ProgressBar';

function App() {
    const [message, setMessage] = useState('');
    const [postResponse, setPostResponse] = useState('');

    const [currentValue, setCurrentValue] = useState(50); // Example current value
    const goalValue = 100; // Example goal value

    const [buttonData, setButtonData] = useState([]);

    const [splashScreenSeen, setSplashScreenSeen] = useState(false); // Example current value
    const [hasSelectedPlan, setHasSelectedPlan] = useState(false); // Example current value

    // BUTTONS IMPL.
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/buttons');
                setButtonData(response.data);
            } catch (error) {
                console.error("Error fetching button data:", error);
            }
        };

        fetchData();
    }, []);

      if (!splashScreenSeen) {
          return (
            <div align="center">
            <img src="http://127.0.0.1:5000/static/images/dollars.png" alt="dollars" style={{ width: '100px', height: 'auto' }} />
            <img src="http://127.0.0.1:5000/static/images/piggybank.png" alt="piggybank" style={{ width: '100px', height: 'auto' }} />
            <p align="center">Welcome to your<br/><b>Smart Saver Journey!</b></p>
            <div className="custom-button" onClick={() => setSplashScreenSeen(true)}>Let's Go!</div>

            </div>
          )
      }
      else if (!hasSelectedPlan) {
        setHasSelectedPlan(true);
      }
      else {
        return (
          <div>
            <div class="banner">
            <div className="balance-indicator">
            <p className="aligned-text">
              <span className="left">MY SMART SAVER</span>
              <span className="right">200</span>
            </p>
              <img src="http://127.0.0.1:5000/static/images/points.png" alt="Points Icon" />
            </div>
          </div>

          <p>We're here to help you make the most from your money and earn rewards along the way!</p>
          <p>Tell me what I can help you with:</p>

          <div class="custom-checkbox-container">
            <input type="checkbox" id="customCheckbox" class="custom-checkbox" />
            <label htmlFor="customCheckbox">House Deposit</label>
          </div>

          <div class="custom-checkbox-container">
            <input type="checkbox" id="customCheckbox" class="custom-checkbox" />
            <label htmlFor="customCheckbox">Holiday/Travel</label>
          </div>

          <div class="custom-checkbox-container">
            <input type="checkbox" id="customCheckbox" class="custom-checkbox" />
            <label htmlFor="customCheckbox">Rainy Day Fund</label>
          </div>

          <div class="custom-checkbox-container">
            <input type="checkbox" id="customCheckbox" class="custom-checkbox" />
            <label htmlFor="customCheckbox">Other</label>
          </div>



          <div className="streak-display">
              <span>4 WEEK STREAK</span>
              <img src="http://127.0.0.1:5000/static/images/flame.png" alt="Flame Icon" />
          </div>
          
          <div className="custom-button">
            GOAL:
            <img src="http://127.0.0.1:5000/static/images/house.png" alt="Goal" />
          </div>
          <div className="custom-button">
            SAVED:
            <ProgressBar currentValue={currentValue} goalValue={goalValue} />
          </div>


          <div class="banner">
            <p>MY REWARDS</p>
          </div>
          <div className="button-container">
              {buttonData.map((data, index) => (
                  <button key={index} className="custom-button">
                      <img className="custom-image" src={`http://127.0.0.1:5000${data.imageSrc}`} alt={data.subject} />
                      <div className="button-label">{data.subject}</div>
                      <div className="balance-indicator">
                        <span>{data.cost}</span>
                        <img src="http://127.0.0.1:5000/static/images/points.png" alt="Points Icon" />
                      </div>
                  </button>
              ))}
          </div>

          <div class="banner">
              <p>MY JOURNEY</p>
          </div>
        </div>
    );
  }
}

export default App;
