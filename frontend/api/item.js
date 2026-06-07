import { get, post, put, MOCK, resolveImageUrl } from './index'

const BASE_URL = 'http://127.0.0.1:5000'

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
    const token = uni.getStorageSync('token')
    return new Promise((resolve, reject) => {
        uni.uploadFile({
            url: BASE_URL + '/api/items/images/upload',
            filePath: filePath,
            name: 'file',
            header: {
                'Authorization': 'Bearer ' + (token || '')
            },
            success(res) {
                try {
                    const data = JSON.parse(res.data)
                    if (data.code === 0) {
                        resolve(data.data.url)
                    } else {
                        uni.showToast({ title: data.message || '上传失败', icon: 'none' })
                        reject(data)
                    }
                } catch (e) {
                    reject(e)
                }
            },
            fail(err) {
                uni.showToast({ title: '网络错误', icon: 'none' })
                reject(err)
            }
        })
    })
}