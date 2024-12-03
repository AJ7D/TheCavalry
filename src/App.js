import React, { useState, useEffect }from 'react';
import axios from 'axios';
import CustomButton from './CustomButton';

function App() {
    const [message, setMessage] = useState('');
    const [postResponse, setPostResponse] = useState('');

    const [buttonData, setButtonData] = useState([]);

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


    const handleClick = (subject) => {
        alert(`You clicked on ${subject}`);
    };

    //HOMEPAGE IMPL.
    return (
      <div>
        <img src="http://127.0.0.1:5000/static/images/dollars.png" alt="dollars" style={{ width: '100px', height: 'auto' }} />
        <img src="http://127.0.0.1:5000/static/images/piggybank.png" alt="piggybank" style={{ width: '100px', height: 'auto' }} />
        <p>Welcome to your Smart Saver Journey!</p>
        <br/><div className="custom-button">Let's Go!</div>

        
        <p>MY REWARDS</p>
        <div className="button-container">
            {buttonData.map((data, index) => (
                <button key={index} className="custom-button">
                    <img className="custom-image" src={`http://127.0.0.1:5000${data.imageSrc}`} alt={data.subject} />
                    <div className="button-label">{data.subject}</div>
                </button>
            ))}
        </div>

        <p>MY JOURNEY</p>
        </div>
    );
}

export default App;
