# Android Single-Activity（来自 blooddonationterminalapp/app 的可复用架构总结）

## 目标

将一个典型的 **Single-Activity + 多 Fragment + ViewModel(LiveData) + Retrofit/OkHttp** 的工程组织方式沉淀为可复用的模板说明，便于你在后续项目快速套用。

本总结基于：`/Users/qwz/yzkj/blooddonationterminalapp/app`。

---

## 1. 项目入口与全局初始化

- **Application**：`KtApplication`
  - 初始化：Toast、SP、Crash、AutoSize、多进程生命周期回调、音效资源等
  - 全局单例：`KtApplication.application`

- **Launcher Activity**：`SplashActivity`
  - `AndroidManifest.xml` 中声明为 `MAIN/LAUNCHER`
  - 通常负责：启动页、权限预检查/跳转到主界面

- **主 Activity（Single-Activity 宿主）**：`MainActivity`
  - 负责 Fragment 容器（`replaceFragment`）
  - 负责全局 UI（顶部状态、步骤条/菜单、网络断开遮罩等）
  - 负责硬件/服务绑定（如 AromeClient）、EventBus 注册、双屏展示等
  - 通过 `MainViewModel` 统一管理“流程状态/用户状态/字典数据/网络请求结果”

---

## 2. 分层与职责（可复用的最小分层）

> 该项目没有显式 Repository 层，主要是 **UI -> ViewModel -> ApiServer** 的直连形态。复用时可保留或按需补一层 Repository。

### 2.1 UI 层

- `MainActivity`：承载容器和全局 UI、统一导航
- `Fragment`：具体页面（例如首页、识别页、登记流程页等）
- `dialog/`：弹窗以 `DialogFragment` 为主
- `adapter/`：RecyclerView / ViewPager 适配器
- `viewStep/`：流程分步页面（FlowStepOne~Seven）

### 2.2 状态/业务协调层（ViewModel）

- `MainViewModel`：全局共享状态（Activity 级别）
  - 步骤状态：`mStepIndex`
  - 用户/流程状态：`mUserInfo`、`mFlowId`、`mUserId`、`mNode`
  - 字典数据：`dictSLiveData` + `isDictDataReady` + `invokeOnDictDataReady()`
  - 业务开关/页面决策：`mShowBloodType`、`mSwitchQr` 等
  - 网络请求结果：`identifyInfoResult`、`mBloodTypeList` 等

- 各步骤 ViewModel（如存在）：例如 `FlowStepTwoViewModel`、`FlowStepFourViewModel`…
  - 更偏向“页面内”数据加载与状态（例如五级联动地区数据）

### 2.3 网络层

- Retrofit 创建：`net/RetrofitNet`
  - OkHttpClient：超时、连接池、拦截器（日志、鉴权、Header、SSL）
- API 接口：`api/ApiServer`（业务接口）、`SystemServer`、`LoginServer`
- 统一响应体：`net/BaseResponse`

---

## 3. 导航与流程编排（项目的关键可复用点）

### 3.1 单 Activity + Fragment 替换

- 核心方式：`replaceFragment(containerId, fragment, tag)`（见 `utils/Expand.kt`）
- `MainActivity` 提供一组 `goXXXFrgm()` 方法统一跳转

### 3.2 “步骤驱动”的流程页面

- `MainViewModel.mStepIndex` 作为流程驱动变量
- `MainActivity` 监听 `mStepIndex`，调用 `navigateToStep(step)`，再进入对应 Fragment（Step1~Step7）

**建议复用的约定**：
- `mStepIndex` 只表达“流程步骤”，不要和“是否显示首页 Fragment”混用
- 首页跳转建议独立成 `showHomeView()/goHomeFrgm()`，避免把 `step=0` 既当首页又当某个流程页

---

## 4. 数据流（推荐你复用的写法）

### 4.1 典型数据流

- **UI 事件**（点击/扫码/识别回调）
  -> **ViewModel 发起请求**（`viewModelScope.launch`）
  -> **ApiServer Retrofit**
  -> **LiveData postValue/value 更新**
  -> **Fragment/Activity observe** 更新 UI 或导航

### 4.2 字典数据就绪回调模式（值得复用）

- `MainViewModel` 使用 `isDictDataReady` + `invokeOnDictDataReady {}`
- 优点：避免多个 Fragment 自己轮询/判断字典数据是否加载完成

---

## 5. 目录结构（以本项目为样例的可复用约定）

建议你后续项目继续沿用类似分包：

- `api/`：Retrofit 接口定义（按业务域拆分）
- `net/`：Retrofit/OkHttp 初始化、拦截器、统一响应体
- `bean/`：数据模型（DTO/VO）
- `utils/`：通用工具（扩展方法、SP、加密、时间、UI 小组件封装）
- `dialog/`：DialogFragment
- `adapter/`：RecyclerView/ViewPager 适配器
- `viewStep/`：流程型页面（按 step 拆分）
- `viewmodel/`：非流程、业务域 ViewModel（如果有）
- `view/`：自定义 View
- `widget/`：小组件

---

## 6. 网络层可复用清单

- `RetrofitNet`：统一创建 Retrofit
- `AuthInterceptor`：登录 token/鉴权
- `HeaderInterceptor`：统一 Header（设备信息/版本等）
- `LoggingInterceptor` + `LogNetInterceptor`：日志
- `SSLSocketClient`：自定义 SSL（如你后续不需要可删）

复用建议：
- 把 `baseUrl` 等配置集中在 `BuildConfigField` + `UrlConstant`
- 统一 `BaseResponse`，并在 ViewModel 层做 `isSuccess()` 判断与错误消息透传

---

## 7. UI/交互层可复用清单

- `utils/Expand.kt`
  - `replaceFragment`/`provider(ViewModelProvider)`
  - 各种扩展（toast、debounce click 等）
- `utils/DropdownSelector` / `DropdownAddressSelector`
  - 下拉选择、五级联动/智能搜索
- `NetworkStateReceiver`
  - 网络状态观察（注意：网络变化触发导航时要避免打断流程）

---

## 8. 迁移到新项目的步骤（推荐）

- **基础**
  - 拷贝 `net/` + `api/` + `BaseResponse`
  - 拷贝 `utils/Expand.kt` + 你常用的 util
  - 建立 `MainActivity` 作为宿主 + `MainViewModel` 全局状态

- **核心逻辑**
  - 决定是否继续使用“stepIndex 驱动流程”的模式
  - 若使用：统一把导航入口收口在 `MainActivity.navigateToStep()`

- **集成**
  - 替换 `BuildConfigField(BASE_URL...)` 与 token 存储逻辑
  - 按业务拆 `api/*Server.kt`

- **优化**
  - 若业务复杂：补 `repository/`（VM 不直接碰 ApiServer）

---

## 9. 本项目中你需要留意的“坑位”（复用时避免）

- **LiveData 重复触发导致导航/请求循环**：
  - 当 ViewModel 的某个 LiveData 同时被多个 Fragment/Activity 监听时，谨慎在回调中做导航/二次请求

- **网络恢复触发自动回首页**：
  - 如果流程进行中，网络恢复不应强制回首页（容易打断流程）

- **全局状态清理**：
  - 流程结束时需要系统性 `clearFlowInfo()`，避免残留数据导致新 Fragment 立即触发 observe

---

## 10. 你想要的输出形态（下一步可补充）

如果你希望这里变成“可直接拷贝的模板工程”，我可以再补：
- 一个最小可运行的骨架（MainActivity + HomeFragment + BaseVM + RetrofitNet）
- 标准化的包结构与命名约定
- 一套通用的导航与流程状态管理范式
