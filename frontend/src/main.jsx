import React from 'react'
import { createRoot } from 'react-dom/client'
import './auth.css'
import Reg from './auth/reg/reg.jsx'
import Log from './auth/log/log.jsx'


createRoot(document.getElementById('root')).render(
    <div className='block'>
        <Reg />
        <Log />
    </div>
    )