import { useEffect } from 'react';
import './App.css';
import Splashpage from './pages/Splashpage'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/Login';
function App() {
  return (

    <Router>
      <Routes>
        <Route exact path='/' element={<Splashpage />} />
        <Route exact path='/login' element={<Login />} />
      </Routes>
    </Router>
  )

}

export default App;
