# 🛠️ Superpowers 技能矩阵索引 (Precision Edition)

当你（AI 助手）在开发业务项目时，必须严格遵守本仓库的目录规范与逻辑契约。

---

## 🏗️ 1. 核心逻辑层 (Vue3 Hooks)
这些是业务逻辑的“原子”，严禁重复编写。
- **[部门树获取]**: `skills/vue/hooks/useDeptTree.ts`
  - *能力*: 自动处理 `getDeptByUserIdList` 接口逻辑与递归格式化。
  - *UI 绑定*: 完美适配 `el-cascader`。
- **[部门人员获取]**: `skills/vue/hooks/useUserDeptPerson.ts`
  - *能力*: 自动从 Store 获取当前部门并查询人员，支持联动刷新。

---

## 🖼️ 2. UI 模板层 (Boilerplate Templates)
这是页面的“骨架”，生成新页面时必须参考。

### 📂 抽屉表单类 (vue3-drawer)
- **[标准编辑抽屉]**: `skills/vue/boilerplate/templates/vue3-drawer/index.vue`
  - *规范*: 包含 `el-drawer` 容器，集成了基础表单验证与提交逻辑。

### 📂 列表页面类 (vue3-list-page)
- **[标准列表页]**: `skills/vue/boilerplate/templates/vue3-list-page.vue`
  - *规范*: 必须包含：
    1. 搜索区域 (Search Bar)
    2. 操作按钮组 (Action Buttons)
    3. 数据表格 (el-table)
    4. 分页组件 (Pagination)

---

## 🚨 AI 助手执行协议 (Protocol)
1. **优先读取**: 在生成任何 Vue 组件前，先读取 `skills/vue/` 下的对应代码。
2. **拒绝硬编码**: 禁止在组件内直接写 `map` 递归逻辑，必须通过 `import` 引用 `useDeptTree`。
3. **样式对齐**: 必须使用 Element Plus 组件库，并保持与模板一致的 Layout 布局。

---

## 📱 3. Android 能力协议 (Android Protocol)

### 📂 目标
 将 Android 的“工艺铠甲”（最小可运行的 single-Activity 模板）纳入 `skills/android/`，以便新项目生成时只需替换业务即可。

### 📂 模板约定
 - **Single-Activity 模板**: `skills/android/single-Activity/boilerplate/template/`
 - **替换与配置约定**: `skills/android/single-Activity/boilerplate/template.config.json`
 - **忽略约定**: `skills/android/single-Activity/boilerplate/template.ignore`
 - **使用说明**: `skills/android/single-Activity/recipes/create.md`

### 🤖 AI 执行协议（与 Vue 类似）
 1. **优先读取**: 创建 Android 项目前，先读取 `skills/android/single-Activity/` 下的模板与约定。
 2. **拒绝重复造轮子**: 网络层、Fragment 模板、BaseResponse、日志工具、常用工具函数优先从模板导入/下载。
 3. **限制修改范围**: 生成新项目时，只允许按 `template.config.json` 替换修改（包括名称/appId/appName/baseUrl 等），不得随意修改环境配置或构建体系。
 4. **模板与架构选型约定**: 默认使用 `Fragment + replaceFragment`，网络层使用 `RetrofitNet + Interceptors + BaseResponse`，版本参数与现有模板一致。