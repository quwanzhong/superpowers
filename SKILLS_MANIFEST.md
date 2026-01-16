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