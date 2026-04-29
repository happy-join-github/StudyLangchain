// 引入 axios
const request = axios.create({
    baseURL: 'http://localhost:8080/api/v1', // 替换为你的后端 API 地址
    timeout: 10000
});

// 请求拦截器：自动带上 Token
request.interceptors.request.use(
    config => {
        const token = localStorage.getItem("token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }else{
            window.location.href = '../page/login.html'
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// 响应拦截器：统一处理业务报错和 Token 失效
request.interceptors.response.use(
    response => {
        const res = response.data;
        
        if (res.status === 200) {
            return res.data; 
        } else {
            alert(res.message || '请求失败');
            return Promise.reject(new Error(res.message || 'Error'));
        }
    },
    error => {
        // 处理 HTTP 状态码错误（比如 401 token 过期）
        if (error.response && error.response.status === 401) {
            alert("登录已失效，请重新登录");
            localStorage.removeItem("token");
            window.location.href = "./login.html";
        }  else {
            alert(error.response.message);
        }
        return Promise.reject(error);
    }
);

// 导出封装后的 request
window.$http = request;
