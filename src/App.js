import React, { useState, useEffect }from 'react';
import axios from 'axios';
import CustomButton from './CustomButton';
import './Banner.css';
import StreakDisplay from './StreakDisplay';
import ProgressBar from './ProgressBar';
import Modal from './Modal';

function App() {
    const [message, setMessage] = useState('');
    const [postResponse, setPostResponse] = useState('');

    const [currentValue, setCurrentValue] = useState(50); 
    const [goalValue, setGoalValue] = useState(100); 
    const [userPoints, setUserPoints] = useState(200); 

    const [buttonData, setButtonData] = useState([]);

    const [planData, setPlanData] = useState([]);

    const [splashScreenSeen, setSplashScreenSeen] = useState(false); 
    const [hasSelectedPlan, setHasSelectedPlan] = useState(true);

    const [isModalOpen, setIsModalOpen] = useState(false);

    const [isLocked, setIsLocked] = useState(false);

    const toggleLock = () => {
        setIsLocked((prevState) => !prevState);
    };

    const updateUserScore = (minusPoints) => {
      if (userPoints - minusPoints < 0) {
        return;
      }
      setUserPoints(prevPoints => prevPoints - minusPoints); 
      setIsModalOpen(true);
    };

    // BUTTONS IMPL.
    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/buttons');
                setButtonData(response.data);
            } catch (error) {
                console.error("Error fetching button data:", error);
            }

            try {
              const plan_response = await axios.get('http://127.0.0.1:5000/static/plandata');
              const data = plan_response.data;
              // Use the response data directly
              setCurrentValue(data[0].plans[0].locked);
              setGoalValue(data[0].plans[0].target_amount);

              setPlanData(plan_response.data);
              setCurrentValue(planData[0].plans[0].locked)
              setGoalValue(planData[0].plans[0].target_amount)
            } catch (error) {
              console.error("Error fetching plan data.");
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
        return (
          <div>
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
          </div>
        )
      }
      else {
        return (
          <div>
            <div class="banner">
            <div className="balance-indicator">
            <p className="aligned-text">
              <span className="left">MY SMART SAVER</span>
              <span className="right">{userPoints}</span>
            </p>
              <img src="http://127.0.0.1:5000/static/images/points.png" alt="Points Icon" />
            </div>
          </div>


          <div className="streak-display">
              <span>4 WEEK STREAK</span>
              <img src="http://127.0.0.1:5000/static/images/flame.png" alt="Flame Icon" />
          </div>
          
          <div align="center">

          <div className="button-container">
          <div className="custom-button">
            GOAL:
            <div>
              {planData ? (
                  <img src={planData[0].plans[0].image} alt="Goal" />
              ) : (
                  <p>Loading...</p>
              )}
            </div>
          </div>

          <div className="custom-button"
                onClick={toggleLock}
                style={{ position: "relative", cursor: "pointer" }}
            >
                SAVED:
                <ProgressBar currentValue={currentValue} goalValue={goalValue} />
                {isLocked && (
                    <img
                        src="http://127.0.0.1:5000/static/images/lockpad.png" 
                        alt="Lock Overlay" 
                        style={{
                            position: "absolute",
                            top: 0,
                            left: 0,
                            width: "100%",
                            height: "100%",
                            backgroundColor: "rgba(255, 255, 255, 0.5)", // Semi-transparent effect
                            objectFit: "contain",
                            zIndex: 1,
                        }}
                    />
                )}
            </div>
          </div>
          </div>


          <div class="banner">
            <p>MY REWARDS</p>
          </div>
          <div className="button-container">
              {buttonData.map((data, index) => (
                  <button key={index} className="custom-button" onClick={() => {updateUserScore(data.cost);}}>
                    <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
                        <h2>Congratulations!</h2>
                        <img src="http://127.0.0.1:5000/static/images/partypopper.gif"/>
                        <p>You've earned it.</p>
                        <button onClick={() => setIsModalOpen(false)}>Close</button>
                    </Modal>
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
