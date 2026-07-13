<template>
  <div class="tutorial-detail">
    <header class="tutorial-header">
      <router-link to="/" class="back-link">← 返回首页</router-link>
      <h1 class="tutorial-title">需求引导教程</h1>
      <p class="tutorial-subtitle">通过智能引导，发现您的教学需求</p>
    </header>

    <div class="tutorial-content">
      <div class="tutorial-hero">
        <div class="hero-visual">
          <div class="visual-step">
            <div class="step-icon">📚</div>
            <div class="step-text">文理分科</div>
          </div>
          <div class="visual-arrow">→</div>
          <div class="visual-step">
            <div class="step-icon">🔍</div>
            <div class="step-text">需求分析</div>
          </div>
          <div class="visual-arrow">→</div>
          <div class="visual-step">
            <div class="step-icon">🛠️</div>
            <div class="step-text">工具推荐</div>
          </div>
          <div class="visual-arrow">→</div>
          <div class="visual-step">
            <div class="step-icon">✨</div>
            <div class="step-text">体验使用</div>
          </div>
        </div>
      </div>

      <div class="tutorial-info">
        <h2>什么是需求引导？</h2>
        <p>需求引导是智教通的核心创新点。我们发现，很多老师（尤其是"小白"用户）不知道自己需要什么样的教学工具。</p>
        <p>通过智能引导流程，系统能够：</p>
        <ul>
          <li>帮助您梳理教学场景和需求</li>
          <li>推荐最适合的教学工具</li>
          <li>降低使用AI工具的门槛</li>
          <li>让您快速找到解决方案</li>
        </ul>

        <h2>引导流程详解</h2>
        <div class="flow-detail">
          <div class="flow-step">
            <div class="flow-number">1</div>
            <div class="flow-content">
              <h3>文理分科</h3>
              <p>首先选择您的教学方向（文科或理科）。这一步帮助系统缩小推荐范围，为您推荐更精准的工具。</p>
              <p><strong>文科：</strong>语文、英语、历史、政治、地理</p>
              <p><strong>理科：</strong>数学、物理、化学、生物、信息技术</p>
            </div>
          </div>

          <div class="flow-step">
            <div class="flow-number">2</div>
            <div class="flow-content">
              <h3>需求引导</h3>
              <p>系统会询问您目前最需要帮助的教学场景：</p>
              <ul>
                <li><strong>课前备课：</strong>找资料、做课件、设计教学方案</li>
                <li><strong>课堂教学：</strong>互动、提问、演示、课堂管理</li>
                <li><strong>课后辅导：</strong>作业批改、答疑、个性化辅导</li>
                <li><strong>兴趣激发：</strong>趣味学习、游戏化教学、知识拓展</li>
              </ul>
            </div>
          </div>

          <div class="flow-step">
            <div class="flow-number">3</div>
            <div class="flow-content">
              <h3>工具推荐</h3>
              <p>根据您的选择，系统会推荐3-5个最合适的教学工具。每个工具都有：</p>
              <ul>
                <li>工具名称和图标</li>
                <li>功能简介</li>
                <li>"立即体验"按钮</li>
                <li>"了解更多"按钮</li>
              </ul>
            </div>
          </div>

          <div class="flow-step">
            <div class="flow-number">4</div>
            <div class="flow-content">
              <h3>体验使用</h3>
              <p>选择一个工具，立即体验AI辅助教学的便捷。您也可以：</p>
              <ul>
                <li>使用AI对话创建自己的工具</li>
                <li>跳转到师大智能体平台创建复杂工具</li>
                <li>将工具分享给学生使用</li>
              </ul>
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

.flow-detail {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 32px;
}

.flow-step {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 24px;
  background: white;
  border-radius: 12px;
}

.flow-number {
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

.flow-content h3 {
  margin: 0 0 8px;
  font-family: var(--font-sans);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-ink);
}

.flow-content p {
  margin: 0 0 8px;
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
}

.flow-content ul {
  margin: 8px 0 0;
  padding-left: 20px;
}

.flow-content li {
  font-size: 14px;
  margin-bottom: 4px;
}

.flow-content li::before {
  display: none;
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

  .flow-step {
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
