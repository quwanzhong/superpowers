# 创建 Single-Activity 项目（铠甲生成器）

## 目标

从 `skills/android/single-Activity/boilerplate/template` 生成一个**最小可运行**的 Android 工程骨架，并替换：
- `applicationId`
- Kotlin 包名（`packageName`）
- `appName`
- `baseUrl`

> 生成方式：本地脚本（路线 2）。

---

## 参数

- **target_dir**
  - 新工程输出目录（必须不存在或为空目录）
- **application_id**
  - Android `applicationId`，例如：`com.xxx.yyy`
- **package_name**
  - Kotlin 源码包名（通常与 `application_id` 一致）
- **app_name**
  - 应用展示名，例如：`血站终端`
- **base_url**
  - `BuildConfig.BASE_URL` 的默认值

---

## 使用

在终端执行：

```bash
python3 /Users/qwz/superpowers/skills/android/single-Activity/boilerplate/create_single_activity.py \
  --target_dir "/path/to/new-project" \
  --application_id "com.example.singleactivity" \
  --package_name "com.example.singleactivity" \
  --app_name "SingleActivityApp" \
  --base_url "http://127.0.0.1/"
```

生成后：
- 用 Android Studio 打开 `target_dir`
- 等待 Gradle Sync
- 直接运行

质量门禁：
- 在工程根目录执行：`./gradlew quality`
- 该任务会聚合 `lintDebug` + `testDebugUnitTest`
- 开发节奏建议按测试驱动开发（TDD）的红-绿-重构周期推进，并避免常见测试反模式（详见 obra/superpowers 仓库内相关规范）

## 版本约定

- **Gradle**: 8.10-bin
- **AGP**: 8.10.0
- **Kotlin**: 1.9.24

---

## 约定

- 模板占位符：见 `boilerplate/template.config.json`
- 替换逻辑：
  - 文本文件内替换 `__APPLICATION_ID__` / `__PACKAGE_NAME__` / `__APP_NAME__` / `__BASE_URL__`
  - 源码目录 `app/src/main/java/__PACKAGE_PATH__/` 会被重命名为实际包路径
- 忽略文件：见 `boilerplate/template.ignore`
