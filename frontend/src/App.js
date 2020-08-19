import React from 'react';
import axios from 'axios';
import './App.css';
import './generated-styles.css';

function VoteCountInput() {
  return (
    <textarea>
      
    </textarea>
  )
}

function handleSubmit(event) {
  const text = document.querySelector('#char-input').value

  axios
    .get(`/char_count?text=${text}`).then(({data}) => {
      document.querySelector('#char-count').textContent = `${data.count} characters!`
    })
    .catch(err => console.log(err))
}

function App() {
  return (
    <div className="App">
      <div>
        <label htmlFor='char-input'>How many characters does</label>
        <input id='char-input' type='text' />
        <button onClick={handleSubmit}>have?</button>
      </div>

      <div>
        <h3 id='char-count'></h3>
      </div>

      <div className="max-w-md mx-auto flex p-6 bg-gray-100 mt-10 rounded-lg shadow-xl">
        <div className="ml-6 pt-1">
          <h1 className="text-2xl text-blue-700 leading-tight">
            Tailwind and Create React App
      </h1>
          <p className="text-base text-gray-700 leading-normal">
            Building apps together
      </p>
        </div>
      </div>
    </div>
  );
}

export default App;
