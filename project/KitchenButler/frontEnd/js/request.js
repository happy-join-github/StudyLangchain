// 引入 axios
const request = axios.create({
    baseURL: 'http://localhost:8080/api/v1', // 替换为你的后端 API 地址
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 请求拦截器（可选：添加 token、loading 等）
request.interceptors.request.use(
    config => {
        console.log('发送请求:', config);
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// 响应拦截器（统一处理错误、数据格式等）
request.interceptors.response.use(
    response => {
        
        const res = response.data;
        if (res.code === 200) {
            return res.data; // 直接返回业务数据
        } else {
            alert(res.message || '请求失败');
            return Promise.reject(new Error(res.message || 'Error'));
        }
    },
    error => {
        // 网络错误或超时
        if (error.code === 'ECONNABORTED') {
            alert('请求超时，请重试');
        } else if (error.response) {
            // 服务器返回了错误状态码（如 404, 500）
            alert(`服务器错误: ${error.response.status}`);
        } else {
            alert('网络异常，请检查连接');
        }
        return Promise.reject(error);
    }
);

// 导出封装后的 request
window.$http = request;
