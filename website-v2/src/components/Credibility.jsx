import { useState } from 'react'
import { Play } from 'lucide-react'

const LOOM_ID = 'a243a6f8c920487a9db15e9c9816c36e'

const stack = ['n8n', 'Claude (Anthropic)', 'Gmail API', 'Shopify', 'WooCommerce', 'Playwright', 'Python']

export default function Credibility() {
  const [loaded, setLoaded] = useState(false)

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
            Kein Template. Kein Baukasten.<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>Kein Abo.</em>
          </h2>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(0, 1fr)',
          gap: '3rem',
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
              „Ich baue seit 2024 KI-Support-Workflows auf n8n-Basis. Jeder Agent wird für einen konkreten Shop entwickelt — angepasst an Stack, Ticket-Typen und Tonalität. Statt Demo-Screenshots zeige ich dir direkt eine Live-Demo eines funktionsfähigen Systems."
            </p>
            <footer style={{
              fontSize: '0.825rem',
              color: 'var(--text-subtle)',
              letterSpacing: '0.03em',
            }}>
              — Ilias Tebque, Gründer GetKiAgent
            </footer>
          </blockquote>

          <div>
            <p style={{
              fontSize: '0.8rem',
              color: 'var(--text-subtle)',
              textTransform: 'uppercase',
              letterSpacing: '0.12em',
              marginBottom: '0.875rem',
              fontWeight: 600,
            }}>
              Live-Demo eines gebauten Agenten
            </p>
            <div
              style={{
                position: 'relative',
                width: '100%',
                maxWidth: '820px',
                aspectRatio: '16 / 9',
                borderRadius: 'var(--r-md)',
                overflow: 'hidden',
                border: '1px solid var(--border-strong)',
                background: 'var(--bg-elevated)',
                cursor: loaded ? 'default' : 'pointer',
              }}
              onClick={() => setLoaded(true)}
            >
              {loaded ? (
                <iframe
                  src={`https://www.loom.com/embed/${LOOM_ID}?autoplay=1`}
                  title="GetKiAgent Live-Demo"
                  loading="lazy"
                  frameBorder="0"
                  allow="autoplay; fullscreen; picture-in-picture"
                  allowFullScreen
                  style={{
                    position: 'absolute',
                    inset: 0,
                    width: '100%',
                    height: '100%',
                  }}
                />
              ) : (
                <button
                  type="button"
                  aria-label="Live-Demo abspielen"
                  onClick={() => setLoaded(true)}
                  style={{
                    position: 'absolute',
                    inset: 0,
                    width: '100%',
                    height: '100%',
                    background: 'radial-gradient(ellipse at center, rgba(201,166,107,0.15) 0%, rgba(11,14,20,0.4) 70%)',
                    border: 'none',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--text)',
                  }}
                >
                  <span style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '72px',
                    height: '72px',
                    borderRadius: '50%',
                    background: 'var(--accent)',
                    color: 'var(--bg)',
                    boxShadow: '0 12px 40px -8px rgba(201, 166, 107, 0.5)',
                  }}>
                    <Play size={26} fill="currentColor" style={{ marginLeft: '4px' }} />
                  </span>
                </button>
              )}
            </div>
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
