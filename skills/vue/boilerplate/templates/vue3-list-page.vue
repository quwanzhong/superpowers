<template>
    <div class="page-container">
        <!-- 筛选区域 -->
        <div class="filter-header" :class="{ 'animate-in': animationVisible }">
            <div class="filter-left">
                <!-- 示例：输入框 -->
                <el-input class="inputBox" v-model="queryParams.keyword" placeholder="请输入关键字" clearable
                    @keyup.enter="handleSearch" />
                
                <!-- 示例：下拉选择 -->
                <!-- <el-select class="selectBox" v-model="queryParams.status" placeholder="请选择状态" clearable filterable>
                    <el-option v-for="item in dict.statusList" :key="item.value" :label="item.name" :value="item.value" />
                </el-select> -->
            </div>

            <div class="filter-right">
                <BaseButton btn-type="secondary" @click="handleReset">重置</BaseButton>
                <BaseButton btn-type="primary" @click="handleSearch">查询</BaseButton>
            </div>
        </div>

        <!-- 表格区域 -->
        <div class="tableBox" :class="{ 'animate-in': animationVisible }">
            <div class="list-header">
                <div class="tableTitle">列表标题</div>
                <div class="action-buttons">
                    <!-- 列设置 -->
                    <el-popover placement="bottom" width="auto" :visible-arrow="false"
                        popper-class="column-setting-popper" v-model:visible="showColumnSetting" trigger="manual">
                        <columnSetting v-if="showColumnSetting" :settings="columnSettings" @save="saveSetting"
                            @change="handleColumnChange" @reset="resetColumnSetting" @close="showColumnSetting = false">
                        </columnSetting>
                        <template #reference>
                            <BaseButton btn-type="secondary" custom-class="btn-column-setting"
                                @click="showColumnSetting = !showColumnSetting">
                                <template #icon>
                                    <div class="btn-icon icon-list"></div>
                                </template>
                                列设置
                            </BaseButton>
                        </template>
                    </el-popover>

                    <!-- 导出 -->
                    <BaseButton btn-type="secondary" @click="handleExport">
                        <template #icon>
                            <div class="btn-icon icon-export"></div>
                        </template>
                        导出
                    </BaseButton>

                    <!-- 新增 -->
                    <BaseButton btn-type="primary" @click="handleCreate">
                        <template #icon>
                            <div class="btn-icon icon-add"></div>
                        </template>
                        新增
                    </BaseButton>
                </div>
            </div>

            <!-- 数据表格 -->
            <el-table :data="tableData" class="base-table" height="100%"
                :class="`row-height-${columnSettings.rowHeightStyle || 'default'}`" v-loading="loading"
                @selection-change="handleSelectionChange">
                <el-table-column type="index" label="序号" width="80" align="center" />
                <el-table-column type="selection" width="55" align="center" />
                
                <el-table-column v-for="(col, index) in columnSettings.columns || []" :key="col.prop + '-' + index"
                    :prop="col.prop" :label="col.name" :fixed="col.fixed || false" :min-width="col.widths || 120"
                    :align="col.align || 'left'" show-overflow-tooltip>
                    <template #default="scope">
                        <!-- 字典格式化示例 -->
                        <span v-if="col.prop === 'status'">
                            {{ proxy.$dictFormatter(dict.statusList, scope.row[col.prop]) || "--" }}
                        </span>
                        
                        <!-- 状态标签示例 -->
                        <template v-if="col.prop === 'status'">
                            <div class="status-tag" :class="getStatusMeta(scope.row.status).className">
                                {{ getStatusMeta(scope.row.status).label || "--" }}
                            </div>
                        </template>
                        
                        <!-- 默认显示 -->
                        <span v-else>{{ scope.row[col.prop] !== undefined && scope.row[col.prop] !== null &&
                            scope.row[col.prop] !== '' ? scope.row[col.prop] : '--' }}</span>
                    </template>
                </el-table-column>

                <el-table-column label="操作" width="200" align="center" fixed="right">
                    <template #default="{ row }">
                        <div class="button-flex">
                            <BaseButton btn-type="table" status="view" @click="handleView(row)">查看</BaseButton>
                            <BaseButton btn-type="table" status="edit" @click="handleEdit(row)">编辑</BaseButton>
                            <BaseButton btn-type="table" status="delete" @click="handleDel(row)">删除</BaseButton>
                        </div>
                    </template>
                </el-table-column>
            </el-table>

            <!-- 分页 -->
            <div class="paginationBox">
                <div class="paginationText">
                    显示第 {{ pageInfo.start }}-{{ pageInfo.end }} 条，共 {{ total }} 条记录
                </div>
                <el-pagination v-model:current-page="queryParams.pageNum" v-model:page-size="queryParams.pageSize"
                    :page-sizes="[10, 20, 50, 100]" :total="total" layout="sizes, prev, pager, next, jumper" background
                    @size-change="handleSizeChange" @current-change="handleCurrentChange" />
            </div>
        </div>

        <!-- 弹窗/抽屉组件 -->
        <!-- <FormDrawer v-model:visible="drawerVisible" :mode="drawerMode" :record="drawerRecord" @fresh="handleRefresh" v-if="drawerVisible" /> -->

        <!-- 导出配置 -->
        <exportConfig :columns="exportColumns" v-model:show="showExportConfig" @save="handleExportFields">
        </exportConfig>
    </div>
