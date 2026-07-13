<template>
  <section class="hero" id="hero">
    <div class="hero__bg" aria-hidden="true"></div>
    <canvas class="hero__mask" ref="heroMask" aria-hidden="true"></canvas>

    <a class="hero__logo-link" href="#" aria-label="智教通">
      <img class="hero__logo" src="../assets/logo-temp.svg" alt="智教通" width="120">
    </a>

    <div class="hero__divider" aria-hidden="true"></div>

    <div class="hero__bar">
      <nav class="hero__nav" aria-label="Main navigation">
        <div class="hero__nav-dropdown">
          <button type="button" class="hero__nav-link hero__nav-dropdown-trigger">
            平台功能
            <svg class="hero__nav-caret" width="1em" height="1em" viewBox="0 0 32 32" aria-hidden="true">
              <path fill="currentColor" d="M16 22 6 12l1.4-1.4 8.6 8.6 8.6-8.6L26 12z"></path>
            </svg>
          </button>
          <div class="hero__nav-menu" role="menu">
            <a class="hero__nav-menu-item" href="#features" role="menuitem">核心功能</a>
            <a class="hero__nav-menu-item" href="#tutorials" role="menuitem">使用教程</a>
            <a class="hero__nav-menu-item" href="#cases" role="menuitem">案例展示</a>
          </div>
        </div>
        <a class="hero__nav-link" href="#">文档</a>
        <a class="hero__nav-link" href="#">关于我们</a>
      </nav>

      <div class="hero__lang hero__nav-dropdown">
        <button type="button" class="hero__lang-trigger hero__nav-dropdown-trigger" aria-label="Language">
          <img class="hero__lang-icon" src="../assets/icon-translate.svg" alt="">
          <svg class="hero__nav-caret" width="1em" height="1em" viewBox="0 0 32 32" aria-hidden="true">
            <path fill="currentColor" d="M16 22 6 12l1.4-1.4 8.6 8.6 8.6-8.6L26 12z"></path>
          </svg>
        </button>
        <div class="hero__nav-menu hero__lang-menu" role="menu">
          <button type="button" class="hero__nav-menu-item hero__lang-option is-active" role="menuitem">简体中文</button>
          <button type="button" class="hero__nav-menu-item hero__lang-option" role="menuitem">English</button>
        </div>
      </div>
    </div>

    <div class="hero__content">
      <div class="hero__heading">
        <h1 class="hero__title">智教通</h1>
        <p class="hero__subtitle" ref="heroSubtitle"></p>
      </div>

      <div class="install">
        <router-link class="btn btn--primary" to="/login">
          开始体验
          <svg class="btn__arrow" viewBox="0 0 16 16" fill="none" aria-hidden="true" focusable="false">
            <path d="M6.3333 3.66665H12.3333V9.66665" stroke="currentColor" stroke-width="1.33333" stroke-linecap="round" stroke-linejoin="round"></path>
            <path d="M3.848 12.152L12.3333 3.66665" stroke="currentColor" stroke-width="1.33333" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </router-link>
      </div>

      <div class="ctas">
        <a class="btn" href="https://github.com/xinyuzhang610/-" target="_blank" rel="noreferrer noopener">
          GitHub
          <svg class="btn__arrow" viewBox="0 0 16 16" fill="none" aria-hidden="true" focusable="false">
            <path d="M6.3333 3.66665H12.3333V9.66665" stroke="currentColor" stroke-width="1.33333" stroke-linecap="round" stroke-linejoin="round"></path>
            <path d="M3.848 12.152L12.3333 3.66665" stroke="currentColor" stroke-width="1.33333" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </a>
        <a class="btn" href="#">
          查看文档
          <svg class="btn__arrow" viewBox="0 0 16 16" fill="none" aria-hidden="true" focusable="false">
            <path d="M6.3333 3.66665H12.3333V9.66665" stroke="currentColor" stroke-width="1.33333" stroke-linecap="round" stroke-linejoin="round"></path>
            <path d="M3.848 12.152L12.3333 3.66665" stroke="currentColor" stroke-width="1.33333" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </a>
        <a class="btn" href="#">
          了解更多
          <svg class="btn__arrow" viewBox="0 0 16 16" fill="none" aria-hidden="true" focusable="false">
            <path d="M6.3333 3.66665H12.3333V9.66665" stroke="currentColor" stroke-width="1.33333" stroke-linecap="round" stroke-linejoin="round"></path>
            <path d="M3.848 12.152L12.3333 3.66665" stroke="currentColor" stroke-width="1.33333" stroke-linecap="round" stroke-linejoin="round"></path>
          </svg>
        </a>
      </div>
    </div>
  </section>

  <section class="features" id="features">
    <canvas class="section-canvas" data-section="features"></canvas>
    <h2 class="features__title">为什么选择智教通</h2>
    <div class="features__list">
      <router-link to="/feature/discover" class="card card--1">
        <div class="card__painting"><img src="../assets/feature-discover.svg" alt=""></div>
        <div class="card__text">
          <h3>智能教学需求发现</h3>
          <p>AI自动分析教学场景，精准识别教师需求，为每位教育工作者量身定制解决方案。</p>
        </div>
      </router-link>

      <router-link to="/feature/agent" class="card card--2">
        <div class="card__text">
          <h3>AI代理工具体验</h3>
          <p>集成多种AI代理工具，支持智能备课、作业批改、学情分析，让教学更高效。</p>
        </div>
        <div class="card__painting"><img src="../assets/feature-agent.svg" alt=""></div>
      </router-link>

      <router-link to="/feature/resource" class="card card--3">
        <div class="card__painting"><img src="../assets/feature-resource.svg" alt=""></div>
        <div class="card__text">
          <h3>海量教学资源库</h3>
          <p>整合优质教学资源，智能推荐适配内容，覆盖各学科各年级，备课从此轻松简单。</p>
        </div>
      </router-link>

      <router-link to="/feature/path" class="card card--4">
        <div class="card__text">
          <h3>个性化学习路径</h3>
          <p>基于学生画像和学习数据，智能规划个性化学习路径，因材施教，助力每一位学生成长。</p>
        </div>
        <div class="card__painting"><img src="../assets/feature-path.svg" alt=""></div>
      </router-link>

      <router-link to="/feature/analysis" class="card card--5">
        <div class="card__painting"><img src="../assets/feature-analysis.svg" alt=""></div>
        <div class="card__text">
          <h3>精准学情分析</h3>
          <p>实时追踪学习进度，多维度分析学情数据，让教学决策有据可依，让学习效果可视化。</p>
        </div>
      </router-link>
    </div>
  </section>

  <!-- 使用教程 -->
  <section class="tutorials" id="tutorials">
    <canvas class="section-canvas" data-section="tutorials"></canvas>
    <h2 class="section-title">使用教程</h2>
    <div class="tutorials-grid">
      <router-link to="/register" class="tutorial-card">
        <div class="tutorial-step">1</div>
        <h3 class="tutorial-title">注册登录</h3>
        <p class="tutorial-desc">创建账号并登录平台，完善个人信息和教学科目</p>
        <span class="tutorial-link">立即注册 →</span>
      </router-link>
      <router-link to="/tutorial/guide" class="tutorial-card">
        <div class="tutorial-step">2</div>
        <h3 class="tutorial-title">需求引导</h3>
        <p class="tutorial-desc">通过智能引导，发现您的教学需求，系统为您推荐合适工具</p>
        <span class="tutorial-link">了解详情 →</span>
      </router-link>
      <router-link to="/student/plaza" class="tutorial-card">
        <div class="tutorial-step">3</div>
        <h3 class="tutorial-title">体验工具</h3>
        <p class="tutorial-desc">选择推荐工具或浏览工具广场，体验AI辅助教学的便捷</p>
        <span class="tutorial-link">进入广场 →</span>
      </router-link>
      <router-link to="/tutorial/share" class="tutorial-card">
        <div class="tutorial-step">4</div>
        <h3 class="tutorial-title">分享使用</h3>
        <p class="tutorial-desc">生成分享链接或二维码，让学生轻松使用您创建的教学工具</p>
        <span class="tutorial-link">学习分享 →</span>
      </router-link>
    </div>
  </section>

  <!-- 案例展示 -->
  <section class="cases" id="cases">
    <canvas class="section-canvas" data-section="cases"></canvas>
    <h2 class="section-title">案例展示</h2>
    <div class="cases-grid">
      <router-link to="/tool/1" class="case-card">
        <div class="case-icon">🏮</div>
        <h3 class="case-title">古诗词趣味赏析</h3>
        <p class="case-subject">语文 · 文科</p>
        <p class="case-desc">输入诗词名，获得趣味化赏析、背景知识和知识卡片，让古诗词学习更生动</p>
        <span class="case-link">立即体验 →</span>
      </router-link>
      <router-link to="/tool/7" class="case-card">
        <div class="case-icon">🧮</div>
        <h3 class="case-title">公式推导助手</h3>
        <p class="case-subject">数学 · 理科</p>
        <p class="case-desc">输入公式名称，获得详细的推导过程和几何直觉解释，让数学公式不再难懂</p>
        <span class="case-link">立即体验 →</span>
      </router-link>
      <router-link to="/tool/2" class="case-card">
        <div class="case-icon">✍️</div>
        <h3 class="case-title">作文灵感助手</h3>
        <p class="case-subject">语文 · 文科</p>
        <p class="case-desc">输入作文题目或主题，获得写作思路、素材建议和结构框架，激发创作灵感</p>
        <span class="case-link">立即体验 →</span>
      </router-link>
    </div>
  </section>

  <footer class="footer">
    <div class="footer__inner">
      <span>© 2026 智教通</span>
      <span class="footer__sep">·</span>
      <a class="footer__link" href="#">隐私政策</a>
      <span class="footer__sep">·</span>
      <a class="footer__link" href="#">使用条款</a>
      <span class="footer__sep">·</span>
      <a class="footer__link" href="#">联系我们</a>
    </div>
  </footer>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const heroMask = ref(null)
