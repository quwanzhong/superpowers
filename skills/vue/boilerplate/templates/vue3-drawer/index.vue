<template>
  <Drawer :model-value="visible" @update:modelValue="(val) => emit('update:visible', val)" :title="drawerTitle"
    :size="1630">
    <template #cont>
      <!-- 新增/编辑模式 -->
      <PageAdd ref="formAddEditRef" v-if="mode === 'create' || mode === 'edit'" :mode="mode"
        :formStep="formStep" :activeStep="activeStep" @update:activeStep="activeStep = $event" />
      
      <!-- 查看模式 -->
      <PageView v-else-if="mode === 'view'" :showInfo="detailInfo" />
    </template>

    <template #footer>
      <div :class="{ 'only-cancel': mode === 'view' }">
        <BaseButton @click="handleCancel" btn-type="default">取消</BaseButton>
        
        <!-- 分步按钮逻辑 -->
        <BaseButton v-if="mode !== 'view' && activeStep === 2" @click="handlePrev" :disabled="activeStep === 1"
          btn-type="secondary">上一步</BaseButton>
        <BaseButton v-if="mode !== 'view' && activeStep === 1" type="primary" @click="handleNext">下一步</BaseButton>
        <BaseButton v-if="mode !== 'view' && activeStep === 2" type="primary" @click="handleSave">保存</BaseButton>
      </div>
    </template>
  </Drawer>
</template>

<script setup>
/**
 * 模板说明：
 * 这是一个通用的抽屉（Drawer）框架组件，包含：
 * 1. 抽屉容器与底部按钮栏
 * 2. 模式切换 (create/edit/view)
 * 3. 分步逻辑 (activeStep)
 * 4. 动态加载 Add (新增/编辑) 和 View (查看) 子组件
 * 
 * 使用说明：
 * 1. 引用 `add.vue` 和 `view.vue`
 * 2. 替换 API 接口
 * 3. 定义表单结构 `formStep`
 */

import PageAdd from './add.vue'
import PageView from './view.vue'
// import { addApi, updateApi, getDetailApi } from '@blood-supply-department-web/api/yourApi';

const props = defineProps({
  mode: { type: String, default: 'create' }, // create, edit, view
  visible: { type: Boolean, default: false },
  record: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['update:visible', 'save', 'fresh'])

// 状态管理
const formAddEditRef = ref(null)
const detailInfo = ref({}) // 详情数据
const mainId = ref("") // 主键ID

// 向子组件提供上下文
provide("recordInfo", props.record)

// 标题逻辑
const drawerTitle = computed(() => {
  if (props.mode === 'view') return '查看详情'
  if (props.mode === 'edit') return '编辑信息'
  return '新增信息'
})

// 分步逻辑
const activeStep = ref(1)
const formStep = reactive({
  id: '',
  receiveDeptId: '', // 示例字段
  remark: '',
  // ... 其他字段
})

// 重置表单
const resetForm = () => {
  Object.assign(formStep, {
    id: '',
    receiveDeptId: '',
    remark: '',
  })
  activeStep.value = 1
  mainId.value = ""
}

// 获取详情
const getDetail = async (id) => {
  try {
    if (id) {
      // const res = await getDetailApi(id)
      // detailInfo.value = res || {}
      
      // 模拟数据
      detailInfo.value = { 
        code: 'ORDER001', 
        status: '1', 
        detailList: [{ productName: '示例产品', volume: 1 }] 
      }
    }
  } catch (error) {
    console.error('获取详情失败:', error)
  }
}

// 按钮操作：取消
const handleCancel = () => {
  emit("fresh")
  emit('update:visible', false)
}

// 按钮操作：上一步
const handlePrev = async () => {
  activeStep.value = 1
}

// 按钮操作：下一步 (Step 1 -> Step 2)
const handleNext = async () => {
  // 1. 校验 Step 1 表单
  const validation = formAddEditRef.value?.validateForm()
  if (!validation?.isValid) {
    ElMessage.error(validation.errors[0] || '请完善表单信息')
    return
  }
  
  // 2. 获取 Step 1 数据并提交 (可选：分步提交或最后统一提交)
  const formData = formAddEditRef.value?.getFormData1()
  if (formData) {
    // 示例：第一步先保存主表
    // const res = await addApi(formData.formStep)
    // if (res) {
    //   mainId.value = res
    //   activeStep.value = 2
    // }
    
    // 模拟成功
    activeStep.value = 2
  }
}

// 按钮操作：保存 (Step 2 -> Finish)
const handleSave = async () => {
  // 1. 校验 Step 2 数据
  const validation = formAddEditRef.value?.validateList()
  if (!validation?.isValid) {
    ElMessage.error(validation.errors[0] || '请完善明细信息')
    return
  }
  
  // 2. 获取全部数据并提交
  const listData = formAddEditRef.value?.getFormData2()
  if (listData) {
    // const ok = await updateApi({ id: mainId.value, details: listData })
    const ok = true // 模拟
    if (ok) {
      ElMessage.success('保存成功')
      emit("fresh")
      emit('update:visible', false)
    }
  }
}

// 监听弹窗显示
watch(
  () => props.visible,
  (val) => {
    if (val) {
      if (props.mode === 'view') {
        getDetail(props.record.id)
      } else {
        resetForm()
        // 如果是编辑模式，可以在这里回显数据
        // if (props.mode === 'edit') { ... }
      }
    } else {
      resetForm()
    }
  },
  { immediate: true }
)

</script>
