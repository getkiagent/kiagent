import { useState, useEffect } from 'react'

export default function StickyCtaMobile() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    function check() {
      setVisible(window.innerWidth < 768 && window.scrollY > 300)
    }
    check()
    window.addEventListener('scroll', check, { passive: true })
    window.addEventListener('resize', check, { passive: true })
    return () => {
      window.removeEventListener('scroll', check)
      window.removeEventListener('resize', check)
    }
  }, [])

  if (!visible) return null

  return (
    <div
      aria-hidden="true"
      style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 200,
        background: 'rgba(11, 14, 20, 0.95)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        borderTop: '1px solid var(--border-strong)',
        padding: '0.875rem 1.25rem',
        display: 'flex',
        gap: '0.75rem',
      }}
    >
      <a
        href="#demo"
        style={{
          flex: 1,
          textAlign: 'center',
          padding: '0.75rem',
          background: 'transparent',
          border: '1px solid var(--border-strong)',
          borderRadius: 'var(--r-sm)',
          color: 'var(--text)',
          fontSize: '0.875rem',
          fontWeight: 500,
          textDecoration: 'none',
          fontFamily: 'var(--font-sans)',
        }}
      >
        Demo
      </a>
      <a
        href="#kontakt"
        style={{
          flex: 2,
          textAlign: 'center',
          padding: '0.75rem',
          background: 'var(--accent)',
          borderRadius: 'var(--r-sm)',
          color: 'var(--bg)',
          fontSize: '0.875rem',
          fontWeight: 600,
          textDecoration: 'none',
          fontFamily: 'var(--font-sans)',
        }}
      >
        Kostenloses Gespräch
      </a>
    </div>
  )
}
