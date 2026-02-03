package __PACKAGE_NAME__.net

import okhttp3.Interceptor
import okhttp3.Response

class LoggingInterceptor private constructor() : Interceptor {
    override fun intercept(chain: Interceptor.Chain): Response {
        return chain.proceed(chain.request())
    }

    companion object {
        fun create(): LoggingInterceptor = LoggingInterceptor()
    }
}
