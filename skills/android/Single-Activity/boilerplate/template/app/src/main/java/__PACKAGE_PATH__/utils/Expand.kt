package __PACKAGE_NAME__.utils

import androidx.annotation.IdRes
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment

fun AppCompatActivity.replaceFragment(
    @IdRes containerViewId: Int,
    fragment: Fragment,
    tag: String
) {
    supportFragmentManager.beginTransaction()
        .setReorderingAllowed(true)
        .replace(containerViewId, fragment, tag)
        .commit()
}
