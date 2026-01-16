// src/skills/useDeptTree.ts
import { ref, computed } from 'vue'
import { getDeptByUserIdList } from '@blood-supply-department-web/api/sys' // 假设你的接口路径

export function useDeptTree(initialDeptId = "1990755881964130306") {
    const deptId = ref(initialDeptId)
    const deptData = ref([])

    const normalizeDeptTree = (list) => {
        return (list || []).map((n) => ({
            value: n.id,
            label: n.name,
            children: n.children?.length ? normalizeDeptTree(n.children) : undefined
        }))
    }

    const deptOptions = computed(() => normalizeDeptTree(deptData.value))

    const getDeptData = async () => {
        try {
            const res = await getDeptByUserIdList({ deptId: deptId.value, containSelf: false })
            deptData.value = Array.isArray(res) ? res : (res?.data || [])
        } catch (err) {
            console.error("部门获取失败:", err)
        }
    }

    // 默认配置
    const deptCascaderProps = {
        value: 'value',
        label: 'label',
        children: 'children',
        emitPath: false,
        checkStrictly: true
    }

    return {
        deptId,
        deptOptions,
        deptCascaderProps,
        getDeptData
    }
}