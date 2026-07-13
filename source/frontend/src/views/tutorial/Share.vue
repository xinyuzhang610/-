<template>
  <div class="tutorial-detail">
    <header class="tutorial-header">
      <router-link to="/" class="back-link">← 返回首页</router-link>
      <h1 class="tutorial-title">分享使用教程</h1>
      <p class="tutorial-subtitle">生成分享链接或二维码，让学生轻松使用您创建的教学工具</p>
    </header>

    <div class="tutorial-content">
      <div class="tutorial-hero">
        <div class="hero-visual">
          <div class="visual-step">
            <div class="step-icon">🔧</div>
            <div class="step-text">选择工具</div>
          </div>
          <div class="visual-arrow">→</div>
          <div class="visual-step">
            <div class="step-icon">🔗</div>
            <div class="step-text">生成链接</div>
          </div>
          <div class="visual-arrow">→</div>
          <div class="visual-step">
            <div class="step-icon">📱</div>
            <div class="step-text">分享学生</div>
          </div>
          <div class="visual-arrow">→</div>
          <div class="visual-step">
            <div class="step-icon">📊</div>
            <div class="step-text">查看数据</div>
          </div>
        </div>
      </div>

      <div class="tutorial-info">
        <h2>分享方式</h2>
        <p>智教通提供多种分享方式，让您可以轻松地将教学工具分享给学生：</p>

        <div class="share-methods">
          <div class="method-card">
            <div class="method-icon">🔗</div>
            <h3>分享链接</h3>
            <p>生成唯一的分享链接，学生点击即可使用工具。支持复制链接、生成二维码。</p>
          </div>
          <div class="method-card">
            <div class="method-icon">📱</div>
            <h3>二维码分享</h3>
            <p>生成工具专属二维码，学生扫码即可使用。适合课堂展示、打印材料等场景。</p>
          </div>
          <div class="method-card">
            <div class="method-icon">⚙️</div>
            <h3>权限设置</h3>
            <p>设置工具的使用权限：允许匿名使用、设置有效期、限制使用次数等。</p>
          </div>
        </div>

        <h2>使用场景</h2>
        <div class="scenarios">
          <div class="scenario">
            <h3>📝 课后作业</h3>
            <p>将工具链接发布到班级群，学生点击即可完成作业，系统自动记录使用情况。</p>
          </div>
          <div class="scenario">
            <h3>🎯 课堂互动</h3>
            <p>在课堂上展示二维码，学生扫码参与互动，实时查看学生使用数据。</p>
          </div>
          <div class="scenario">
            <h3>📚 自主学习</h3>
            <p>将工具分享给学生，让他们在课后自主学习，系统记录学习轨迹。</p>
          </div>
        </div>

        <h2>数据看板</h2>
        <p>分享工具后，您可以在数据看板中查看：</p>
        <ul>
          <li>工具使用次数和趋势</li>
          <li>学生使用情况统计</li>
          <li>热门工具排行榜</li>
          <li>最近使用记录</li>
        </ul>

        <div class="cta">
          <router-link to="/register" class="btn-primary">立即注册体验</router-link>
          <router-link to="/login" class="btn-secondary">已有账号登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.tutorial-detail {
  min-height: 100vh;
  background: var(--color-bg);
}

.tutorial-header {
  padding: 24px 32px;
  background: white;
  border-bottom: 1px solid var(--color-chip-bg);
}

.back-link {
  display: inline-block;
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
  text-decoration: none;
  margin-bottom: 16px;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: var(--color-ink);
}

.tutorial-title {
  margin: 0 0 8px;
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 600;
  color: var(--color-ink);
}

.tutorial-subtitle {
  margin: 0;
  font-family: var(--font-sans);
  font-size: 16px;
  color: var(--color-ink-soft);
}

.tutorial-content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 48px 32px;
}

.tutorial-hero {
  margin-bottom: 48px;
}

.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 40px;
  background: white;
  border-radius: 12px;
}

.visual-step {
  text-align: center;
}

.step-icon {
  font-size: 48px;
  margin-bottom: 8px;
}

.step-text {
  font-family: var(--font-sans);
  font-size: 14px;
  font-weight: 500;
  color: var(--color-ink);
}

.visual-arrow {
  font-size: 24px;
  color: var(--color-ink-soft);
}

.tutorial-info h2 {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  color: var(--color-ink);
  margin: 32px 0 16px;
}

.tutorial-info p {
  font-family: var(--font-sans);
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-ink-soft);
  margin-bottom: 16px;
}

.tutorial-info ul {
  list-style: none;
  padding: 0;
  margin-bottom: 24px;
}

.tutorial-info li {
  font-family: var(--font-sans);
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-ink-soft);
  padding-left: 24px;
  position: relative;
  margin-bottom: 8px;
}

.tutorial-info li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: var(--color-ink);
}

.share-methods {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.method-card {
  padding: 24px;
  background: white;
  border-radius: 12px;
  text-align: center;
}

.method-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.method-card h3 {
  margin: 0 0 8px;
  font-family: var(--font-sans);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-ink);
}

.method-card p {
  margin: 0;
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
}

.scenarios {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.scenario {
  padding: 24px;
  background: white;
  border-radius: 12px;
}

.scenario h3 {
  margin: 0 0 8px;
  font-family: var(--font-sans);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-ink);
}

.scenario p {
  margin: 0;
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
}

.cta {
  display: flex;
  gap: 16px;
  margin-top: 40px;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 32px;
  background: var(--color-ink);
  color: #fafafa;
  font-family: var(--font-misans);
  font-size: 16px;
  font-weight: 500;
  border-radius: 46px;
  text-decoration: none;
  transition: background 0.3s ease;
}

.btn-primary:hover {
  background: #3a3933;
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 32px;
  background: transparent;
  color: var(--color-ink);
  font-family: var(--font-misans);
  font-size: 16px;
  font-weight: 500;
  border: 1px solid var(--color-border);
  border-radius: 46px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  border-color: var(--color-ink);
  background: rgba(38, 37, 30, 0.05);
}

@media (max-width: 640px) {
  .tutorial-header {
    padding: 16px 20px;
  }

  .tutorial-title {
    font-size: 28px;
  }

  .tutorial-content {
    padding: 32px 20px;
  }

  .hero-visual {
    flex-direction: column;
    gap: 12px;
  }

  .visual-arrow {
    transform: rotate(90deg);
  }

  .share-methods {
    grid-template-columns: 1fr;
  }

  .cta {
    flex-direction: column;
  }

  .btn-primary, .btn-secondary {
    width: 100%;
  }
}
</style>
