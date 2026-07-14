<template>
  <div class="feature-detail">
    <header class="feature-header">
      <router-link to="/" class="back-link">← 返回首页</router-link>
      <h1 class="feature-title">智能教学需求发现</h1>
      <p class="feature-subtitle">AI自动分析教学场景，精准识别教师需求</p>
    </header>

    <div class="feature-content">
      <div class="feature-hero">
        <img src="../../assets/feature-discover.svg" alt="智能教学需求发现" class="feature-image">
      </div>

      <div class="feature-info">
        <h2>功能介绍</h2>
        <p>智教通的核心创新点在于"需求引导"——帮助"小白"用户学会发现需求、理解需求、满足需求。</p>
        <p>通过智能引导流程，系统能够：</p>
        <ul>
          <li>分析教师的教学科目、年级和教学场景</li>
          <li>识别教师在备课、课堂教学、课后辅导等环节的需求</li>
          <li>推荐最适合的教学工具和资源</li>
          <li>引导教师逐步探索和使用AI工具</li>
        </ul>

        <h2>使用流程</h2>
        <div class="steps">
          <div class="step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h3>文理分科</h3>
              <p>选择您的教学方向（文科/理科），缩小推荐范围</p>
            </div>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h3>需求引导</h3>
              <p>通过问答形式，帮助您发现真实的教学需求</p>
            </div>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h3>工具推荐</h3>
              <p>根据您的需求，智能推荐最合适的教学工具</p>
            </div>
          </div>
          <div class="step">
            <div class="step-number">4</div>
            <div class="step-content">
              <h3>体验使用</h3>
              <p>立即体验推荐的工具，或创建自己的教学工具</p>
            </div>
          </div>
        </div>

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
.feature-detail {
  min-height: 100vh;
  background: var(--color-bg);
}

.feature-header {
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

.feature-title {
  margin: 0 0 8px;
  font-family: var(--font-display);
  font-size: 36px;
  font-weight: 600;
  color: var(--color-ink);
}

.feature-subtitle {
  margin: 0;
  font-family: var(--font-sans);
  font-size: 16px;
  color: var(--color-ink-soft);
}

.feature-content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 48px 32px;
}

.feature-hero {
  text-align: center;
  margin-bottom: 48px;
}

.feature-image {
  max-width: 400px;
  height: auto;
}

.feature-info h2 {
  font-family: var(--font-display);
  font-size: 24px;
  font-weight: 600;
  color: var(--color-ink);
  margin: 32px 0 16px;
}

.feature-info p {
  font-family: var(--font-sans);
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-ink-soft);
  margin-bottom: 16px;
}

.feature-info ul {
  list-style: none;
  padding: 0;
  margin-bottom: 24px;
}

.feature-info li {
  font-family: var(--font-sans);
  font-size: 16px;
  line-height: 1.8;
  color: var(--color-ink-soft);
  padding-left: 24px;
  position: relative;
  margin-bottom: 8px;
}

.feature-info li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: var(--color-ink);
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 32px;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 24px;
  background: white;
  border-radius: 12px;
}

.step-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-ink);
  color: #fafafa;
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 600;
  border-radius: 50%;
  flex-shrink: 0;
}

.step-content h3 {
  margin: 0 0 8px;
  font-family: var(--font-sans);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-ink);
}

.step-content p {
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
  .feature-header {
    padding: 16px 20px;
  }

  .feature-title {
    font-size: 28px;
  }

  .feature-content {
    padding: 32px 20px;
  }

  .step {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .cta {
    flex-direction: column;
  }

  .btn-primary, .btn-secondary {
    width: 100%;
  }
}
</style>
