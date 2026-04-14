export default function Footer() {
  const year = new Date().getFullYear()

  return (
    <footer
      style={{
        background: 'var(--bg)',
        borderTop: '1px solid var(--border)',
        padding: '2rem clamp(1.5rem, 4vw, 3rem)',
      }}
    >
      <div style={{
        maxWidth: '1120px',
        margin: '0 auto',
        display: 'flex',
        flexWrap: 'wrap',
        gap: '1.25rem 2rem',
        alignItems: 'center',
        justifyContent: 'space-between',
        fontSize: '0.825rem',
        color: 'var(--text-subtle)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem' }}>
          <span style={{
            fontFamily: 'var(--font-serif)',
            fontSize: '0.95rem',
            fontWeight: 500,
          }}>
            <span style={{ color: 'var(--text-muted)' }}>GetKi</span>
            <span style={{ color: 'var(--accent)' }}>Agent</span>
          </span>
          <span style={{ color: 'var(--border-strong)' }}>·</span>
          <span>© {year} Ilias Tebque</span>
        </div>

        <nav aria-label="Rechtliches" style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
          <a
            href="/impressum.html"
            style={{ color: 'var(--text-muted)', textDecoration: 'none', transition: 'color 0.2s ease' }}
            onMouseEnter={(e) => (e.target.style.color = 'var(--accent)')}
            onMouseLeave={(e) => (e.target.style.color = 'var(--text-muted)')}
          >
            Impressum
          </a>
          <a
            href="/datenschutz.html"
            style={{ color: 'var(--text-muted)', textDecoration: 'none', transition: 'color 0.2s ease' }}
            onMouseEnter={(e) => (e.target.style.color = 'var(--accent)')}
            onMouseLeave={(e) => (e.target.style.color = 'var(--text-muted)')}
          >
            Datenschutz
          </a>
          <a
            href="mailto:getkiagent@gmail.com"
            style={{ color: 'var(--text-muted)', textDecoration: 'none', transition: 'color 0.2s ease' }}
            onMouseEnter={(e) => (e.target.style.color = 'var(--accent)')}
            onMouseLeave={(e) => (e.target.style.color = 'var(--text-muted)')}
          >
            getkiagent@gmail.com
          </a>
        </nav>
      </div>
    </footer>
  )
}