</template>

<script setup>
/**
 * 模板说明：
 * 这是一个通用的 Vue3 列表页面模板，包含：
 * 1. 顶部筛选栏（Filter Header）
 * 2. 表格区域（Table Box）
 *    - 列设置（Column Setting）
 *    - 导出（Export）
 *    - 新增（Add）
 *    - 表格展示（Table）
 *    - 分页（Pagination）
 * 3. 基础 CRUD 逻辑（Create, Read, Update, Delete）
 * 
 * 使用步骤：
 * 1. 复制本文件到目标目录
 * 2. 修改 API 导入路径
 * 3. 配置数据字典（useDict）
 * 4. 修改 defaultColumns 定义表格列
 * 5. 修改 queryParams 定义查询条件
 * 6. 实现/替换 fetchDataList, deleteItem 等业务方法
 */

import { TableColSetting } from '@blood-supply-department-web/utils/tableColSetting.js'
import { downloadFile } from '@commonlib/api/tool.js';
import ColumnSetting from '@commonlib/components/ColumnSetting/index.vue'
import exportConfig from '@commonlib/components/exportConfig/index.vue'

// 导入 API (请替换为实际 API)
// import { getList, deleteItem } from '@blood-supply-department-web/api/yourApi';

// =====================  数据字典  ===================
const { proxy } = getCurrentInstance()
const { dict } = useDict(['bloodUnit'], (d) => {})

// ===================== 页面相关 ==================
// 进场动画开关
const animationVisible = ref(false)

// ===================== 列设置相关 ==================
const route = useRoute()
const showColumnSetting = ref(false)

// 列设置默认配置 (请根据实际业务修改)
const defaultColumns = reactive({
    rowHeightStyle: 'default',
    columns: [
        { prop: 'code', name: '编号', isShow: true, fixed: '', widths: 180, align: 'center' },
        { prop: 'name', name: '名称', isShow: true, fixed: '', widths: 180, align: 'center' },
        { prop: 'status', name: '状态', isShow: true, fixed: '', widths: 120, align: 'center' },
        { prop: 'createTime', name: '创建时间', isShow: true, fixed: '', widths: 180, align: 'center' },
        { prop: 'remark', name: '备注', isShow: true, fixed: '', widths: 200, align: 'center' },
    ]
})
const originColumns = ref({})
const columnSettings = ref({})

// 获取账户配置
const getAccountConfig = async () => {
    const res = await TableColSetting.get(route.path)
    if (res) {
        const defaultColumnsMap = new Map()
        defaultColumns.columns.forEach(col => {
            defaultColumnsMap.set(col.prop, col)
        })

        const mergedColumns = []

        if (res.columns) {
            res.columns.forEach(savedCol => {
                const defaultCol = defaultColumnsMap.get(savedCol.prop)
                if (defaultCol) {
                    mergedColumns.push({
                        ...defaultCol,
                        isShow: savedCol.isShow !== undefined ? savedCol.isShow : defaultCol.isShow,
                        fixed: savedCol.fixed !== undefined ? savedCol.fixed : defaultCol.fixed
                    })
                    defaultColumnsMap.delete(savedCol.prop)
                }
            })
        }

        defaultColumnsMap.forEach(defaultCol => {
            mergedColumns.push({ ...defaultCol })
        })

        const mergedConfig = {
            columns: mergedColumns,
            rowHeightStyle: res.rowHeightStyle || defaultColumns.rowHeightStyle
        }

        columnSettings.value = mergedConfig
        originColumns.value = mergedConfig
    } else {
        columnSettings.value = defaultColumns
        originColumns.value = defaultColumns
    }
}

// 列设置变化处理
const handleColumnChange = (newConfig) => {
    columnSettings.value = { ...columnSettings.value, ...newConfig }
}

// 列设置重置
const resetColumnSetting = () => {
    columnSettings.value = JSON.parse(JSON.stringify(originColumns.value))
}

// 保存列设置
const saveSetting = async () => {
    await TableColSetting.set(route.path, columnSettings.value)
    showColumnSetting.value = false
    ElMessage.success('保存成功')
}


// ===================== 导出 ==================
const exportColumns = ref([])
const showExportConfig = ref(false)

const handleExport = async () => {
    exportColumns.value = columnSettings.value.columns
    showExportConfig.value = true
}

const handleExportFields = async (fields) => {
    const nameToPropMap = {}
    exportColumns.value.forEach(col => {
        nameToPropMap[col.name] = col.prop
    })
    const selectedProps = fields.map(name => nameToPropMap[name])
    const params = {
        tableName: '列表导出', // 修改导出文件名
        fieldNames: selectedProps,
        size: -1,
        current: 1,
        ...queryParams // 包含查询条件
    }
    try {
        const fileName = `列表导出_${new Date().toISOString().slice(0, 10)}`
        // await downloadFile('/api/path/export', params, fileName) // 修改导出接口
        ElMessage.success('导出功能需配置接口')
        showExportConfig.value = false
    } catch (error) {
        console.error('导出失败:', error)
        ElMessage.error('导出失败，请重试')
        showExportConfig.value = false
    }
}


