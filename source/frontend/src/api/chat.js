import { createApiClient } from './client'

const client = createApiClient('/api/chat', 15000)

export const sendChat = (payload) => client.post('/', payload)

export async function streamChat(payload, { onMeta, onDelta, onDone, onError } = {}) {
  const token = localStorage.getItem('token')
  const response = await fetch('/api/chat/stream', { method: 'POST', headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) }, body: JSON.stringify(payload) })
  if (!response.ok || !response.body) throw new Error(`stream request failed: ${response.status}`)
  const reader = response.body.getReader(); const decoder = new TextDecoder(); let buffer = ''
  while (true) {
    const { value, done } = await reader.read(); if (done) break
    buffer += decoder.decode(value, { stream: true })
    const blocks = buffer.split('\n\n'); buffer = blocks.pop() || ''
    for (const block of blocks) {
      const event = block.match(/^event: (.+)$/m)?.[1]; const raw = block.match(/^data: (.+)$/m)?.[1]
      if (!event || !raw) continue
      const data = JSON.parse(raw)
      if (event === 'meta') onMeta?.(data); else if (event === 'delta') onDelta?.(data); else if (event === 'done') onDone?.(data); else if (event === 'error') onError?.(data)
    }
  }
}
