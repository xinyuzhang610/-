<script setup>
import { nextTick, ref } from 'vue'
import { sendChat } from '../../api/chat'

const input = ref(''), pending = ref(false), error = ref(''), sessionId = ref(''), feed = ref(null)
const messages = ref([{ id: 'welcome', role: 'assistant', content: '把你正在卡住的问题写下来。我们会从已知条件出发，一步一步找到突破口。' }])
const lastFailed = ref('')
const scroll = () => nextTick(() => { if (feed.value) feed.value.scrollTop = feed.value.scrollHeight })
async function submit(text = input.value) {
  const question = text.trim(); if (!question || pending.value) return
  pending.value = true; error.value = ''; lastFailed.value = question
  try {
    const { data } = await sendChat({ message: question, session_id: sessionId.value || undefined })
    messages.value.push({ id: `u-${Date.now()}`, role: 'user', content: question }, { id: `a-${Date.now()}`, role: 'assistant', content: data.reply })
    sessionId.value = data.session_id; input.value = ''; lastFailed.value = ''; scroll()
  } catch (cause) { error.value = cause?.response?.data?.detail || '回答生成超时，问题仍保留在输入框中。'; input.value = question }
  finally { pending.value = false }
}
</script>

<template>
  <main class="chat-page">
    <aside class="context-panel"><p class="eyebrow">AI LEARNING COMPANION</p><h1>让问题显形</h1><p>它不会替你跳过思考，而会帮助你看见条件、关系与下一步。</p><dl><div><dt>当前会话</dt><dd>{{ sessionId || '尚未建立' }}</dd></div><div><dt>对话原则</dt><dd>先理解，再推导</dd></div></dl></aside>
    <section class="chat-panel" aria-labelledby="chat-title"><header><span class="core" aria-hidden="true"><i /></span><div><h2 id="chat-title">智教通学习助手</h2><p>{{ pending ? '正在梳理知识脉络…' : '在线 · 等待你的问题' }}</p></div></header>
      <div ref="feed" class="message-feed" aria-live="polite"><article v-for="message in messages" :key="message.id" :class="message.role"><span aria-hidden="true">{{ message.role === 'user' ? '你' : '智' }}</span><p>{{ message.content }}</p></article><article v-if="pending" class="assistant pending"><span aria-hidden="true">智</span><p>正在连接知识节点<span class="dots">···</span></p></article></div>
      <div v-if="error" class="error-note" role="alert"><p>{{ error }}</p><button data-testid="retry-message" type="button" @click="submit(lastFailed)">重试上一次提问</button></div>
      <form class="composer" @submit.prevent="submit()"><label for="student-question">输入你的问题</label><textarea id="student-question" v-model="input" rows="3" placeholder="例如：为什么勾股定理只适用于直角三角形？" /><div><span>{{ input.length }}/1000</span><button type="submit" :disabled="pending || !input.trim()">{{ pending ? '生成中' : '发送问题' }}</button></div></form>
    </section>
  </main>
</template>

<style scoped>
.chat-page{display:grid;min-height:calc(100vh - 80px);grid-template-columns:minmax(260px,.7fr) minmax(0,1.6fr);gap:24px;padding:clamp(22px,4vw,52px);background:linear-gradient(135deg,#0d1714,#172722);color:var(--moon-50)}.context-panel,.chat-panel{border:1px solid rgb(203 211 201 / 16%);border-radius:28px;background:rgb(255 255 255 / 4%);box-shadow:0 30px 80px rgb(0 0 0 / 22%)}.context-panel{padding:clamp(24px,3vw,42px);background:radial-gradient(circle at 20% 8%,rgb(213 166 79 / 18%),transparent 28%),rgb(255 255 255 / 3%)}.eyebrow{color:var(--gold-300);font-size:.68rem;letter-spacing:.2em}.context-panel h1{margin:20px 0;font:500 clamp(2.3rem,4vw,4.2rem)/1.1 var(--font-display)}.context-panel>p:not(.eyebrow){color:var(--moon-300);line-height:1.8}.context-panel dl{margin-top:48px}.context-panel dl div{padding:15px 0;border-top:1px solid rgb(255 255 255 / 12%)}dt{color:var(--ink-300);font-size:.72rem}dd{margin:5px 0 0}.chat-panel{display:flex;min-height:650px;flex-direction:column;overflow:hidden}.chat-panel>header{display:flex;align-items:center;gap:14px;padding:20px 24px;border-bottom:1px solid rgb(255 255 255 / 10%)}.chat-panel h2{font:500 1.05rem var(--font-heading)}.chat-panel header p{margin-top:3px;color:var(--jade-200);font-size:.72rem}.core{display:grid;width:42px;height:42px;place-items:center;border:1px solid var(--gold-400);border-radius:50%;box-shadow:0 0 24px rgb(213 166 79 / 26%)}.core i{width:9px;height:9px;border-radius:50%;background:var(--gold-300)}.message-feed{display:flex;flex:1;flex-direction:column;gap:18px;overflow-y:auto;padding:28px}.message-feed article{display:flex;max-width:82%;gap:10px;align-items:flex-start}.message-feed article>span{display:grid;width:32px;height:32px;flex:0 0 32px;place-items:center;border:1px solid var(--jade-400);border-radius:50%;color:var(--jade-200);font-size:.7rem}.message-feed article p{padding:13px 16px;border-radius:4px 18px 18px 18px;background:rgb(255 255 255 / 7%);line-height:1.7;white-space:pre-wrap}.message-feed .user{align-self:flex-end;flex-direction:row-reverse}.message-feed .user p{border-radius:18px 4px 18px 18px;background:rgb(23 107 90 / 44%)}.error-note{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 24px;padding:12px 14px;border:1px solid rgb(189 69 59 / 50%);border-radius:12px;background:rgb(189 69 59 / 10%);color:#ffd2cd}.error-note button{min-height:40px;padding:0 14px;border:1px solid currentColor;border-radius:9px;background:transparent;color:inherit;cursor:pointer}.composer{margin:18px 24px 24px;padding:15px;border:1px solid rgb(213 166 79 / 26%);border-radius:18px;background:rgb(0 0 0 / 14%)}.composer label{display:block;margin-bottom:7px;color:var(--moon-300);font-size:.72rem}.composer textarea{width:100%;resize:none;border:0;background:transparent;color:var(--moon-50);font:inherit;line-height:1.6;outline:0}.composer>div{display:flex;align-items:center;justify-content:space-between}.composer span{color:var(--ink-300);font-size:.68rem}.composer button{min-height:44px;padding:0 20px;border:0;border-radius:11px;background:var(--gold-400);color:var(--ink-950);font-weight:700;cursor:pointer}.composer button:disabled{opacity:.45;cursor:not-allowed}@media(max-width:820px){.chat-page{grid-template-columns:1fr}.context-panel{min-height:auto}.chat-panel{min-height:70vh}}@media(max-width:520px){.chat-page{padding:14px}.message-feed{padding:18px}.message-feed article{max-width:95%}.error-note{align-items:flex-start;flex-direction:column}}
</style>
