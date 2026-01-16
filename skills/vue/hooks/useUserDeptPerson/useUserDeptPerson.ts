import { ref } from 'vue'
import { useUserStore } from '@/store'
import { getCreatorList } from '@blood-supply-department-web/api/sys'

export const useUserDeptPerson = () => {
  const personOptions = ref<Array<{ label: string; value: string }>>([])

  const fetchDeptPersons = async () => {
    try {
      const userStore = useUserStore()
      const deptId = (userStore.info as any)?.deptId as string | undefined
      if (!deptId) return

      const res = await getCreatorList(deptId)
      const list = Array.isArray(res) ? res : (res?.data || [])

      personOptions.value = (list || []).map((item: any) => ({
        label: item.nickName || item.name,
        value: String(item.id)
      }))
    } catch (error) {
      console.error('获取部门人员列表失败:', error)
    }
  }

  return {
    personOptions,
    fetchDeptPersons
  }
}
