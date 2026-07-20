export const demoData = {
  recommendations: { tools: [
    { id: 1, name: '古诗词趣味赏析', description: '将意象、背景与表达手法组织为课堂探索线索。', subject: '语文' },
    { id: 6, name: '诗词飞花令', description: '以飞花令游戏激发古诗词兴趣。', subject: '语文' },
    { id: 4, name: '阅读理解辅助', description: '帮学生抓住文本关键信息和中心思想。', subject: '语文' }
  ] },
  tools: { items: [
    { id: 1, name: '古诗词趣味赏析', description: '从意象与时代背景切入古诗词。', category: '文科', subject: '语文', usage_count: 128, is_preset: true },
    { id: 7, name: '公式推导助手', description: '把抽象公式拆解为可追踪的推导路径。', category: '理科', subject: '数学', usage_count: 96, is_preset: true }
  ] },
  dashboard: {
    total_tools: 18, total_users: 326, today_usage: 84,
    weekly_trend: [{ date: '07/08', count: 42 }, { date: '07/09', count: 58 }, { date: '07/10', count: 49 }, { date: '07/11', count: 76 }, { date: '07/12', count: 63 }, { date: '07/13', count: 91 }, { date: '07/14', count: 84 }],
    top_tools: [{ name: '古诗词趣味赏析', count: 128 }, { name: '公式推导助手', count: 96 }, { name: '概念辨析器', count: 73 }],
    recent_logs: [{ id: 1, user_id: 12, tool_id: 1, input_text: '分析《静夜思》的意象', output_text: '从月光意象开始…', created_at: '2026-07-14T08:20:00Z' }]
  },
  plaza: {
    categories: [{ value: '文科', label: '文科专区' }, { value: '理科', label: '理科专区' }, { value: '通用', label: '通用工具' }],
    tools: [
      { id: 1, name: '古诗词趣味赏析', description: '以意象为入口探索诗词。', category: '文科', subject: '语文', usage_count: 128 },
      { id: 7, name: '公式推导助手', description: '逐步理解公式的来路。', category: '理科', subject: '数学', usage_count: 96 },
      { id: 11, name: '概念辨析器', description: '对照易混概念与适用边界。', category: '通用', subject: null, usage_count: 73 }
    ],
    hot_tools: [{ id: 1 }, { id: 7 }]
  },
  studentHistory: [
    { id: 1, tool_id: 7, user_id: 8, input_text: '勾股定理为什么成立？', output_text: '可以从正方形面积关系开始理解。', session_id: 'demo-session', created_at: '2026-07-14T08:00:00Z' },
    { id: 2, tool_id: 1, user_id: 8, input_text: '《静夜思》的月光有什么作用？', output_text: '月光连接了眼前景象与故乡记忆。', session_id: 'demo-session-2', created_at: '2026-07-13T09:30:00Z' }
  ]
}
