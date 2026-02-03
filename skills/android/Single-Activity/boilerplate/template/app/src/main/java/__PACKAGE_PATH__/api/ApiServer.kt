package __PACKAGE_NAME__.api

import __PACKAGE_NAME__.net.RetrofitNet

interface ApiServer {
    companion object {
        val api: ApiServer by lazy {
            RetrofitNet.createApi(ApiServer::class.java)
        }
    }
}
