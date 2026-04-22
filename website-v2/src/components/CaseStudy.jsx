import { Zap, Clock, Globe, TrendingDown } from 'lucide-react'
import ChatDemo from './ChatDemo'
import DemoCarousel from './DemoCarousel'

const metrics = [
  { icon: Zap,          value: '< 2 Sek.',   label: 'WISMO-Antwort',      sub: 'vs. 4h per E-Mail' },
  { icon: Clock,        value: '90 Sek.',     label: 'Retoure einleiten',  sub: 'vs. 8 Min. E-Mail-Ping-Pong' },
  { icon: Globe,        value: '5 Sprachen',  label: 'ohne Personal-Hire', sub: 'DE · EN · FR · IT · NL' },
  { icon: TrendingDown, value: '24 / 7',      label: 'Verfügbarkeit',      sub: '€0 Grenzkosten pro Ticket' },
]

export default function CaseStudy() {
  return (
    <section
      id="demo"
      className="section"
      style={{
        background: 'var(--bg-elevated)',
        borderTop: '1px solid var(--border)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Subtle background glow */}
      <div aria-hidden="true" style={{
        position: 'absolute',
        top: '30%',
        left: '50%',
        transform: 'translateX(-50%)',
        width: '800px',
        height: '400px',
        background: 'radial-gradient(ellipse at center, rgba(201, 166, 107, 0.04) 0%, transparent 65%)',
        pointerEvents: 'none',
        zIndex: 0,
      }} />

      <div className="container" style={{ position: 'relative', zIndex: 1 }}>
        <div style={{ marginBottom: '3rem', maxWidth: '720px' }}>
          <p className="eyebrow">Demo-Szenario</p>
          <h2 className="display-l" style={{ marginBottom: '1rem' }}>
            So sieht der Agent<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>in der Praxis aus.</em>
          </h2>
          <p className="lead">
            GlowLab — fiktiver Beauty-Shop, 600 Tickets/Monat, 3 Support-Mitarbeiter. Die Mechanik dahinter ist real.
          </p>
        </div>

        {/* Metric cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1rem',
          marginBottom: '3rem',
        }}>
          {metrics.map(({ icon: Icon, value, label, sub }) => (
            <div key={label} style={{
              background: 'var(--bg)',
              border: '1px solid var(--border)',
              borderRadius: 'var(--r-md)',
              padding: '1.5rem',
              position: 'relative',
              overflow: 'hidden',
            }}>
              <div aria-hidden="true" style={{
                position: 'absolute', top: 0, left: 0, right: 0,
                height: '2px',
                background: 'linear-gradient(90deg, var(--accent) 0%, transparent 100%)',
                opacity: 0.5,
              }} />
              <Icon size={18} color="var(--accent)" strokeWidth={1.75} style={{ marginBottom: '0.75rem', opacity: 0.8 }} />
              <div style={{
                fontFamily: 'var(--font-serif)',
                fontSize: 'clamp(1.5rem, 3vw, 2rem)',
                fontWeight: 500,
                color: 'var(--text)',
                letterSpacing: '-0.025em',
                lineHeight: 1,
                marginBottom: '0.25rem',
              }}>{value}</div>
              <div style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.25rem' }}>{label}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-subtle)' }}>{sub}</div>
            </div>
          ))}
        </div>

        {/* Chat + Screenshots side by side */}
        <div style={{
          display: 'flex',
          gap: '1.5rem',
          flexWrap: 'wrap',
          alignItems: 'flex-start',
        }}>
          <ChatDemo />
          <DemoCarousel />
        </div>
      </div>
    </section>
  )
}
