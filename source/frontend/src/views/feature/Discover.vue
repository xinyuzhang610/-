<template>
  <div class="feature-detail vintage-theme">
    <header class="feature-header">
      <router-link to="/" class="back-link">← 返回首页</router-link>
      <VintageOrnament name="swallow" />
      <VintageRibbonTitle label="NEED DISCOVERY" />
      <h1 class="feature-title">智能教学需求发现</h1>
      <p class="feature-subtitle">AI自动分析教学场景，精准识别教师需求</p>
      <VintageDivider />
    </header>

    <div class="feature-content">
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
            <div class="step-num">01</div>
            <div class="step-content">
              <h3>文理分科</h3>
              <p>选择您的教学方向（文科/理科），缩小推荐范围</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">02</div>
            <div class="step-content">
              <h3>选择学科</h3>
              <p>细化到语数英等具体教学科目</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">03</div>
            <div class="step-content">
              <h3>明确目标</h3>
              <p>定位备课、上课、辅导或兴趣激发的真实需求</p>
            </div>
          </div>
          <div class="step">
            <div class="step-num">04</div>
            <div class="step-content">
              <h3>工具匹配</h3>
              <p>从真实工具库中匹配最适合的课堂工具</p>
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
import VintageRibbonTitle from '../../components/vintage/VintageRibbonTitle.vue'
import VintageDivider from '../../components/vintage/VintageDivider.vue'
import VintageOrnament from '../../components/vintage/VintageOrnament.vue'
</script>

<style scoped>
.feature-detail.vintage-theme {
  min-height: 100vh;
  background:
    radial-gradient(circle at 10% 8%, rgba(184, 161, 110, 0.07), transparent 30%),
    radial-gradient(circle at 90% 85%, rgba(138, 154, 140, 0.05), transparent 25%),
    #f5f1e8;
  color: #4a4333;
}

.feature-detail.vintage-theme::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.03;
  background-image:
    radial-gradient(circle at 25% 25%, #6b5d3e 1px, transparent 1px),
    radial-gradient(circle at 75% 75%, #6b5d3e 1px, transparent 1px);
  background-size: 80px 80px;
  z-index: 0;
}

.feature-header {
  position: relative;
  z-index: 1;
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 32px 0;
  text-align: center;
}

.feature-header .vintage-ornament {
  margin-bottom: 0.5rem;
}

.back-link {
  display: inline-block;
  font-family: var(--font-display);
  font-size: 0.9rem;
  color: #8b6f47;
  text-decoration: none;
  margin-bottom: 24px;
  transition: color 0.2s;
}

.back-link:hover { color: #5c4f34; }

.feature-title {
  margin: 0.75rem 0 8px;
  font: 500 clamp(2.2rem, 4.5vw, 3.8rem)/1.1 var(--font-display);
  color: #3d3526;
}

.feature-subtitle {
  margin: 0;
  font-size: 1rem;
  color: #6b5d3e;
  line-height: 1.7;
}

.feature-header .vintage-divider {
  margin: 1.25rem 0 0;
}

.feature-content {
  position: relative;
  z-index: 1;
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 32px 80px;
}

.feature-info h2 {
  font: 500 1.6rem var(--font-display);
  color: #3d3526;
  margin: 36px 0 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(196, 180, 154, 0.3);
}

.feature-info p {
  font-size: 1rem;
  line-height: 1.85;
  color: #5c4f34;
  margin-bottom: 16px;
}

.feature-info ul {
  list-style: none;
  padding: 0;
  margin-bottom: 24px;
}

.feature-info li {
  font-size: 1rem;
  line-height: 1.8;
  color: #5c4f34;
  padding-left: 24px;
  position: relative;
  margin-bottom: 8px;
}

.feature-info li::before {
  content: '◆';
  position: absolute;
  left: 0;
  color: #b8a16e;
  font-size: 0.5rem;
  top: 0.55rem;
}

/* 步骤卡片 */
.steps {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 18px;
  padding: 22px 24px;
  border: 1px solid rgba(196, 180, 154, 0.35);
  border-radius: 2px;
  background: rgba(250, 248, 242, 0.6);
  position: relative;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.step::before {
  content: '';
  position: absolute;
  inset: 4px;
  border: 1px dashed rgba(139, 111, 71, 0.15);
  pointer-events: none;
}

.step:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(107, 93, 62, 0.08);
}

.step-num {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #b8a16e;
  border-radius: 50%;
  background: rgba(184, 161, 110, 0.1);
  color: #8b6f47;
  font: 600 1.1rem var(--font-display);
  flex-shrink: 0;
}

.step-content h3 {
  margin: 0 0 6px;
  font: 600 1.1rem var(--font-display);
  color: #3d3526;
}

.step-content p {
  margin: 0;
  font-size: 0.9rem;
  color: #6b5d3e;
}

/* CTA */
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
  border: 1px solid #b8a16e;
  border-radius: 2px;
  background: linear-gradient(135deg, rgba(250, 248, 242, 0.95), rgba(242, 239, 230, 0.85));
  color: #5c4f34;
  font: 600 1rem var(--font-display);
  text-decoration: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(107, 93, 62, 0.12);
}

.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 14px 32px;
  border: 1px solid rgba(196, 180, 154, 0.4);
  border-radius: 2px;
  background: transparent;
  color: #6b5d3e;
  font: 500 1rem var(--font-display);
  text-decoration: none;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  border-color: #b8a16e;
  background: rgba(184, 161, 110, 0.06);
}

@media (max-width: 640px) {
  .feature-header { padding: 24px 20px 0; }
  .feature-title { font-size: 2rem; }
  .feature-content { padding: 32px 20px 60px; }
  .step { flex-direction: column; align-items: flex-start; }
  .cta { flex-direction: column; }
  .btn-primary, .btn-secondary { width: 100%; text-align: center; }
}
</style>
