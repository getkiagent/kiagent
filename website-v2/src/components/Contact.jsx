export default function Contact() {
  return (
    <section
      id="kontakt"
      className="section"
      style={{
        background: 'var(--bg-elevated)',
        borderTop: '1px solid var(--border)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <div aria-hidden="true" style={{
        position: 'absolute',
        top: '-20%',
        right: '-10%',
        width: '700px',
        height: '500px',
        background: 'radial-gradient(ellipse at center, rgba(201, 166, 107, 0.08) 0%, transparent 65%)',
        pointerEvents: 'none',
      }} />

      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <div style={{ marginBottom: '3rem', maxWidth: '720px' }}>
          <p className="eyebrow">Kontakt</p>
          <h2 className="display-l" style={{ marginBottom: '1rem' }}>
            30 Minuten.<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>Keine Verkaufsmasche.</em>
          </h2>
          <p className="lead">
            Buch dir einen Call. Wir schauen deinen Support-Alltag an und ich sage dir ehrlich, ob KI bei dir Sinn ergibt — und wenn ja, wie ein konkreter Build aussehen würde.
          </p>
        </div>

        <div style={{
          background: 'var(--bg)',
          border: '1px solid var(--border-strong)',
          borderRadius: 'var(--r-lg)',
          overflow: 'hidden',
          maxWidth: '900px',
        }}>
          <iframe
            src="https://cal.com/getkiagent?embed=1&theme=dark"
            title="Termin bei GetKiAgent buchen"
            loading="lazy"
            style={{
              width: '100%',
              height: '680px',
              border: 'none',
              display: 'block',
              background: 'var(--bg)',
            }}
          />
        </div>

        <p style={{
          marginTop: '1.25rem',
          color: 'var(--text-subtle)',
          fontSize: '0.85rem',
          maxWidth: '720px',
        }}>
          Cal.com lädt nicht? Schreib direkt an{' '}
          <a
            href="mailto:getkiagent@gmail.com"
            style={{
              color: 'var(--accent)',
              textDecoration: 'underline',
              textUnderlineOffset: '3px',
              textDecorationColor: 'rgba(201, 166, 107, 0.4)',
            }}
          >
            getkiagent@gmail.com
          </a>
          {' '}— Antwort innerhalb von 24h.
        </p>
      </div>
    </section>
  )
}
