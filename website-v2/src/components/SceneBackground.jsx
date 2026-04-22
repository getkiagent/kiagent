import { useEffect, useRef } from 'react'

export default function SceneBackground({ opacity = 0.7, particleCount = 90 }) {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext('2d')
    let animId
    let particles = []
    const CONNECT_DIST = 170
    const R = 201, G = 166, B = 107
    const mouse = { x: -9999, y: -9999 }
    const MOUSE_RADIUS = 140

    const onMouseMove = (e) => {
      const rect = canvas.getBoundingClientRect()
      mouse.x = e.clientX - rect.left
      mouse.y = e.clientY - rect.top
    }
    const onMouseLeave = () => { mouse.x = -9999; mouse.y = -9999 }
    canvas.addEventListener('mousemove', onMouseMove)
    canvas.addEventListener('mouseleave', onMouseLeave)

    const resize = () => {
      canvas.width = canvas.offsetWidth
      canvas.height = canvas.offsetHeight
      initParticles()
    }

    const initParticles = () => {
      particles = Array.from({ length: particleCount }, (_, i) => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: (Math.random() - 0.5) * 0.28,
        vy: (Math.random() - 0.5) * 0.28,
        r: i < 8 ? Math.random() * 1.8 + 1.4 : Math.random() * 1.2 + 0.5,
        hub: i < 8,
      }))
    }

    const tick = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      for (const p of particles) {
        // Mouse repulsion
        const mdx = p.x - mouse.x
        const mdy = p.y - mouse.y
        const md = Math.sqrt(mdx * mdx + mdy * mdy)
        if (md < MOUSE_RADIUS && md > 0) {
          const force = (MOUSE_RADIUS - md) / MOUSE_RADIUS * 0.6
          p.vx += (mdx / md) * force
          p.vy += (mdy / md) * force
        }

        // Speed cap
        const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy)
        if (speed > 1.2) { p.vx *= 0.97; p.vy *= 0.97 }

        p.x += p.vx
        p.y += p.vy
        if (p.x < 0 || p.x > canvas.width) p.vx *= -1
        if (p.y < 0 || p.y > canvas.height) p.vy *= -1

        // Draw particle
        if (p.hub) {
          // Glowing hub node
          const grd = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4)
          grd.addColorStop(0, `rgba(${R},${G},${B},0.9)`)
          grd.addColorStop(0.4, `rgba(${R},${G},${B},0.35)`)
          grd.addColorStop(1, `rgba(${R},${G},${B},0)`)
          ctx.beginPath()
          ctx.arc(p.x, p.y, p.r * 4, 0, Math.PI * 2)
          ctx.fillStyle = grd
          ctx.fill()
        }
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
        ctx.fillStyle = `rgba(${R},${G},${B},${p.hub ? 1 : 0.7})`
        ctx.fill()
      }

      // Connections
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x
          const dy = particles[i].y - particles[j].y
          const dist = Math.sqrt(dx * dx + dy * dy)
          if (dist < CONNECT_DIST) {
            const a = (1 - dist / CONNECT_DIST) * (particles[i].hub || particles[j].hub ? 0.55 : 0.28)
            ctx.beginPath()
            ctx.moveTo(particles[i].x, particles[i].y)
            ctx.lineTo(particles[j].x, particles[j].y)
            ctx.strokeStyle = `rgba(${R},${G},${B},${a})`
            ctx.lineWidth = particles[i].hub || particles[j].hub ? 1.1 : 0.7
            ctx.stroke()
          }
        }
      }

      animId = requestAnimationFrame(tick)
    }

    resize()
    tick()

    const ro = new ResizeObserver(resize)
    ro.observe(canvas)

    return () => {
      cancelAnimationFrame(animId)
      ro.disconnect()
      canvas.removeEventListener('mousemove', onMouseMove)
      canvas.removeEventListener('mouseleave', onMouseLeave)
    }
  }, [particleCount])

  return (
    <canvas
      ref={canvasRef}
      aria-hidden="true"
      style={{
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        opacity,
        pointerEvents: 'none',
        zIndex: 0,
      }}
    />
  )
}
