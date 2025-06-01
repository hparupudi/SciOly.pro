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
                <h1 className="title">Helping future scientists like <i>you</i></h1>
                <h1 className="title"><span style={{'color': '#42C8F9'}}>triumph</span></h1>
                <h1 className="title">in Science Olympiad competitions</h1>
                <p className="subtext">
                scioly.pro generates <b>comprehensive</b> practice tests & questions to give you that 
                <i> extra competitive edge.</i></p>
                <div className="button-con">
                    <button className="lp-button"
                    onClick={() => navigate('/menu')}
                    >generate a test</button>
                    <button className="lp-button"
                    style={{"border-color": "blue"}}
                    onClick={() => navigate('/menu')}
                    >individual practice questions</button>
                </div>
            </div>
        </div>
        </>
    )
}

export default LandingPage;