// ===================== 核心业务 ==================
const tableData = ref([])
const loading = ref(false)
const total = ref(0)

// 查询参数 (请根据实际业务修改)
const queryParams = reactive({
    pageNum: 1,
    pageSize: 10,
    keyword: '',
    status: ''
})

// 清除筛选条件
const handleClearFilter = () => {
    queryParams.keyword = ''
    queryParams.status = ''
}

const selectedRows = ref([])
const handleSelectionChange = (selection) => {
    selectedRows.value = selection
}

const handleSizeChange = (size) => {
    queryParams.pageSize = size
    queryParams.pageNum = 1
    handleSearch()
}

const handleCurrentChange = (page) => {
    queryParams.pageNum = page
    fetchDataList()
}

// 分页信息
const pageInfo = computed(() => {
    const start = (queryParams.pageNum - 1) * queryParams.pageSize + 1
    const end = Math.min(queryParams.pageNum * queryParams.pageSize, total.value)
    return { start: total.value > 0 ? start : 0, end }
})

const handleReset = () => {
    handleClearFilter()
    queryParams.pageNum = 1
    handleSearch()
}

const handleSearch = () => {
    tableData.value = []
    queryParams.pageNum = 1
    fetchDataList()
}

// 弹窗状态
const drawerVisible = ref(false)
const drawerMode = ref('create')
const drawerRecord = ref({})

// 查看
const handleView = (row) => {
    drawerMode.value = 'view'
    drawerRecord.value = row
    drawerVisible.value = true
}

// 编辑
const handleEdit = (row) => {
    drawerMode.value = 'edit'
    drawerRecord.value = row
    drawerVisible.value = true
}

// 删除
const handleDel = (row) => {
    ElMessageBox.confirm('确定删除该数据吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
    }).then(async () => {
        try {
            // const res = await deleteItem(row.id)
            // if (res) {
            //     fetchDataList()
            //     ElMessage.success("操作成功")
            // }
            ElMessage.success("删除功能需配置接口")
        } catch (error) {
            ElMessage.error("删除失败")
        }
    })
}

// 新增
const handleCreate = () => {
    drawerMode.value = 'create'
    drawerRecord.value = {}
    drawerVisible.value = true
}

const handleRefresh = () => {
    fetchDataList()
}

// 获取列表数据
const fetchDataList = async () => {
    loading.value = true
    try {
        // 模拟数据
        setTimeout(() => {
            tableData.value = [
                { id: 1, code: 'TEST001', name: '测试数据1', status: '1', createTime: '2023-01-01', remark: '这是测试数据' },
                { id: 2, code: 'TEST002', name: '测试数据2', status: '0', createTime: '2023-01-02', remark: '这是测试数据' },
            ]
            total.value = 20
            loading.value = false
        }, 500)
        
        // 实际接口调用
        /*
        const params = { ...queryParams }
        const res = await getList(params);
        if (res) {
            tableData.value = res.records || []
            total.value = Number(res.total) || 0
        }
        */
    } catch (error) {
        console.error('获取列表失败:', error);
        ElMessage.error('获取列表失败');
        loading.value = false
    }
};

const getStatusMeta = (type) => {
    // 示例状态样式逻辑
    const label = type === '1' ? '启用' : '禁用'
    const className = type === '1' ? 'tag-normal' : 'tag-danger'
    return { label, className }
}


onMounted(async () => {
    await getAccountConfig()
    fetchDataList()
    nextTick(() => {
        animationVisible.value = true
    })
})

</script>

<style lang="scss" scoped>
.page-container {
    padding: 16px;
    background-color: var(--box_bgc);
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 16px;
    font-size: 16px;
    overflow: hidden;

    .filter-header {
        background-color: var(--logistics-card-bg);
        border-radius: 20px;
        padding: 20px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid var(--logistics-card-border);
        box-shadow: 0px 2px 20px var(--logistics-card-shadow);
    }

    .tableBox {
        flex: 1;
        height: 0;
        display: flex;
        flex-direction: column;
        background-color: var(--logistics-card-bg);
        border-radius: 20px;
        padding: 20px 30px;
        border: 1px solid var(--logistics-card-border);
        box-shadow: 0px 2px 20px var(--logistics-card-shadow);
    }

    .filter-left {
        display: flex;
        gap: 12px;
        align-items: center;
    }

    .filter-right {
        display: flex;
        gap: 12px;
    }

    .list-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .status-tag {
        display: inline-block;
        padding: 4px 16px;
        border-radius: 12px;
        font-size: 16px;
        line-height: 20px;
        text-align: center;
        min-width: 60px;

        &.tag-danger {
            background-color: #D32F2F30;
            color: #D32F2F;
        }

        &.tag-warning {
            background-color: #FA8C0530;
            color: #F08400;
        }

        &.tag-normal {
            background-color: #2C70DE30;
            color: #2C70DE;
        }
    }
}
</style>
