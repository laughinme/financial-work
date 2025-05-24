import React from 'react'
import './reg.css'
import { LoginButton } from '@telegram-auth/react';


function Reg() {
    return (
      <>
        <div className='container'>
            <div className='regplace'>
                     
                <h1 className='header'>Registration</h1>
                <input className='email' type="email" placeholder='Email/Телефон'/>
                <input className='email' type="password" placeholder='Пароль' />
                <div className='btns'>
                    <button className='reg'>Create an account</button>
                    <button className='login'>Log in</button>
                </div>
                        
          

            </div>
        </div>
      </>
    )
  }
  
  export default Reg