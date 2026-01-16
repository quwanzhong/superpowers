<template>
  <div class="drawer-container des_scrollbar">

    <!-- 第一步：基本信息 -->
    <div v-show="activeStep === 1" class="step-content">
      <div>
        <div class="theme-title">基本信息</div>
        <div class="section-content">
          <el-form :model="formStep" label-position="top" class="form-vertical">
            <div class="theme-grid-row-3" style="padding:0;gap: 10px;">
              
              <!-- 示例字段：级联选择 -->
              <el-form-item label="用血机构" class="required-right">
                <el-cascader class="selectBox" v-model="formStep.receiveDeptId" :options="deptOptions"
                  :props="deptCascaderProps" placeholder="请选择用血机构" clearable filterable />
              </el-form-item>
              
              <!-- 示例字段：下拉选择 -->
              <el-form-item label="关联订血单">
                <el-select v-model="formStep.bsOrderDocIds" placeholder="请选择关联订血单" multiple clearable
                  collapse-tags-tooltip>
                  <el-option v-for="opt in orderListOptions" :key="opt.value" :label="opt.label" :value="opt.value" />
                </el-select>
              </el-form-item>

              <!-- 示例字段：字典选择 -->
              <el-form-item label="预约方式" class="required-right">
                <el-select v-model="formStep.appointmentType" placeholder="请选择预约方式" clearable>
                  <el-option v-for="opt in dict.appointmentType" :key="opt.value" :label="opt.name"
                    :value="opt.value" />
                </el-select>
              </el-form-item>
              
              <!-- 更多表单项... -->
              <el-form-item label="备注" class="form-title" style="grid-column: span 3;">
                <el-input v-model="formStep.remark" type="textarea" :autosize="{ minRows: 5 }" placeholder="请输入备注信息"
                  class="input-textarea" maxlength="100" show-word-limit />
              </el-form-item>
            </div>
          </el-form>
        </div>
      </div>
    </div>

    <!-- 第二步：列表/明细信息 -->
    <div v-show="activeStep === 2" class="step-content">
      <!-- 扫码输入组件 (可选) -->
      <ScanTipInput class="scan-input" v-model="scanCode" placeholder="请输入或扫描条码" @scan="handleScan" />
      
      <!-- 列表明细 -->
      <div class="step-block-top">
        <div class="theme-title">已登记明细</div>
        <el-table :data="scannedList" class="base-table" border max-height="300px">
          <el-table-column type="index" width="60" label="序号" align="center" />
          <el-table-column prop="donorCode" label="编码" width="180" align="center" />
          <el-table-column prop="productName" label="名称" align="center" />
          <!-- 示例：自定义列模板 -->
          <el-table-column prop="state" label="状态" width="120" align="center">
            <template #default="{ row }">
              <span :class="['state-pill', row.state === '已备血' ? 'is-prepared' : '']">{{ row.state }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80" align="center">
            <template #default="{ $index }">
              <BaseButton btn-type="table" status="delete" @click="removeScannedItem($index)">删除</BaseButton>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 汇总统计表 (复杂表格示例) -->
      <div class="step-block-top">
        <div class="theme-title">统计汇总表</div>
        <div class="summary-table">
          <el-table class="base-table" :data="summaryData" border show-summary :summary-method="getSummaries"
            :span-method="objectSpanMethod">
            <el-table-column prop="index" label="序号" width="80" align="center" />
            <el-table-column prop="productName" label="类别" min-width="140" align="center" />
            <el-table-column prop="specification" label="规格" width="130" align="center" />
            
            <!-- 多级表头示例 -->
            <el-table-column label="详细统计" align="center">
              <el-table-column prop="total" label="小计" width="90" align="center" />
              <el-table-column prop="amount" label="金额" width="100" align="center" />
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 模板说明：
 * 这是一个分步表单的新增/编辑组件模板
 * Step 1: 基础表单
 * Step 2: 列表明细与汇总
 */

// 引入通用组件
import ScanTipInput from '@commonlib/components/ScanTipInput/index.vue';
// 引入 hooks
import { useDeptTree } from '@blood-supply-department-web/hooks/useDeptTree'
import { useUserDeptPerson } from '@blood-supply-department-web/hooks/useUserDeptPerson'
// 引入 API
// import { yourApi } from '@blood-supply-department-web/api/yourApi'

// 注入依赖
const { proxy } = getCurrentInstance()
// 数据字典
const { dict } = useDict(['appointmentType'], (d) => {
  proxy.$forceUpdate()
})

// Hooks 调用示例
const { deptOptions, deptCascaderProps } = useDeptTree()
const { personOptions } = useUserDeptPerson()

// Props 定义
const props = defineProps({
  mode: { type: String, default: 'create' },
  formStep: { type: Object, required: true },
  activeStep: { type: Number, default: 1 },
})

const emit = defineEmits(['update:activeStep'])

// 内部状态
const scanCode = ref('')
const scannedList = ref([]) // 明细列表
const summaryData = ref([]) // 汇总列表

// 示例：扫码处理
const handleScan = async (code) => {
  if (!code) return
  try {
    // 模拟查询
    // const data = await api(code)
    const data = { donorCode: code, productName: '示例产品', state: '正常' }
    scannedList.value.push(data)
    rebuildSummaryData()
    scanCode.value = ''
    ElMessage.success('扫码成功')
  } catch (error) {
    ElMessage.error('扫码失败')
  }
}

const removeScannedItem = (index) => {
  scannedList.value.splice(index, 1)
  rebuildSummaryData()
}

// 示例：重建汇总数据 (请替换为实际业务逻辑)
const rebuildSummaryData = () => {
  // 简单汇总示例
  summaryData.value = scannedList.value.map((item, index) => ({
    index: index + 1,
    productName: item.productName,
    specification: '默认规格',
    total: 1,
    amount: 100
  }))
}

// 示例：表格合并逻辑
const objectSpanMethod = ({ row, column, rowIndex, columnIndex }) => {
  // 实现你的合并逻辑
  return { rowspan: 1, colspan: 1 }
}

// 示例：合计逻辑
const getSummaries = (param) => {
  const { columns, data } = param
  const sums = []
  columns.forEach((column, index) => {
    if (index === 0) {
      sums[index] = '合计'
      return
    }
    // 计算逻辑...
    sums[index] = ''
  })
  return sums
}

// 表单校验 (供父组件调用)
const validateForm = () => {
  // 简单校验示例
  if (!props.formStep.receiveDeptId) {
    return { isValid: false, errors: ['请选择用血机构'] }
  }
  return { isValid: true }
}

const validateList = () => {
  if (scannedList.value.length === 0) {
    return { isValid: false, errors: ['请至少添加一条明细'] }
  }
  return { isValid: true }
}

// 获取数据 (供父组件调用)
const getFormData1 = () => {
  return { formStep: props.formStep }
}

const getFormData2 = () => {
  return scannedList.value
}

// 暴露方法给父组件
defineExpose({
  validateForm,
  validateList,
  getFormData1,
  getFormData2
})

</script>

<!-- 引入公共样式 -->
<style src="./style.scss" lang="scss" scoped></style>
