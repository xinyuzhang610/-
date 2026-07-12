import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const getPlaza = (category, search) =>
  api.get('/plaza/', { params: { category, search } })

export const getCategories = () =>
  api.get('/plaza/categories')

export const getHotTools = (limit = 5) =>
  api.get('/plaza/hot', { params: { limit } })
