import React, { useState } from 'react';
import { useNavigate, useLocation, StaticRouter} from 'react-router-dom';
import axois from 'axios';
import qs from 'qs';

function LandingPage() {

    const navigate = useNavigate();

    return (
        <>
        <div className="navbar">
            <h1 className="header-title" onClick={() => navigate('/')}>scioly.pro</h1>
            <p onClick={() => navigate('/menu')} className="header-text">generate test</p>
            <p onClick={() => navigate('/menu')} className="header-text">practice questions</p>
            <p className="header-text">sign up</p>
        </div>
        <div className="main">
            <div className="title-con">
                <h1 className="title">Training future scientists like <i>you</i></h1>
                <h1 className="title">to <span style={{'color': '#42C8F9'}}>triumph</span> in</h1>
                <h1 className="title">Science Olympiad competitions</h1>
                <p className="subtext">
                scioly.pro generates <b>comprehensive</b> practice tests & questions to give you that 
                <i> extra competitive edge.</i></p>
                <div className="button-con">
                    <button className="btn-primary"
                    onClick={() => navigate('/menu')}
                    >generate a test</button>
                    <button className="btn-secondary"
                    onClick={() => navigate('/menu')}
                    >individual practice questions</button>
                </div>
            </div>
        </div>
        </>
    )
}

export default LandingPage;
