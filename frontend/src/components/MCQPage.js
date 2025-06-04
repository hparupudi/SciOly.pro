import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation, StaticRouter} from 'react-router-dom';
import axios from 'axios';
import qs from 'qs';

function MCQPage() {

    const navigate = useNavigate();
    const location = useLocation();
    const { state } = location;
    const effectRan = useRef(false)
    const [title, setTitle] = useState(state.title) 
    const [event, setEvent] = useState(state.event)
    const [description, setDescription] = useState(state.description)
    const [generate, setGenerate] = useState(false)
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [options, setOptions] = useState([]);
    const [newOptions, setNewOptions] = useState([]);
    const [newQuestion, setNewQuestion] = useState('')
    const [newAnswer, setNewAnswer] = useState('')
    const [saveQ, setSaveQ] = useState(true);
    const [updateQ, setUpdateQ] = useState(false);
    const [select, setSelect] = useState();
    const [isCorrect, setIsCorrect] = useState(null);
    const [check, setCheck] = useState(false);

    const option_letters = ['A', 'B', 'C', 'D'];

    useEffect(() => {
        async function fetchQuestion() {
        const eventObject = {'event': event}
        try {
            const result = await axios.post('/mcq', qs.stringify(eventObject));
            let tempResponse = result.data.response
            let question = tempResponse.substring(tempResponse.indexOf("question") + 11,
            tempResponse.indexOf("options") - 3);
            let options = tempResponse.substring(tempResponse.indexOf("options") + 9,
            tempResponse.indexOf("answer") - 2);
            options = JSON.parse(options.replace(/'/g, '"'))
            let answer = tempResponse.substring(tempResponse.indexOf("answer"), tempResponse.length);
            question = question.split('\n');
            setNewQuestion(question);
            setNewAnswer(answer); 
            setNewOptions(options)
            if (saveQ) {
                setUpdateQ(true);
                setSaveQ(false);
            }
        } catch (error) {
            console.log(error)
        }
        }
        if (effectRan.current === false) {
            fetchQuestion()
        }

        return () => {
            effectRan.current = true;
        }
        
    }, [generate])

    useEffect(() => {
        setQuestion(newQuestion);
        setAnswer(newAnswer);
        setOptions(newOptions);
    }, [updateQ])

    useEffect(() => {
        let curr_answer = answer.substring(9, answer.indexOf("}") - 1);
        let answer_option = option_letters[options.indexOf(curr_answer)]
        if (answer_option != null) {
            if (answer_option == select) {
                setIsCorrect(true);
            } else {
                setIsCorrect(false);
            }
    }},
    [check])

    return (
        <>
        <div className="navbar">
            <h1 className="header-title" onClick={() => navigate('/')}>scioly.pro</h1>
            <p onClick={() => navigate('/menu')} className="header-text">generate test</p>
            <p onClick={() => navigate('/menu')}className="header-text">practice questions</p>
            <p className="header-text">sign up</p>
        </div>
        <div className="main">
            <div className="title-con">
                <p className="page-subtitle1">{event}</p>
                <h1 className="page-title">{title}</h1>
                <p className="subtext">{description}</p>
                <div className="aristo-con">
                    <p className="subtext"><b>{question}</b></p>
                    {options.map((option, index) => {
                        return (
                            <div>
                                <input onClick={() => setSelect(option_letters[index])} type="radio" name="option" id="option"/>
                                <label className="subtext" for="option">{option_letters[index] + ". " + option}</label>
                            </div>
                        ) 
                    })}
                    {isCorrect && 
                    <div style={{'background-color':'rgb(53, 120, 53)'}} className="answer-choice">
                        <p className="subtext">Correct!</p>
                    </div>}
                    {isCorrect == false && 
                    <div style={{'background-color': '#8d241e'}}className="answer-choice">
                        <p className="subtext">Wrong! The correct answer is { 
                        option_letters[options.indexOf(answer.substring(9, answer.indexOf("}") - 1))]
                        + ". " + answer.substring(9, answer.length -2) + "."}</p>
                    </div>}
                    <div className="mb2-con">
                        <button onClick={() => setCheck(!check)} className="mcq-button">Submit</button>
                    </div>
                </div>
            </div>
        </div>
        </>
    )
}

export default MCQPage;