const heroSubtitle = ref(null)

// 墨水揭示效果
let animationId = null

const initInkEffect = () => {
  const hero = document.getElementById('hero')
  const canvas = heroMask.value
  if (!hero || !canvas) return

  const canHover = window.matchMedia('(hover: hover)').matches
  if (!canHover) return

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const MASK = '252, 250, 248'
  const R_START = 8
  const R_END = 128
  const R_VARY = 0.45
  const LIFETIME = 520
  const STAMP_STEP = 12
  const MAX_STAMPS = 160
  const DPR = Math.min(window.devicePixelRatio || 1, 2)

  let w = 0, h = 0
  function resize() {
    const rect = hero.getBoundingClientRect()
    w = rect.width
    h = rect.height
    canvas.width = Math.round(w * DPR)
    canvas.height = Math.round(h * DPR)
    canvas.style.width = w + 'px'
    canvas.style.height = h + 'px'
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0)
    ctx.globalCompositeOperation = 'source-over'
    ctx.fillStyle = `rgb(${MASK})`
    ctx.fillRect(0, 0, w, h)
  }
  resize()
  window.addEventListener('resize', resize)

  let stamps = []
  let lastX = null, lastY = null

  function addStamp(x, y) {
    if (stamps.length >= MAX_STAMPS) stamps.shift()
    stamps.push({
      x, y,
      born: performance.now(),
      seed: Math.random() * Math.PI * 2,
      rmax: R_END * (1 - R_VARY + Math.random() * R_VARY)
    })
  }

  function stampAlong(x, y) {
    if (lastX === null) {
      addStamp(x, y)
    } else {
      const dx = x - lastX, dy = y - lastY
      const dist = Math.hypot(dx, dy)
      const steps = Math.max(1, Math.ceil(dist / STAMP_STEP))
      for (let i = 1; i <= steps; i++) {
        addStamp(lastX + (dx * i) / steps, lastY + (dy * i) / steps)
      }
    }
    lastX = x
    lastY = y
  }

  function carveInk(x, y, r, alpha, seed) {
    const g = ctx.createRadialGradient(x, y, r * 0.25, x, y, r)
    g.addColorStop(0, `rgba(0, 0, 0, ${0.95 * alpha})`)
    g.addColorStop(0.55, `rgba(0, 0, 0, ${0.88 * alpha})`)
    g.addColorStop(1, 'rgba(0, 0, 0, 0)')
    ctx.fillStyle = g
    ctx.beginPath()
    const segs = 32
    for (let i = 0; i <= segs; i++) {
      const a = (i / segs) * Math.PI * 2
      const wob = 0.78 + 0.14 * Math.sin(a * 3 + seed) + 0.08 * Math.sin(a * 7 + seed * 2.1) + 0.05 * Math.sin(a * 13 + seed * 0.7)
      const rr = r * wob
      const px = x + Math.cos(a) * rr
      const py = y + Math.sin(a) * rr
      if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py)
    }
    ctx.closePath()
    ctx.fill()
  }

  let running = false
  function loop() {
    const now = performance.now()
    ctx.globalCompositeOperation = 'source-over'
    ctx.fillStyle = `rgb(${MASK})`
    ctx.fillRect(0, 0, w, h)

    ctx.globalCompositeOperation = 'destination-out'
    for (let i = stamps.length - 1; i >= 0; i--) {
      const t = (now - stamps[i].born) / LIFETIME
      if (t >= 1) { stamps.splice(i, 1); continue }
      const ease = 1 - Math.pow(1 - t, 3)
      const r = R_START + (stamps[i].rmax - R_START) * ease
      const alpha = 1 - t * t
      carveInk(stamps[i].x, stamps[i].y, r, alpha, stamps[i].seed)
    }

    if (stamps.length) {
      animationId = requestAnimationFrame(loop)
    } else {
      running = false
    }
  }

  function start() {
    if (!running) { running = true; animationId = requestAnimationFrame(loop) }
  }

  hero.addEventListener('mouseenter', (e) => {
    const rect = hero.getBoundingClientRect()
    lastX = e.clientX - rect.left
    lastY = e.clientY - rect.top
    stampAlong(lastX, lastY)
    start()
  })
  hero.addEventListener('mousemove', (e) => {
    const rect = hero.getBoundingClientRect()
    stampAlong(e.clientX - rect.left, e.clientY - rect.top)
    start()
  })
  hero.addEventListener('mouseleave', () => { lastX = null; lastY = null })
}

