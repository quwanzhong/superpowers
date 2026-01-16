<template>
  <div class="drawer-container des_scrollbar">
    <!-- 顶部状态栏 -->
    <div class="order-top theme-grid-row-2 flex-row jus-bet">
      <div>
        <span class="order-top-title">单号：</span>
        <span class="order-top-content">{{ showInfo?.code || '--' }}</span>
      </div>
      <div>
        <span class="order-top-title">状态：</span>
        <span class="order-top-content">{{ proxy.$dictFormatter(dict.status, showInfo?.status) || '--' }}</span>
      </div>
    </div>

    <div class="section-root">
      <!-- 基本信息 -->
      <div class="theme-title">基本信息</div>
      <div class="section-content">
        <div class="theme-grid-row-3 info-grid-padding" style="padding:0;gap: 20px;">
          <div class="theme-grid-row-item">
            <span>用血机构：</span>
            <span class="theme-grid-value">{{ recordInfo?.receiveDeptName || '--' }}</span>
          </div>
          <div class="theme-grid-row-item">
            <span>预约方式：</span>
            <span class="theme-grid-value">{{ proxy.$dictFormatter(dict.appointmentType, showInfo?.appointmentType) || '--' }}</span>
          </div>
          <div class="theme-grid-row-item">
            <span>创建时间：</span>
            <span class="theme-grid-value">{{ showInfo?.createTime || '--' }}</span>
          </div>
          <div class="theme-grid-row-item" style="grid-column: span 3;">
            <span>备注：</span>
            <span class="theme-grid-value">{{ showInfo?.remark || '--' }}</span>
          </div>
        </div>
      </div>

      <!-- 明细列表 -->
      <div class="order-middle">
        <div class="theme-title" style="margin-top: 10px;">已登记明细</div>
        <div>
          <el-table :data="showInfo?.detailList || []" class="base-table" border>
            <el-table-column type="index" width="60" label="序号" align="center">
              <template #default="{ $index }">
                {{ ($index + 1).toString().padStart(2, '0') }}
              </template>
            </el-table-column>
            <el-table-column prop="donorCode" label="编码" min-width="180" align="center" />
            <el-table-column prop="productName" label="名称" align="center" />
            <el-table-column prop="volume" label="数量" width="120" align="center" />
          </el-table>
        </div>
      </div>

      <!-- 汇总表格 -->
      <div class="order-middle">
        <div class="theme-title">统计汇总表</div>
        <div class="summary-table">
          <el-table class="base-table" :data="summaryData" border show-summary :summary-method="getSummaries">
            <el-table-column prop="index" label="序号" width="80" align="center" />
            <el-table-column prop="productName" label="类别" min-width="140" align="center" />
            <el-table-column prop="total" label="小计" width="90" align="center" />
            <el-table-column prop="amount" label="金额" width="100" align="center" />
          </el-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 模板说明：
 * 这是一个只读详情页组件模板
 * 用于展示 `index.vue` 传入的 `showInfo` 数据
 */

const recordInfo = inject('recordInfo', {}) // 注入父组件提供的上下文信息

const { proxy } = getCurrentInstance()
const { dict } = useDict(['status', 'appointmentType'], (d) => {
  proxy.$forceUpdate()
})

const props = defineProps({
  showInfo: {
    type: Object,
    default: () => ({})
  },
})

// 汇总数据逻辑 (根据 showInfo 自动计算)
const summaryData = ref([])

const rebuildSummaryData = (val) => {
  if (!val || !Array.isArray(val)) return
  // 示例汇总逻辑
  summaryData.value = val.map((item, index) => ({
    index: index + 1,
    productName: item.productName,
    total: 1,
    amount: 100
  }))
}

// 监听数据变化更新汇总
watch(() => props.showInfo?.detailList, (val) => {
  rebuildSummaryData(val)
}, { deep: true, immediate: true })

// 合计逻辑
const getSummaries = (param) => {
  const { columns } = param
  const sums = []
  columns.forEach((column, index) => {
    if (index === 0) {
      sums[index] = '合计'
      return
    }
    sums[index] = ''
  })
  return sums
}

</script>

<style src="./style.scss" lang="scss" scoped></style>

<style lang="scss" scoped>
.info-grid-padding {
  :deep(.theme-grid-row-item) {
    display: flex;
    align-items: center;
    padding: 0px 10px !important;

    span {
      font-size: 18px !important;
    }
  }
}
</style>
