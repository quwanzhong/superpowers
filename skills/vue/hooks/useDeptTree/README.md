# 🌟 Skill: useDeptTree (部门树组合式钩子)

### 📖 描述
该技能专为处理“部门层级数据”设计。它封装了递归转换逻辑、响应式状态管理以及 API 请求流程，将后端返回的原始数据一键转换为前端 UI 组件（如 `el-cascader` 或 `el-tree`）可用的格式。

---

### 🚀 核心超能力
* **自动递归**：内置 `normalizeDeptTree` 逻辑，自动将 `children` 转换为符合 UI 组件规范的结构。
* **配置标准化**：预设 `deptCascaderProps`，支持单选、路径点击等常用业务配置。
* **请求封装**：集成 `getDeptByUserIdList` 接口调用。

---

### 🛠️ 使用指南

#### 1. 逻辑引入 (Setup Script)
```typescript
import { onMounted } from 'vue';
import { useDeptTree } from '@/skills/vue/hooks/useDeptTree';

const { 
  deptOptions, 
  deptCascaderProps, 
  getDeptData 
} = useDeptTree();

// 挂载时初始化数据
onMounted(() => {
  getDeptData();
});
``` 

#### 2. 模板绑定示例 (Template)
配合 Element Plus 的 el-cascader/el-tree 使用
``` typescript
<template>
  <el-cascader
    v-model="selectedDept"
    :options="deptOptions"
    :props="deptCascaderProps"
    placeholder="请选择部门"
    clearable
  />
</template>
```