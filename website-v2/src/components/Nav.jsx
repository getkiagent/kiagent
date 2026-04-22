import { useState, useEffect } from 'react'

export default function Nav() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 100,
        transition: 'background 0.3s ease, border-color 0.3s ease, backdrop-filter 0.3s ease, height 0.3s ease',
        background: scrolled ? 'rgba(11, 14, 20, 0.88)' : 'transparent',
        backdropFilter: scrolled ? 'blur(18px) saturate(1.2)' : 'none',
        WebkitBackdropFilter: scrolled ? 'blur(18px) saturate(1.2)' : 'none',
        borderBottom: scrolled ? '1px solid var(--border)' : '1px solid transparent',
      }}
    >
      <nav
        aria-label="Hauptnavigation"
        style={{
          maxWidth: '1120px',
          margin: '0 auto',
          padding: '0 clamp(1.25rem, 3vw, 2rem)',
          height: scrolled ? '64px' : '76px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          transition: 'height 0.3s ease',
        }}
      >
        <a
          href="#"
          aria-label="GetKiAgent Startseite"
          style={{
            textDecoration: 'none',
            fontFamily: 'var(--font-serif)',
            fontSize: '1.35rem',
            fontWeight: 500,
            letterSpacing: '-0.01em',
            display: 'flex',
            alignItems: 'center',
            gap: 0,
          }}
        >
          <span style={{ color: 'var(--text)' }}>GetKi</span>
          <span style={{ color: 'var(--accent)' }}>Agent</span>
        </a>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
          <div className="nav-links" style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            {[
              { label: 'Leistungen', href: '#leistungen' },
              { label: 'Ablauf',     href: '#ablauf' },
              { label: 'Preise',     href: '#preise' },
              { label: 'Kontakt',    href: '#kontakt' },
            ].map(({ label, href }) => (
              <a
                key={href}
                href={href}
                style={{
                  color: 'var(--text-muted)',
                  textDecoration: 'none',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  transition: 'color 0.2s ease',
                  whiteSpace: 'nowrap',
                }}
                onMouseEnter={(e) => (e.target.style.color = 'var(--accent)')}
                onMouseLeave={(e) => (e.target.style.color = 'var(--text-muted)')}
              >
                {label}
              </a>
            ))}
          </div>
          <a href="#demo" className="btn-primary" style={{ padding: '0.625rem 1.25rem', fontSize: '0.875rem', whiteSpace: 'nowrap' }}>
            Demo ansehen
          </a>
        </div>
      </nav>
    </header>
  )
}
