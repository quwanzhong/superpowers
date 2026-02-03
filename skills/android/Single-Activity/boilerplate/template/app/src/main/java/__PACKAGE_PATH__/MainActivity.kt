package __PACKAGE_NAME__

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import __PACKAGE_NAME__.databinding.ActivityMainBinding
import __PACKAGE_NAME__.utils.replaceFragment

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        if (savedInstanceState == null) {
            replaceFragment(binding.container.id, HomeFragment.newInstance(), "HomeFragment")
        }
    }
}
