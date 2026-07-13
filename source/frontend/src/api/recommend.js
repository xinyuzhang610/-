import axios from 'axios'
const client = axios.create({ baseURL: '/api/recommend', timeout: 10000 })
export const getRecommendation = (payload) => client.post('/', payload)

