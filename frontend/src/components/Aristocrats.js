import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, StaticRouter} from 'react-router-dom';
import axios from 'axios';
import qs from 'qs';

function Aristocrats() {

    const navigate = useNavigate();
    const [type, setType] = useState('K1');
    const [difficulty, setDifficulty] = useState('Easy');
    const [aristo, setAristo] = useState(false);
    const [frequency, setFrequency] = useState([]);
    const [plaintext, setPlaintext] = useState('')
    const [ciphertext, setCiphertext] = useState('');
    const [solution, setSolution] = useState('');
    const [guessAlphabet, setGuessAlphabet] = useState(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']);
    const alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
    const [updateLetter, setUpdateLetter] = useState(false)

    useEffect(() => {
        const alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        let tempSolutionText = "";
        console.log(ciphertext);
        for (let i = 0; i < ciphertext.length; i++) {
            if (alphabet.indexOf(ciphertext.substring(i, i+1)) > -1) {
                tempSolutionText += guessAlphabet[alphabet.indexOf(ciphertext.substring(i, i+1).toUpperCase())];
            }
            else {
                tempSolutionText += ciphertext.substring(i, i+1);
            }
        }
        setSolution(tempSolutionText);
        
        if (solution.length > 0 && solution == plaintext.toLowerCase()) {
            alert('You win');
        }
    }, [updateLetter, guessAlphabet, ciphertext, solution])

    const generateAristo = async () => {
        const settingsObject = {
            'type': type,
            'difficulty': difficulty
        }
        try {
            const response = await axios.post('/aristo', qs.stringify(settingsObject))
            setCiphertext(response.data.ciphertext);
            setSolution(response.data.ciphertext);
            setPlaintext(response.data.plaintext);
            setFrequency(response.data.frequency);
            setAristo(true);
        } catch (error) {
            console.log(error);
        }
        }

    const updateAlphabet = (new_letter, index) => {
        let currGuessAlphabet = guessAlphabet;
        if (new_letter.length > 0) 
            currGuessAlphabet[index] = new_letter.toLowerCase();
        else
            currGuessAlphabet[index] = alphabet[index];
        setGuessAlphabet(currGuessAlphabet);
        setUpdateLetter(!updateLetter);
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
            <div className="title-con">
                <p className="page-subtitle1">CodeBusters</p>
                <h1 className="page-title">aristocrat generator</h1>
                <p className="subtext">every letter is encoded with a seperate ciphertext letter</p>
                <div className="settings-con">
                    <p className="settings-text">Customize Settings</p>
                    <div className="settings-subcon">
                        <select className="settings" value={type} onChange={(e) => setType(e.target.value)}>
                            <option>K1</option>
                            <option>K2</option>
                        </select>
                        <select className="settings" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
                            <option>Easy</option>
                            <option>Medium</option>
                            <option>Hard</option>
                        </select>
                        <button className="mini-button" onClick={() => generateAristo()}>Generate</button>
                    </div>
                </div>
                {aristo && <div className="aristo-con">
                    <h1 className="cipher-text">{ciphertext}</h1>
                    <h1 className="cipher-text">{solution}</h1>
                    <table className="table">
                        <thead className="table-head">
                            <tr>
                                {alphabet.map((letter, index) => (
                                    <th className="table-head-element" key={index}>{letter}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                {frequency.map((number, index) =>
                                    <td className="table-element" key={index}>{number}</td>
                                )}
                            </tr>
                            <tr>
                                {alphabet.map((letter, index) =>
                                    <td className="table-element" key={index}>
                                        <input className="table-input" placeholder={letter}
                                        value={guessAlphabet[index] != letter ? guessAlphabet[index] : ""}
                                        onChange={(e) => updateAlphabet(e.target.value, index)}/>
                                    </td>
                                )}
                            </tr>
                        </tbody>
                    </table>
                </div>}
            </div>
        </div>
        </>
    )
}

export default Aristocrats;