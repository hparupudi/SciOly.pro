import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, StaticRouter} from 'react-router-dom';
import axois from 'axios';
import qs from 'qs';

function MenuPage() {
    const navigate = useNavigate();
    const options = ["All", "Codebusters", "Fermi Questions"];
    const [buttons, setButtons] = useState([false, true, true]);

    const questionBanks = {
      "aristocrat generator": "codebusters",
      "fermi generator": "fermi questions",
    }

    const paths = {
      "aristocrat generator": "/aristo",
      "fermi generator": "fermi"
    }

    const handleUpdate = async (index) => {
      let tempButtons = [...buttons];
      tempButtons[index] = !tempButtons[index]
      setButtons(tempButtons);
      console.log(buttons);
    }

    return (
        <>
          <div className="navbar">
            <h1 className="header-title" onClick={() => navigate('/')}>scioly.pro</h1>
            <p className="header-text">generate test</p>
            <p onClick={() => navigate('/code')}className="header-text">practice questions</p>
            <p className="header-text">sign up</p>
          </div>
          <div className="main">
            <div className="subcon">
              <div className="title-con">
                <h1 className="white-page-title">generate practice questions</h1>
                <p className="subtext">individually curated, developed, and tested.</p>
              </div>
              <div className="sidebar-con">
              <div className="event-container">
                  <div className="sidebar">
                    {options.map((option, index) => (
                      <button 
                      style={{'backgroundColor': buttons[index] ? '#111F3B' : 'aquamarine', 
                              'color': buttons[index] ? 'white' : 'black'}}
                      onClick={() => handleUpdate(index)} 
                      className="mp-button" 
                      key={index}>{option}</button>
                    ))}
                </div>
                  {Object.keys(questionBanks).map((key, index) => {
                    if (buttons[0] == false || buttons[index+1] == false) {
                      return (
                        <div className="event-card">
                          <h1 className="question-text">{key}</h1>
                          <h1 style={{'fontWeight': 400}}className="question-text">{questionBanks[key]}</h1>
                          <div className="event-sc2">
                            <button onClick={() => navigate(paths[key])} className="event-button">&rarr;</button>
                          </div>
                        </div>
                      )
                    }
                  })};
                </div>
              </div>
              <div className="coming-con">
                <h1 className="coming-title">More Events Coming Soon!</h1>
              </div>
            </div>
          </div>
        </>
    ) 
}

export default MenuPage;