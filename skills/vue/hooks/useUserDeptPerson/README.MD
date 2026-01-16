# 🌟 Skill: useUserDeptPerson (部门人员获取钩子)

### 📖 描述
该技能用于快速获取当前登录用户所属部门的所有人员列表。它自动集成了 `Pinia Store` 状态读取与业务接口调用，将原始的人员数据转换为标准的 Select 选项格式。

---

### 🚀 核心超能力
* **自动鉴权追踪**：内置 `useUserStore` 逻辑，自动提取当前登录用户的 `deptId`，无需手动传参。
* **数据标准归一化**：自动将后端返回的不同字段（如 `nickName` 或 `name`）统一映射为前端通用的 `label/value` 结构。
* **容错处理**：内置了对 `deptId` 缺失的拦截和异常捕获，确保页面不会因为接口报错而挂掉。

---

### 🛠️ 使用指南

#### 1. 逻辑引入 (Setup Script)
```typescript
import { onMounted } from 'vue';
import { useUserDeptPerson } from '@/skills/vue/hooks/useUserDeptPerson';

const { personOptions, fetchDeptPersons } = useUserDeptPerson();

onMounted(() => {
  fetchDeptPersons();
});
```

#### 2. 模板绑定示例 (Template)
配合 Element Plus 的 el-select 使用：
``` typescript
<template>
  <el-select v-model="selectedPerson" placeholder="请选择人员">
    <el-option
      v-for="item in personOptions"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>
```