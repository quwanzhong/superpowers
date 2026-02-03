package __PACKAGE_NAME__.net

data class BaseResponse<T>(
    val code: Int? = null,
    val msg: String? = null,
    val data: T? = null,
    val success: Boolean? = null
) {
    fun isSuccess(): Boolean = success == true || code == 200
}
