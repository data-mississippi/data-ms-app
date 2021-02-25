import React from 'react'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from 'react-router-dom'
import './styles/App.css'
import './styles/generated-styles.css'

function Home() {
  return (
    <p>general map</p>
  )
}

function About() {
  return (
    <p>About Data Mississippi</p>
  )
}

function VotingPrecinctMaps() {
  return (
    <h1>Voting Precinct Maps</h1>
  )
}

function App() {
  return (
    <Router>
      <>
        <nav className="p-4 flex flex-row justify-between bg-blue-100">
          <div>
            <p className="font-black text-2xl text-blue-900">DATA MISSISSIPPI</p>
            <p className="font-mono">Information for people and machines.</p>
          </div>
          
          <ul className="flex flex-row items-center font-bold text-blue-900">
            <li className="m-2">
              <Link to="/">Home</Link>
            </li>
            <li className="m-2">
              <Link to="/about">About</Link>
            </li>
            <li className="m-2">
              <Link to="/precinct-maps">Voting Precinct Maps</Link>
            </li>
            <li className="m-2">
              <Link to="/docs/">API Documentation</Link>
            </li>
          </ul>
        </nav>

        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
        <div className="container mx-auto">
          <Switch>
            
            <Route exact path="/about">
              <About />
            </Route>
            <Route exact path="/precinct-maps">
              <VotingPrecinctMaps />
            </Route>
            <Route exact path="/">
              <Home />
            </Route>
          </Switch>
        </div>
      </>
    </Router>
  )
}

export default App;