// 平滑滚动
const initSmoothScroll = () => {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (e) => {
      const href = anchor.getAttribute('href')
      if (href === '#') return
      const target = document.querySelector(href)
      if (target) {
        e.preventDefault()
        target.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    })
  })
}

// 卡片标题打字机效果
const initTypewriter = () => {
  const titles = document.querySelectorAll('.card__text h3')
  if (!titles.length || !('IntersectionObserver' in window)) return
  const CHAR_DELAY = 130

  titles.forEach((h3) => {
    const text = h3.textContent
    h3.textContent = ''
    for (let ci = 0; ci < text.length; ci++) {
      const span = document.createElement('span')
      span.className = 'char'
      span.textContent = text[ci]
      h3.appendChild(span)
    }
    const cursor = document.createElement('span')
    cursor.className = 'cursor'
    cursor.setAttribute('aria-hidden', 'true')
    h3.appendChild(cursor)
  })

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const h3 = entry.target
        const chars = h3.querySelectorAll('.char')
        const cursor = h3.querySelector('.cursor')
        h3.classList.add('is-active')
        chars.forEach((char, i) => {
          setTimeout(() => {
            char.classList.add('is-typed')
          }, i * CHAR_DELAY)
        })
        setTimeout(() => {
          h3.classList.remove('is-active')
          h3.classList.add('is-done')
        }, chars.length * CHAR_DELAY + 300)
        observer.unobserve(h3)
      }
    })
  }, { threshold: 0.5 })

  titles.forEach((h3) => observer.observe(h3))
}

