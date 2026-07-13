import { beforeEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createMemoryHistory, createRouter } from 'vue-router'
import Layout from '../layout/index.vue'
import TeacherHome from '../views/teacher/Home.vue'
import Tools from '../views/teacher/Tools.vue'
import Dashboard from '../views/teacher/Dashboard.vue'
import MetricCard from '../components/data/MetricCard.vue'

const recommend=vi.fn(),presetTools=vi.fn(),dashboardRequest=vi.fn()
vi.mock('../api/recommend',()=>({getRecommendation:(...args)=>recommend(...args)}))
vi.mock('../api/tools',()=>({getPresetTools:(...args)=>presetTools(...args),deleteTool:vi.fn(),getShareLink:vi.fn()}))
vi.mock('../api/usage',()=>({getDashboard:(...args)=>dashboardRequest(...args)}))

async function routerAt(path='/teacher/home'){
 const router=createRouter({history:createMemoryHistory(),routes:[{path:'/',component:{template:'<div/>'}},{path:'/login',component:{template:'<div/>'}},{path:'/teacher',component:Layout,children:[{path:'home',component:TeacherHome,meta:{title:'需求引导'}},{path:'tools',component:Tools},{path:'dashboard',component:Dashboard}]},{path:'/student/guidance',component:{template:'<div/>'}}]})
 await router.push(path);await router.isReady();return router
}

describe('teacher workspace',()=>{
 beforeEach(()=>{setActivePinia(createPinia());recommend.mockReset();presetTools.mockReset();dashboardRequest.mockReset();localStorage.setItem('token','test')})
 it('renders accessible teacher navigation with active route',async()=>{recommend.mockResolvedValue({data:{tools:[]}});const router=await routerAt();const wrapper=mount(Layout,{global:{plugins:[router,createPinia()]}});expect(wrapper.text()).toContain('需求引导');expect(wrapper.text()).toContain('我的工具');expect(wrapper.text()).toContain('数据洞察');expect(wrapper.get('a[aria-current="page"]').text()).toContain('需求引导');expect(wrapper.get('[aria-label="打开导航菜单"]').exists()).toBe(true)})
 it('keeps the three guidance stages ordered and blocks goals until category selection',async()=>{const wrapper=mount(TeacherHome,{global:{stubs:{RouterLink:true}}});expect(wrapper.findAll('.guidance-step')).toHaveLength(3);expect(wrapper.text()).toContain('选择学科领域');expect(wrapper.text()).toContain('明确教学目标');expect(wrapper.text()).toContain('获得工具推荐');expect(wrapper.get('.goals button').attributes('disabled')).toBeDefined();await wrapper.get('.choice-grid button').trigger('click');expect(wrapper.get('.goals button').attributes('disabled')).toBeUndefined()})
 it('shows an honest empty tools state',async()=>{presetTools.mockResolvedValue({data:{items:[]}});const wrapper=mount(Tools,{global:{stubs:{RouterLink:true}}});await flushPromises();expect(wrapper.text()).toContain('工具库还是空的')})
 it('shows dashboard API errors with retry state',async()=>{dashboardRequest.mockRejectedValue(new Error('offline'));const wrapper=mount(Dashboard);await flushPromises();expect(wrapper.text()).toContain('数据暂时不可用');expect(wrapper.find('[role="alert"]').exists()).toBe(true)})
 it('exposes metric label and value semantically',()=>{const wrapper=mount(MetricCard,{props:{label:'今日使用',value:18}});expect(wrapper.attributes('aria-label')).toBe('今日使用：18')})
})
