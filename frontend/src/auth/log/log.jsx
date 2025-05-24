import React from 'react'
import './log.css'
import { LoginButton } from '@telegram-auth/react';


function Log() {
    return (
      <>
        <div className='container'>
            <div className='regplace'>
                     
                <h1 className='header'>Log in</h1>
                <input className='email' type="email" placeholder='Email/Телефон'/>
                <input className='email' type="password" placeholder='Пароль' />
                <div className='btns'>
                    <button className='reg'>Log in</button>
                    <button className='login'>Reg in</button>
                </div>
                        
          

            </div>
        </div>
      </>
    )
  }
  
  export default Log