// 打字机效果（副标题）
const initSubtitleTypewriter = () => {
  const text = '帮助教师发现教学需求，体验AI工具，提升教学效率'
  let index = 0

  const typeWriter = () => {
    if (index < text.length && heroSubtitle.value) {
      heroSubtitle.value.textContent = text.substring(0, index + 1)
      index++
      setTimeout(typeWriter, 100)
    }
  }

  setTimeout(typeWriter, 500)
}

// 区域墨水效果（画水墨，不是挖掉）
const initSectionInkEffects = () => {
  const canvases = document.querySelectorAll('.section-canvas')
  const canHover = window.matchMedia('(hover: hover)').matches
  if (!canHover) return

  canvases.forEach((canvas) => {
    const section = canvas.parentElement
    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const R_START = 8
    const R_END = 100
    const R_VARY = 0.45
    const LIFETIME = 800
    const STAMP_STEP = 10
    const MAX_STAMPS = 150
    const DPR = Math.min(window.devicePixelRatio || 1, 2)

    // 水墨颜色
    const INK_R = 38, INK_G = 35, INK_B = 28

    let w = 0, h = 0
    function resize() {
      const rect = section.getBoundingClientRect()
      w = rect.width
      h = rect.height
      canvas.width = Math.round(w * DPR)
      canvas.height = Math.round(h * DPR)
      canvas.style.width = w + 'px'
      canvas.style.height = h + 'px'
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0)
    }
    resize()
    window.addEventListener('resize', resize)

    let stamps = []
    let lastX = null, lastY = null

    function addStamp(x, y) {
      if (stamps.length >= MAX_STAMPS) stamps.shift()
      stamps.push({
        x, y,
        born: performance.now(),
        seed: Math.random() * Math.PI * 2,
        rmax: R_END * (1 - R_VARY + Math.random() * R_VARY)
      })
    }

    function stampAlong(x, y) {
      if (lastX === null) {
        addStamp(x, y)
      } else {
        const dx = x - lastX, dy = y - lastY
        const dist = Math.hypot(dx, dy)
        const steps = Math.max(1, Math.ceil(dist / STAMP_STEP))
        for (let i = 1; i <= steps; i++) {
          addStamp(lastX + (dx * i) / steps, lastY + (dy * i) / steps)
        }
      }
      lastX = x
      lastY = y
    }

    function drawInk(x, y, r, alpha, seed) {
      // 外层：淡墨（大面积扩散）
      const g1 = ctx.createRadialGradient(x, y, 0, x, y, r)
      g1.addColorStop(0, `rgba(${INK_R}, ${INK_G}, ${INK_B}, ${0.12 * alpha})`)
      g1.addColorStop(0.2, `rgba(${INK_R}, ${INK_G}, ${INK_B}, ${0.08 * alpha})`)
      g1.addColorStop(0.5, `rgba(${INK_R}, ${INK_G}, ${INK_B}, ${0.03 * alpha})`)
      g1.addColorStop(1, `rgba(${INK_R}, ${INK_G}, ${INK_B}, 0)`)

      ctx.fillStyle = g1
      ctx.beginPath()
      const segs = 32
      for (let i = 0; i <= segs; i++) {
        const a = (i / segs) * Math.PI * 2
        const wob = 0.78 + 0.14 * Math.sin(a * 3 + seed) + 0.08 * Math.sin(a * 7 + seed * 2.1) + 0.05 * Math.sin(a * 13 + seed * 0.7)
        const rr = r * wob
        const px = x + Math.cos(a) * rr
        const py = y + Math.sin(a) * rr
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py)
      }
      ctx.closePath()
      ctx.fill()

      // 中层：中墨
      const g2 = ctx.createRadialGradient(x, y, 0, x, y, r * 0.5)
      g2.addColorStop(0, `rgba(${INK_R}, ${INK_G}, ${INK_B}, ${0.25 * alpha})`)
      g2.addColorStop(0.3, `rgba(${INK_R}, ${INK_G}, ${INK_B}, ${0.15 * alpha})`)
      g2.addColorStop(0.7, `rgba(${INK_R}, ${INK_G}, ${INK_B}, ${0.05 * alpha})`)
      g2.addColorStop(1, `rgba(${INK_R}, ${INK_G}, ${INK_B}, 0)`)

      ctx.fillStyle = g2
      ctx.beginPath()
      for (let i = 0; i <= segs; i++) {
        const a = (i / segs) * Math.PI * 2
        const wob = 0.78 + 0.14 * Math.sin(a * 3 + seed) + 0.08 * Math.sin(a * 7 + seed * 2.1) + 0.05 * Math.sin(a * 13 + seed * 0.7)
        const rr = r * 0.5 * wob
        const px = x + Math.cos(a) * rr
        const py = y + Math.sin(a) * rr
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py)
      }
      ctx.closePath()
      ctx.fill()

      // 内层：浓墨（中心集中）
      const g3 = ctx.createRadialGradient(x, y, 0, x, y, r * 0.25)
      g3.addColorStop(0, `rgba(${INK_R}, ${INK_G}, ${INK_B}, ${0.5 * alpha})`)
      g3.addColorStop(0.4, `rgba(${INK_R}, ${INK_G}, ${INK_B}, ${0.3 * alpha})`)
      g3.addColorStop(1, `rgba(${INK_R}, ${INK_G}, ${INK_B}, 0)`)

      ctx.fillStyle = g3
      ctx.beginPath()
      for (let i = 0; i <= segs; i++) {
        const a = (i / segs) * Math.PI * 2
        const wob = 0.78 + 0.14 * Math.sin(a * 3 + seed) + 0.08 * Math.sin(a * 7 + seed * 2.1) + 0.05 * Math.sin(a * 13 + seed * 0.7)
        const rr = r * 0.25 * wob
        const px = x + Math.cos(a) * rr
        const py = y + Math.sin(a) * rr
        if (i === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py)
      }
      ctx.closePath()
      ctx.fill()
    }

    let running = false
    function loop() {
      const now = performance.now()
      ctx.clearRect(0, 0, w, h)

      for (let i = stamps.length - 1; i >= 0; i--) {
        const t = (now - stamps[i].born) / LIFETIME
        if (t >= 1) { stamps.splice(i, 1); continue }
        const ease = 1 - Math.pow(1 - t, 3)
        const r = R_START + (stamps[i].rmax - R_START) * ease
        const alpha = 1 - t * t
        drawInk(stamps[i].x, stamps[i].y, r, alpha, stamps[i].seed)
      }

      if (stamps.length) {
        requestAnimationFrame(loop)
      } else {
        running = false
      }
    }

    function start() {
      if (!running) { running = true; requestAnimationFrame(loop) }
    }

    section.addEventListener('mouseenter', (e) => {
      const rect = section.getBoundingClientRect()
      lastX = e.clientX - rect.left
      lastY = e.clientY - rect.top
      stampAlong(lastX, lastY)
      start()
    })
    section.addEventListener('mousemove', (e) => {
      const rect = section.getBoundingClientRect()
      stampAlong(e.clientX - rect.left, e.clientY - rect.top)
      start()
    })
    section.addEventListener('mouseleave', () => { lastX = null; lastY = null })
  })
}

