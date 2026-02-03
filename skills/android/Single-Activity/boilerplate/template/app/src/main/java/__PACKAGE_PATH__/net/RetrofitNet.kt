package __PACKAGE_NAME__.net

import __PACKAGE_NAME__.constants.UrlConstant
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

object RetrofitNet {

    private val retrofit: Retrofit by lazy {
        Retrofit.Builder()
            .client(
                OkHttpClient.Builder()
                    .connectTimeout(30, TimeUnit.SECONDS)
                    .readTimeout(20, TimeUnit.SECONDS)
                    .writeTimeout(20, TimeUnit.SECONDS)
                    .addInterceptor(LoggingInterceptor.create())
                    .addInterceptor(AuthInterceptor())
                    .addInterceptor(HeaderInterceptor())
                    .build()
            )
            .baseUrl(UrlConstant.baseUrl)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    fun <T> createApi(api: Class<T>): T {
        return retrofit.create(api)
    }
}
