import React, { useRef, useState, useEffect } from 'react';
import { useNavigate }   from 'react-router-dom';
import { logout as logoutApi } from '../../api/auth';
import { clearCurrent   } from '../../auth/storage';

import './avatarMenu.css';


export default function AvatarMenu({ initials = 'U' }) {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const refMenu  = useRef(null);
  const refBtn   = useRef(null);


  useEffect(() => {
    const handler = (e) => {
      if (
        open &&
        refMenu.current &&
        !refMenu.current.contains(e.target) &&
        refBtn.current &&
        !refBtn.current.contains(e.target)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [open]);

  /** Выход */
  const handleLogout = async () => {
    try { await logoutApi(); } catch {}
    clearCurrent();
    navigate('/', { replace: true });
  };

  return (
    <>
      <button
        ref={refBtn}
        className="sidebar-avatar"
        onClick={() => setOpen(!open)}
        aria-label="User menu"
      >
        {initials}
      </button>

      {open && (
        <div ref={refMenu} className="avatar-popover">
          <button
            className="pop-item"
            onClick={() => { setOpen(false); navigate('/profile'); }}
          >
            Profile
          </button>

          <div className="divider" />

          <button className="pop-item" onClick={handleLogout}>
            Logout
          </button>
        </div>
      )}
    </>
  );
}
