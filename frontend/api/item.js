import { get, post, put, MOCK, resolveImageUrl, uploadFile } from './index'

export function getCategories() {
  return get('/api/categories')
}

export function publishItem(data) {
  return post('/api/items/publish', data)
}

export function getItemDetail(id) {
  return get('/api/items/' + id)
}

export function searchItems(params) {
  return get('/api/items/search', params)
}

export function getUserItems(userId, params) {
  return get('/api/items/user/' + userId, params)
}

export function updateItem(id, data) {
  return put('/api/items/' + id, data)
}

export function offlineItem(id, userId) {
  return put('/api/items/' + id + '/offline?userId=' + userId)
}

export function onlineItem(id, userId) {
  return put('/api/items/' + id + '/online?userId=' + userId)
}

export function uploadImage(filePath) {
    return uploadFile('/api/items/images/upload', filePath, 'file').then(res => res.url)
}