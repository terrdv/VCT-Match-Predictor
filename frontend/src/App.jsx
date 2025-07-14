import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import {Routes, Route} from 'react-router-dom'
import './css/App.css'
import NavBar from './components/Navbar'
import Home from './pages/Home'

function App() {


  return (
    <div>
      <NavBar />
      <main className="main-content">
        <Routes>
          <Route path='/' element={<Home />} />
        </Routes> 
      </main>
      
    </div>
  )
}

export default App