onMounted(() => {
  initInkEffect()
  initSmoothScroll()
  initTypewriter()
  initSubtitleTypewriter()
  initSectionInkEffects()
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})
</script>

<style scoped>
/* ── Hero ─────────────────────────────────────────── */
.hero {
  position: relative;
  height: 592px;
  overflow: hidden;
  isolation: isolate;
}

.hero__bg {
  position: absolute;
  inset: 0;
  background-image: url("../assets/hero-bg.png");
  background-size: 1440px 592px;
  background-position: bottom center;
  background-repeat: no-repeat;
  z-index: 0;
}

.hero__mask {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  display: block;
}

.hero__logo-link {
  position: absolute;
  top: 23px;
  left: 32px;
  width: 141px;
  height: 18px;
  z-index: 3;
  display: block;
}

.hero__logo {
  display: block;
  width: 100%;
  height: 100%;
}

.hero__divider {
  position: absolute;
  top: 65px;
  left: 0;
  right: 0;
  height: 1px;
  background: #f3f0ef;
  z-index: 3;
}

.hero__bar {
  position: absolute;
  top: 24px;
  right: 25px;
  height: 15.32px;
  z-index: 4;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.hero__lang {
  position: relative;
  display: inline-flex;
  align-items: center;
  color: var(--color-ink);
}

.hero__lang-trigger { gap: 5px; }

.hero__lang-icon {
  width: 18px;
  height: 18px;
  display: block;
}

.hero__lang-menu {
  min-width: 132px;
  left: auto;
  right: 0;
  transform: translateY(6px);
}

.hero__lang.hero__nav-dropdown:hover .hero__lang-menu,
.hero__lang.hero__nav-dropdown:focus-within .hero__lang-menu {
  transform: translateY(2px);
}

.hero__lang-option {
  width: 100%;
  text-align: left;
  background: transparent;
  border: none;
  cursor: pointer;
}

.hero__lang-option.is-active { background: rgba(0, 0, 0, 0.06); }

.hero__nav {
  display: inline-flex;
  align-items: center;
  gap: 0;
}

.hero__nav-dropdown-trigger {
  padding: 8px 12px;
  margin: 0 6px;
  background: transparent;
  border: none;
  cursor: pointer;
}

.hero__nav-link {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0 6px;
  padding: 8px 12px;
  background: transparent;
  border: none;
  color: #000;
  font-family: var(--font-misans);
  font-size: 15px;
  font-weight: 500;
  line-height: 1;
  text-decoration: none;
  cursor: pointer;
  white-space: nowrap;
}

.hero__nav-link::after {
  content: "";
  position: absolute;
  left: 4px; right: 4px; bottom: 0;
  height: 2.5px;
  background: #000;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.hero__nav-link:hover::after,
.hero__lang:hover .hero__lang-trigger::after {
  transform: scaleX(1);
}

.hero__lang-trigger {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.hero__lang-trigger::after {
  content: "";
  position: absolute;
  left: 4px; right: 4px; bottom: -2px;
  height: 2.5px;
  background: #000;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.hero__nav-caret {
  width: 16px;
  height: 16px;
  color: currentColor;
}

.hero__nav-dropdown {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.hero__nav-menu {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%) translateY(6px);
  min-width: 160px;
  display: flex;
  flex-direction: column;
  padding: 12px 8px;
  background: #fff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transition: opacity 0.3s ease, transform 0.3s ease, visibility 0.3s;
  z-index: 10;
}

.hero__nav-dropdown:hover .hero__nav-menu,
.hero__nav-dropdown:focus-within .hero__nav-menu {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
  transform: translateX(-50%) translateY(2px);
}

.hero__nav-menu-item {
  display: block;
  padding: 8px 14px;
  border-radius: 8px;
  color: #000;
  font-family: var(--font-misans);
  font-size: 15px;
  font-weight: 400;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.15s ease;
}

.hero__nav-menu-item:hover { background: rgba(0, 0, 0, 0.06); }

.hero__content {
  position: relative;
  z-index: 2;
  max-width: 809px;
  margin: 0 auto;
  padding-top: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 40px;
}

.hero__heading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  text-align: center;
  width: 100%;
}

.hero__title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 50px;
  font-weight: 400;
  letter-spacing: 0.4px;
  color: var(--color-ink);
}

.hero__subtitle {
  margin: 0;
  font-family: var(--font-mincho);
  font-size: 22px;
  font-weight: 500;
  letter-spacing: 0.4px;
  line-height: 1.5;
  color: var(--color-ink);
  white-space: nowrap;
  max-width: min(940px, 94vw);
}

.hero__subtitle .type-caret {
  display: inline-block;
  width: 2px;
  height: 1.05em;
  margin-left: 2px;
  background: currentColor;
  vertical-align: -0.18em;
  animation: sub-caret 0.75s step-end infinite;
}
@keyframes sub-caret { 50% { opacity: 0; } }

.install {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.ctas {
  display: flex;
  gap: 20px;
  align-items: center;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  min-width: 130px;
  padding: 10px 41px;
  border-radius: 46px;
  font-family: var(--font-misans);
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.24px;
  text-decoration: none;
  cursor: pointer;
  background: transparent;
  color: var(--color-ink);
  border: 1px solid var(--color-border);
  transition: transform 200ms ease, background-color 200ms ease, color 200ms ease, border-color 200ms ease;
  white-space: nowrap;
}

.btn:hover {
  background: var(--color-ink);
  color: #fafafa;
  border-color: var(--color-ink);
  transform: translateY(-1px);
}

.btn--primary {
  background: var(--color-ink);
  color: #fafafa;
  border-color: var(--color-ink);
}

.btn--primary:hover { background: #3a3933; border-color: #3a3933; }

.btn__arrow {
  width: 16px; height: 16px;
  flex-shrink: 0;
  opacity: 0;
  margin-left: -16px;
  transition: opacity 200ms ease, margin-left 200ms ease;
}

.btn:hover .btn__arrow, .btn--primary .btn__arrow {
  opacity: 1;
  margin-left: 10px;
}

/* ── Section Canvas ─────────────────────────────────── */
.section-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

/* ── Features ─────────────────────────────────────── */
.features {
  padding: 40px 0 60px;
  background: var(--color-bg);
  position: relative;
  overflow: hidden;
}

.features__title {
  margin: 0 0 35px;
  text-align: center;
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 500;
  letter-spacing: 0.4px;
  color: var(--color-ink);
  position: relative;
  z-index: 1;
}

.features__list {
  display: flex;
  flex-direction: column;
  gap: 43px;
  width: 1100px;
  max-width: calc(100% - 80px);
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.card {
  position: relative;
  width: 100%;
  height: 360px;
  border-radius: 4px;
  overflow: hidden;
}

.card__painting {
  position: absolute;
  overflow: hidden;
}

.card__painting img {
  width: 100%; height: 100%;
  object-fit: cover;
  display: block;
  pointer-events: none;
}

.card__text {
  position: absolute;
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 331px;
  letter-spacing: 0;
}

.card__text h3 {
  margin: 0;
  font-family: var(--font-mincho);
  font-size: 22px;
  font-weight: 500;
  line-height: 1.447;
  color: var(--color-ink);
}

.card__text h3 .char { display: none; white-space: pre; }
.card__text h3 .char.is-typed { display: inline-block; }
.card__text h3 .cursor {
  display: inline-block;
  width: 2px; height: 18px;
  background: currentColor;
  vertical-align: middle;
  margin-left: 3px; margin-bottom: 2px;
  opacity: 0;
  transition: opacity 180ms ease;
}
.card__text h3.is-active .cursor { opacity: 1; }
.card__text h3.is-done .cursor { animation: cursor-blink 1s steps(2, end) infinite; }
@keyframes cursor-blink { 0%, 49% { opacity: 1; } 50%, 100% { opacity: 0; } }

.card__text p {
  margin: 0;
  font-family: var(--font-misans);
  font-size: 16px;
  font-weight: 300;
  line-height: 1.447;
  color: var(--color-ink-soft);
}

.card--1 { background: #efebe3; }
.card--1 .card__painting { left: 0; top: 0; width: 573px; height: 360px; }
.card--1 .card__text { left: 648px; top: 136px; }

.card--2 { background: #f6f1ea; }
.card--2 .card__text { left: 129px; top: 130px; }
.card--2 .card__painting { left: 527px; top: 0; width: 573px; height: 360px; }

.card--3 { background: #efe8e3; }
.card--3 .card__painting { left: 0; top: 0; width: 573px; height: 360px; }
.card--3 .card__text { left: 645px; top: 114px; }

.card--4 { background: #fbf2e9; }
.card--4 .card__text { left: 122px; top: 107px; }
.card--4 .card__painting { left: 527px; top: 0; width: 573px; height: 360px; }

.card--5 { background: #f5ede7; }
.card--5 .card__painting { left: 0; top: 0; width: 660px; height: 360px; }
.card--5 .card__text { left: 670px; top: 112px; }

/* 卡片链接样式 */
a.card {
  text-decoration: none;
  color: inherit;
  display: block;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

a.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15);
}

/* ── Tutorials ─────────────────────────────────────── */
.tutorials {
  padding: 80px 32px;
  background: white;
  position: relative;
  overflow: hidden;
}

.section-title {
  margin: 0 0 48px;
  text-align: center;
  font-family: var(--font-display);
  font-size: 30px;
  font-weight: 500;
  letter-spacing: 0.4px;
  color: var(--color-ink);
  position: relative;
  z-index: 1;
}

.tutorials-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  max-width: 1100px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.tutorial-card {
  padding: 32px 24px;
  background: var(--color-bg);
  border-radius: 12px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  color: inherit;
  display: block;
}

.tutorial-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.tutorial-link {
  display: inline-block;
  margin-top: 12px;
  font-family: var(--font-misans);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-ink);
  text-decoration: underline;
  text-underline-offset: 3px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.tutorial-card:hover .tutorial-link {
  opacity: 1;
}

.tutorial-step {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  background: var(--color-ink);
  color: #fafafa;
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  border-radius: 50%;
}

.tutorial-title {
  margin: 0 0 8px;
  font-family: var(--font-sans);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-ink);
}

.tutorial-desc {
  margin: 0;
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-ink-soft);
}

/* ── Cases ─────────────────────────────────────────── */
.cases {
  padding: 80px 32px;
  background: var(--color-bg);
  position: relative;
  overflow: hidden;
}

.cases-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1100px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.case-card {
  padding: 32px 24px;
  background: white;
  border-radius: 12px;
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none;
  color: inherit;
  display: block;
}

.case-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.case-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.case-title {
  margin: 0 0 8px;
  font-family: var(--font-sans);
  font-size: 20px;
  font-weight: 600;
  color: var(--color-ink);
}

.case-subject {
  margin: 0 0 12px;
  font-family: var(--font-sans);
  font-size: 13px;
  color: var(--color-ink-soft);
}

.case-desc {
  margin: 0 0 20px;
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.6;
  color: var(--color-ink-soft);
}

.case-link {
  display: inline-block;
  font-family: var(--font-misans);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-ink);
  text-decoration: underline;
  text-underline-offset: 3px;
  transition: color 0.3s ease;
}

.case-link:hover {
  color: #3a3933;
}

/* ── Footer ─────────────────────────────────────────── */
.footer {
  background: #f5f4ef;
  min-height: 290px;
  padding: 40px 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer__inner {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 6px 6px;
  font-size: 12px;
  font-weight: 400;
  letter-spacing: 0.8px;
  color: #504f49;
  text-align: center;
}

.footer__sep { color: #b1b1b1; user-select: none; }

.footer__link {
  color: inherit;
  text-decoration: underline;
  text-underline-offset: 3px;
  text-decoration-thickness: 0.5px;
  transition: color 200ms ease;
}

.footer__link:hover { color: var(--color-ink); }

/* ── Mobile ────────────────────────────────────────── */
@media (max-width: 640px) {
  .hero { height: 425px; }
  .hero__logo-link { top: 33px; left: 20px; width: 109px; height: 14px; }
  .hero__divider { top: 66px; }
  .hero__bar { top: 29px; right: 19px; gap: 0; }
  .hero__nav { display: none; }
  .hero__lang-icon { width: 18px; height: 18px; }
  .hero__bg { top: 67px; bottom: auto; height: 218px; }
  .hero__mask { display: none; }
  .hero__content {
    padding-top: 129px; gap: 0;
    max-width: none; padding-left: 20px; padding-right: 20px;
  }
  .hero__heading { gap: 19px; }
  .hero__title { font-size: 30px; }
  .hero__subtitle { font-size: 14px; line-height: 1.6; white-space: normal; }
  .install { width: 100%; margin-top: 54px; gap: 12px; }
  .ctas { width: 100%; max-width: 300px; gap: 13px; margin-top: 20px; }
  .btn { flex: 1; height: 33px; min-width: 0; padding: 0 12px; font-size: 14px; }
  .btn__arrow { width: 12px; height: 12px; }
  .features { padding: 30px 0 50px; }
  .features__title { font-size: 22px; margin: 0 20px 35px; }
  .features__list { width: auto; max-width: none; margin: 0 20px; gap: 30px; }
  .card, .card--1, .card--2, .card--3, .card--4, .card--5 {
    height: auto; padding: 6px 6px 26px;
    display: flex; flex-direction: column;
  }
  .card__painting { order: 1; }
  .card__text { order: 2; }
  .card__painting,
  .card--1 .card__painting, .card--2 .card__painting, .card--3 .card__painting,
  .card--4 .card__painting, .card--5 .card__painting {
    position: relative; left: auto; top: auto; right: auto; bottom: auto;
    width: 100%; height: 202px;
  }
  .card__text,
  .card--1 .card__text, .card--2 .card__text, .card--3 .card__text,
  .card--4 .card__text, .card--5 .card__text {
    position: static; width: auto; margin: 26px 20px 0; left: auto; top: auto;
  }
  .card__text h3 { font-size: 18px; }
  .card__text p { font-size: 14px; }
  .footer { min-height: 217px; padding: 36px 36px; }
  .footer__inner { font-size: 9px; letter-spacing: 0.3px; gap: 5px 5px; }

  /* 教程和案例区域移动端 */
  .tutorials { padding: 50px 20px; }
  .section-title { font-size: 22px; margin-bottom: 35px; }
  .tutorials-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
  .tutorial-card { padding: 20px 16px; }
  .tutorial-step { width: 40px; height: 40px; font-size: 20px; }
  .tutorial-title { font-size: 15px; }
  .tutorial-desc { font-size: 13px; }

  .cases { padding: 50px 20px; }
  .cases-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  .case-card { padding: 24px 20px; }
}
</style>
