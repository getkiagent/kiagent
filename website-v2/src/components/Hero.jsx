import { ArrowRight } from 'lucide-react'
import SceneBackground from './SceneBackground'

export default function Hero() {
  return (
    <section
      id="hero"
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 'clamp(8rem, 14vh, 10rem) 1.5rem clamp(4rem, 8vh, 6rem)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      <SceneBackground opacity={0.72} particleCount={95} />

      {/* Radial glow — outer */}
      <div aria-hidden="true" style={{
        position: 'absolute',
        top: '40%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '1100px',
        height: '800px',
        background: 'radial-gradient(ellipse at center, rgba(201, 166, 107, 0.09) 0%, transparent 55%)',
        pointerEvents: 'none',
        zIndex: 0,
      }} />

      {/* Radial glow — inner tight */}
      <div aria-hidden="true" style={{
        position: 'absolute',
        top: '38%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '500px',
        height: '400px',
        background: 'radial-gradient(ellipse at center, rgba(201, 166, 107, 0.13) 0%, transparent 65%)',
        pointerEvents: 'none',
        zIndex: 0,
      }} />

      {/* 3D perspective grid floor */}
      <div aria-hidden="true" style={{
        position: 'absolute',
        bottom: 0,
        left: '-20%',
        right: '-20%',
        height: '380px',
        backgroundImage: `
          linear-gradient(rgba(201, 166, 107, 0.14) 1px, transparent 1px),
          linear-gradient(90deg, rgba(201, 166, 107, 0.14) 1px, transparent 1px)
        `,
        backgroundSize: '60px 60px',
        transform: 'perspective(360px) rotateX(70deg)',
        transformOrigin: 'bottom center',
        WebkitMaskImage: 'linear-gradient(to top, rgba(0,0,0,0.75) 0%, transparent 75%)',
        maskImage: 'linear-gradient(to top, rgba(0,0,0,0.75) 0%, transparent 75%)',
        pointerEvents: 'none',
        zIndex: 0,
      }} />

      <div style={{ maxWidth: '880px', margin: '0 auto', textAlign: 'center', position: 'relative', zIndex: 1 }}>
        <div className="eyebrow" style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '0.625rem',
          padding: '0.375rem 0.875rem',
          border: '1px solid var(--border-strong)',
          borderRadius: '2rem',
          background: 'rgba(201, 166, 107, 0.04)',
          marginBottom: '2rem',
        }}>
          <span style={{
            width: 6, height: 6, borderRadius: '50%',
            background: 'var(--accent)',
            display: 'inline-block',
          }} />
          KI-Support-Automation · DACH E-Commerce
        </div>

        <h1 className="display-xl" style={{ marginBottom: '1rem' }}>
          Statt einer{' '}
          <em style={{
            fontStyle: 'italic',
            color: 'var(--accent)',
            fontFamily: 'var(--font-serif)',
            fontVariationSettings: "'opsz' 144",
          }}>
            Support-Vollzeitkraft.
          </em>
        </h1>

        <p style={{
          fontFamily: 'var(--font-serif)',
          fontSize: 'clamp(1.15rem, 2.2vw, 1.5rem)',
          color: 'var(--text-muted)',
          lineHeight: 1.45,
          marginBottom: '2.5rem',
          letterSpacing: '-0.01em',
        }}>
          60–70 % deiner Anfragen automatisiert. Festpreis. Tag 14 live.
        </p>

        <div style={{
          display: 'flex',
          gap: '0.875rem',
          justifyContent: 'center',
          flexWrap: 'wrap',
          marginBottom: '3rem',
        }}>
          <a href="#kontakt" className="btn-primary">
            Kostenloses Erstgespräch <ArrowRight size={17} />
          </a>
          <a href="#demo" className="btn-secondary">
            30-Sek Demo ansehen
          </a>
        </div>

        <div style={{
          display: 'flex',
          gap: '0.75rem',
          justifyContent: 'center',
          flexWrap: 'wrap',
          marginBottom: '2rem',
        }}>
          {[
            { value: '< 2 Sek', label: 'WISMO-Antwort' },
            { value: '90 Sek', label: 'Retoure einleiten' },
            { value: '24 / 7', label: 'ohne Schichtbetrieb' },
          ].map(({ value, label }) => (
            <div key={label} style={{
              background: 'var(--bg-elevated)',
              border: '1px solid var(--border)',
              borderRadius: 'var(--r-sm)',
              padding: '0.625rem 1.125rem',
              textAlign: 'center',
            }}>
              <div style={{
                fontFamily: 'var(--font-serif)',
                fontSize: '1.1rem',
                fontWeight: 500,
                color: 'var(--text)',
                letterSpacing: '-0.02em',
                lineHeight: 1,
              }}>
                {value}
              </div>
              <div style={{
                fontSize: '0.7rem',
                color: 'var(--text-subtle)',
                marginTop: '0.2rem',
                letterSpacing: '0.03em',
              }}>
                {label}
              </div>
            </div>
          ))}
        </div>

        <ul style={{
          display: 'flex',
          gap: '0.5rem 1.75rem',
          justifyContent: 'center',
          flexWrap: 'wrap',
          listStyle: 'none',
          color: 'var(--text-subtle)',
          fontSize: '0.8rem',
          letterSpacing: '0.02em',
        }}>
          {['DSGVO-konform', 'EU-gehostet', 'Individueller Build', 'Setup in 2 Wochen', 'Festpreis ab €2.000'].map((t) => (
            <li key={t} style={{ position: 'relative' }}>
              <span style={{
                display: 'inline-block',
                width: 4,
                height: 4,
                borderRadius: '50%',
                background: 'var(--accent)',
                marginRight: '0.5rem',
                verticalAlign: 'middle',
              }} />
              {t}
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}
