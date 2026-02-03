package __PACKAGE_NAME__.net

import okhttp3.Interceptor
import okhttp3.Response

class AuthInterceptor : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        // 这里后续接入你自己的 token 存储
        return chain.proceed(chain.request())
    }
}
