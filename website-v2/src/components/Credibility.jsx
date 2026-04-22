const stack = ['n8n', 'Claude (Anthropic)', 'Gmail API', 'Shopify', 'WooCommerce', 'Playwright', 'Python']

export default function Credibility() {
  return (
    <section
      id="warum"
      className="section"
      style={{
        background: 'var(--bg)',
        borderTop: '1px solid var(--border)',
      }}
    >
      <div className="container">
        <div style={{ marginBottom: '3rem', maxWidth: '720px' }}>
          <p className="eyebrow">Warum mir</p>
          <h2 className="display-l">
            Kein Agency-Pitch.<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>Retail-Ops-Background.</em>
          </h2>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(0, 1fr)',
          gap: '2rem',
          alignItems: 'start',
        }}>
          <blockquote style={{
            background: 'var(--bg-elevated)',
            border: '1px solid var(--border)',
            borderLeft: '3px solid var(--accent)',
            borderRadius: 'var(--r-md)',
            padding: 'clamp(1.75rem, 3vw, 2.5rem)',
            maxWidth: '820px',
          }}>
            <p style={{
              fontFamily: 'var(--font-serif)',
              fontSize: 'clamp(1.15rem, 2vw, 1.375rem)',
              fontWeight: 400,
              color: 'var(--text)',
              lineHeight: 1.55,
              letterSpacing: '-0.01em',
              marginBottom: '1.25rem',
              fontStyle: 'italic',
            }}>
              „Ich war selbst Filialleiter mit 50 Mitarbeitern und siebenstelliger Umsatzverantwortung. Ich kenne den Aufwand und die Kosten von Support-Personal aus erster Hand — und weiß genau, wo Automatisierung wirklich greift und wo nicht.“
            </p>
            <footer style={{
              fontSize: '0.825rem',
              color: 'var(--text-subtle)',
              letterSpacing: '0.03em',
            }}>
              — Ilias Tebque, Gründer GetKiAgent · 4+ Jahre Retail-Ops-Background
            </footer>
          </blockquote>

          <div style={{
            display: 'flex',
            gap: '1.5rem',
            flexWrap: 'wrap',
            maxWidth: '820px',
          }}>
            {[
              { value: '50', label: 'Mitarbeiter geführt' },
              { value: '7-stellig', label: 'Umsatzverantwortung' },
              { value: '4+', label: 'Jahre Retail-Ops' },
            ].map(({ value, label }) => (
              <div
                key={label}
                style={{
                  flex: '1 1 160px',
                  background: 'var(--bg-elevated)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--r-md)',
                  padding: '1.25rem 1.5rem',
                }}
              >
                <div style={{
                  fontFamily: 'var(--font-serif)',
                  fontSize: 'clamp(1.5rem, 2.5vw, 2rem)',
                  fontWeight: 500,
                  color: 'var(--accent)',
                  letterSpacing: '-0.02em',
                  lineHeight: 1,
                  marginBottom: '0.375rem',
                }}>
                  {value}
                </div>
                <div style={{
                  fontSize: '0.825rem',
                  color: 'var(--text-subtle)',
                }}>
                  {label}
                </div>
              </div>
            ))}
          </div>

          <div style={{ maxWidth: '820px' }}>
            <p style={{
              fontSize: '0.75rem',
              color: 'var(--text-subtle)',
              textTransform: 'uppercase',
              letterSpacing: '0.12em',
              marginBottom: '0.875rem',
              fontWeight: 600,
            }}>
              Entwickelt mit
            </p>
            <div style={{
              display: 'flex',
              gap: '0.5rem',
              flexWrap: 'wrap',
            }}>
              {stack.map((tech) => (
                <span
                  key={tech}
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    padding: '0.5rem 0.875rem',
                    background: 'var(--bg-elevated)',
                    border: '1px solid var(--border)',
                    borderRadius: '2rem',
                    fontSize: '0.8rem',
                    color: 'var(--text-muted)',
                    fontWeight: 500,
                    letterSpacing: '0.01em',
                  }}
                >
                  {tech}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
