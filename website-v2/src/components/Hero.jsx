import { ArrowRight } from 'lucide-react'

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
      <div aria-hidden="true" style={{
        position: 'absolute',
        bottom: '-20%',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '900px',
        height: '600px',
        background: 'radial-gradient(ellipse at center, rgba(201, 166, 107, 0.08) 0%, transparent 65%)',
        pointerEvents: 'none',
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

        <h1 className="display-xl" style={{ marginBottom: '1.5rem' }}>
          Individuelle KI-Support-Automation für deinen Shop —{' '}
          <em style={{
            fontStyle: 'italic',
            color: 'var(--accent)',
            fontFamily: 'var(--font-serif)',
            fontVariationSettings: "'opsz' 144",
          }}>
            nicht zusammengeklickt.
          </em>
        </h1>

        <p className="lead" style={{
          margin: '0 auto 2.5rem',
          fontSize: 'clamp(1rem, 1.6vw, 1.15rem)',
        }}>
          Ich baue n8n-basierte Agenten, die auf deinem Stack laufen, deine echten Tickets beantworten und in deiner eigenen Cloud gehostet werden. Kein SaaS-Abo, kein Template.
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
          <a href="#warum" className="btn-secondary">
            Live-Demo ansehen
          </a>
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
          {['DSGVO-konform', 'EU-gehostet', 'Individueller Build', 'Setup in 2 Wochen'].map((t) => (
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
