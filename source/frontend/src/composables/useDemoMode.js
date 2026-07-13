import { readonly, ref } from 'vue'
import { demoData } from '../data/demo'

const clone = (value) => value == null ? value : JSON.parse(JSON.stringify(value))

export function useDemoMode(env = import.meta.env) {
  const enabled = readonly(ref(env?.VITE_DEMO_MODE === 'true'))
  return { enabled, label: '演示数据', getDemoData: (key) => enabled.value ? clone(demoData[key]) : undefined }
}
