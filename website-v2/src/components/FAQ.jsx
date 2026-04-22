import { useState } from 'react'
import { ChevronDown } from 'lucide-react'

const items = [
  {
    q: 'Wie lange dauert die Integration?',
    a: 'Ca. 2 Wochen — parallel zum laufenden Betrieb. Du musst nichts an deinem Shop anpassen. Wir verbinden uns über die bestehende API.',
  },
  {
    q: 'Was passiert mit den Kundendaten?',
    a: 'Alle Daten bleiben in der EU. Auftragsverarbeitungsvertrag (AVV) inklusive. Kein US-Hyperscaler im Datenpfad deiner Kundenanfragen.',
  },
  {
    q: 'Was wenn der Agent eine Frage nicht beantworten kann?',
    a: 'Automatische Eskalation an dein Team — per E-Mail, in Gorgias oder Zendesk, mit vollständigem Gesprächskontext. Kein Ticket geht verloren.',
  },
  {
    q: 'Wie lange bin ich vertraglich gebunden?',
    a: 'Starter: kein Jahresvertrag, monatlich kündbar nach der Setup-Phase. Professional und Enterprise: 6 Monate Mindestlaufzeit.',
  },
  {
    q: 'Funktioniert das auch mit WooCommerce oder Shopware?',
    a: 'Ja. Shopify, WooCommerce und Shopware werden vollständig unterstützt. Für andere Systeme: kurz fragen, meistens lösbar.',
  },
  {
    q: 'Ich habe keine KI-Erfahrung — ist das ein Problem?',
    a: 'Nein. Du bekommst ein fertiges System. Kein Prompting, keine Tool-Einarbeitung, keine Konfigurationsarbeit auf deiner Seite.',
  },
  {
    q: 'Was kostet das laufend nach dem Setup?',
    a: 'Starter: €190/Monat. Professional: €390/Monat. Enthalten: Monitoring, monatliches Reporting, Prompt-Anpassungen und direkter Draht zu mir.',
  },
]

export default function FAQ() {
  const [open, setOpen] = useState(null)

  return (
    <section
      id="faq"
      className="section"
      style={{
        background: 'var(--bg-elevated)',
        borderTop: '1px solid var(--border)',
      }}
    >
      <div className="container">
        <div style={{ marginBottom: '3rem', maxWidth: '680px' }}>
          <p className="eyebrow">FAQ</p>
          <h2 className="display-l">
            Häufige Fragen.<br />
            <em style={{ color: 'var(--accent)', fontStyle: 'italic' }}>Ehrliche Antworten.</em>
          </h2>
        </div>

        <dl style={{ maxWidth: '820px', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {items.map((item, i) => (
            <div
              key={i}
              style={{
                background: 'var(--bg)',
                border: open === i ? '1px solid rgba(201, 166, 107, 0.3)' : '1px solid var(--border)',
                borderRadius: 'var(--r-md)',
                overflow: 'hidden',
                transition: 'border-color 0.2s ease',
              }}
            >
              <dt>
                <button
                  type="button"
                  onClick={() => setOpen(open === i ? null : i)}
                  aria-expanded={open === i}
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    gap: '1rem',
                    padding: '1.25rem 1.5rem',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    textAlign: 'left',
                    color: 'var(--text)',
                    fontFamily: 'var(--font-sans)',
                    fontSize: '0.9375rem',
                    fontWeight: 500,
                    lineHeight: 1.45,
                  }}
                >
                  {item.q}
                  <ChevronDown
                    size={18}
                    color="var(--accent)"
                    style={{
                      flexShrink: 0,
                      transform: open === i ? 'rotate(180deg)' : 'rotate(0deg)',
                      transition: 'transform 0.2s ease',
                    }}
                  />
                </button>
              </dt>
              {open === i && (
                <dd style={{
                  padding: '0 1.5rem 1.25rem',
                  color: 'var(--text-muted)',
                  fontSize: '0.9rem',
                  lineHeight: 1.7,
                  margin: 0,
                }}>
                  {item.a}
                </dd>
              )}
            </div>
          ))}
        </dl>
      </div>
    </section>
  )
}
