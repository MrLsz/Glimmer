# Binder Framework 层分析

> Binder 在 Java Framework 层通过 JNI 桥接到 Native 层的 C/S 架构（Binder/BinderProxy ↔ BBinder/BpBinder），向上为应用提供 ServiceManager API、AIDL 编译机制和完整的跨进程调用能力。本文覆盖 JNI 注册表、Java 层 ServiceManager 全链路封装、Java ↔ Native Binder 对象转换（javaObjectForIBinder / ibinderForJavaObject）、以及完整的 addService/getService 调用链。

## 目录

- [一、Framework 层源码文件与核心类](#一framework-层源码文件与核心类)
- [二、Binder JNI 初始化](#二binder-jni-初始化)
  - [2.1 Zygote 启动时的 gRegJNI](#21-zygote-启动时的-gregjni)
  - [2.2 register_android_os_Binder：Binder 类 JNI](#22-register_android_os_binderbinder-类-jni)
  - [2.3 register_android_os_BinderProxy：BinderProxy 类 JNI](#23-register_android_os_binderproxybinderproxy-类-jni)
  - [2.4 register_android_os_BinderInternal](#24-register_android_os_binderinternal)
- [三、Java 层 ServiceManager 封装](#三java-层-servicemanager-封装)
  - [3.1 getIServiceManager：单例获取 SM 代理](#31-getiservicemanager单例获取-sm-代理)
  - [3.2 getContextObject → javaObjectForIBinder](#32-getcontextobject--javaobjectforibinder)
  - [3.3 ServiceManagerNative.asInterface → ServiceManagerProxy](#33-servicemanagernativeasinterface--servicemanagerproxy)
- [四、服务注册：Java → Native 全链路](#四服务注册java--native-全链路)
  - [4.1 ServiceManagerProxy.addService](#41-servicemanagerproxyaddservice)
  - [4.2 Java writeStrongBinder → ibinderForJavaObject](#42-java-writestrongbinder--ibinderforjavaobject)
  - [4.3 JavaBBinderHolder → JavaBBinder（Java Binder → C++ BBinder 桥）](#43-javabinderholder--javabinderjava-binder--c-bbinder-桥)
  - [4.4 Parcel.writeStrongBinder(C++) → flatten_binder](#44-parcelwritestrongbinderc--flatten_binder)
  - [4.5 BinderProxy.transact → BpBinder::transact（JNI 桥）](#45-binderproxytransact--bpbindertransactjni-桥)
- [五、服务获取：Java → Native 全链路](#五服务获取java--native-全链路)
  - [5.1 ServiceManager.getService](#51-servicemanagergetservice)
  - [5.2 ServiceManagerProxy.getService](#52-servicemanagerproxygetservice)
  - [5.3 readStrongBinder → javaObjectForIBinder（返回为 BinderProxy）](#53-readstrongbinder--javaobjectforibinder返回为-binderproxy)
- [六、关键总结](#六关键总结)

---

## 一、Framework 层源码文件与核心类

Framework 层 Binder 涉及的核心源文件分布在 Java 和 JNI 两层。

<img src="./images/binder-doc9-01.png" width="500" alt="Binder 分层架构">

Java 层与 Native 层架构对应关系如下：

```text
framework/base/core/java/android/os/
  ├── IBinder.java              # 跨进程通信顶层接口（FLAG_ONEWAY, DeathRecipient）
  ├── Binder.java               # 服务端基类（含内部类 BinderProxy）
  ├── Parcel.java               # 数据序列化容器
  ├── IInterface.java           # 业务接口基类
  ├── IServiceManager.java      # ServiceManager 业务接口
  ├── ServiceManager.java       # 对外 API：getService / addService
  └── ServiceManagerNative.java # 含 ServiceManagerProxy 代理类

framework/base/core/jni/
  ├── AndroidRuntime.cpp        # startReg → gRegJNI 注册入口
  ├── android_util_Binder.cpp   # Binder/BinderProxy/BinderInternal JNI 实现
  └── android_os_Parcel.cpp     # Parcel JNI 实现
```

Java 层架构与 Native 层一一对应：

| Java 层 | Native 层 | 角色 |
|---------|----------|------|
| `IBinder` 接口 | `IBinder` 抽象类 | 跨进程通信顶层接口 |
| `Binder` | `BBinder` | 服务端基类 |
| `BinderProxy` | `BpBinder` | 客户端代理 |
| `Parcel` | `Parcel` | 数据序列化 |
| `IInterface` | `IInterface` | 业务接口基类 |
| `ServiceManager` | `IServiceManager` | SM 对外 API |

---

## 二、Binder JNI 初始化

Binder 的 Java API 通过 JNI 桥接到 Native 层——这个桥在 Zygote 启动时一次性建立，所有 App 进程通过 COW 继承。

### 2.1 Zygote 启动时的 gRegJNI

Zygote 在创建 ART 虚拟机后，调用 `AndroidRuntime::startReg` 注册所有 framework 类的 JNI 方法——其中与 Binder 相关的注册项为 `REG_JNI(register_android_os_Binder)`。核心入口代码：

```cpp
// frameworks/base/core/jni/AndroidRuntime.cpp
int AndroidRuntime::startReg(JNIEnv* env) {
    // gRegJNI 是静态数组，含上百个 framework 类的 JNI 注册项
    if (register_jni_procs(gRegJNI, NELEM(gRegJNI), env) < 0) {
        return -1;
    }
    return 0;
}
```

与 Binder 相关的注册项：`REG_JNI(register_android_os_Binder)`——触发 Binder/BinderProxy/BinderInternal 三类 JNI 注册。

### 2.2 register_android_os_Binder：Binder 类 JNI

`register_android_os_Binder` 是 Binder JNI 注册的总入口——内部依次注册 Binder、BinderInternal、BinderProxy 三个类的 JNI 方法。`int_register_android_os_Binder` 负责缓存 Binder 类的信息到 `gBinderOffsets` 并注册 native 方法映射表：

```cpp
// android_util_Binder.cpp
int register_android_os_Binder(JNIEnv* env) {
    if (int_register_android_os_Binder(env) < 0)         return -1;
    if (int_register_android_os_BinderInternal(env) < 0) return -1;
    if (int_register_android_os_BinderProxy(env) < 0)    return -1;
    return 0;
}
```

**int_register_android_os_Binder**：

```cpp
static int int_register_android_os_Binder(JNIEnv* env) {
    jclass clazz = FindClassOrDie(env, "android/os/Binder");

    // 缓存 Java 类信息到全局结构体 gBinderOffsets
    gBinderOffsets.mClass        = MakeGlobalRefOrDie(env, clazz);
    gBinderOffsets.mExecTransact = GetMethodIDOrDie(env, clazz, "execTransact", "(IJJI)Z");
    gBinderOffsets.mObject       = GetFieldIDOrDie(env, clazz, "mObject", "J");

    return RegisterMethodsOrDie(env, "android/os/Binder", gBinderMethods,
                                NELEM(gBinderMethods));
}
```

`gBinderOffsets` 结构体：

```cpp
static struct bindernative_offsets_t {
    jclass mClass;              // Binder 类
    jmethodID mExecTransact;    // execTransact() 方法
    jfieldID mObject;           // mObject 属性（存储 C++ BBinder 指针的 long 值）
} gBinderOffsets;
```

> `FindClassOrDie` / `MakeGlobalRefOrDie` / `GetMethodIDOrDie` 分别等价于 `env->FindClass` / `env->NewGlobalRef` / `env->GetMethodID`——缓存后无需每次 JNI 调用都重新查找，大幅提升效率。

`gBinderMethods` 注册的 native 方法映射：

```cpp
static const JNINativeMethod gBinderMethods[] = {
    {"getCallingPid",            "()I",  android_os_Binder_getCallingPid},
    {"getCallingUid",            "()I",  android_os_Binder_getCallingUid},
    {"clearCallingIdentity",     "()J",  android_os_Binder_clearCallingIdentity},
    {"restoreCallingIdentity",   "(J)V", android_os_Binder_restoreCallingIdentity},
    {"setThreadStrictModePolicy","(I)V", android_os_Binder_setThreadStrictModePolicy},
    {"getThreadStrictModePolicy","()I",  android_os_Binder_getThreadStrictModePolicy},
    {"flushPendingCommands",     "()V",  android_os_Binder_flushPendingCommands},
    {"init",                     "()V",  android_os_Binder_init},
    {"destroy",                  "()V",  android_os_Binder_destroy},
    {"blockUntilThreadAvailable","()V",  android_os_Binder_blockUntilThreadAvailable},
};
```

> 双向桥梁：`gBinderOffsets` 使 JNI 层可访问 Java 层的 Binder 类信息（mObject/execTransact）；`gBinderMethods` 使 Java 层可以调用 JNI 层的 native 方法。

### 2.3 register_android_os_BinderProxy：BinderProxy 类 JNI

`int_register_android_os_BinderProxy` 缓存 BinderProxy 类的构造方法、`mObject`/`mSelf`/`mOrgue` 字段到 `gBinderProxyOffsets`，并注册 7 个 native 方法。这些字段是 Java ↔ C++ BinderProxy 转换的基础：

```cpp
static int int_register_android_os_BinderProxy(JNIEnv* env) {
    jclass clazz = FindClassOrDie(env, "android/os/BinderProxy");

    gBinderProxyOffsets.mClass            = MakeGlobalRefOrDie(env, clazz);
    gBinderProxyOffsets.mConstructor      = GetMethodIDOrDie(env, clazz, "<init>", "()V");
    gBinderProxyOffsets.mSendDeathNotice  = GetStaticMethodIDOrDie(env, clazz, "sendDeathNotice", "...");
    gBinderProxyOffsets.mObject           = GetFieldIDOrDie(env, clazz, "mObject", "J");
    gBinderProxyOffsets.mSelf             = GetFieldIDOrDie(env, clazz, "mSelf", "...");
    gBinderProxyOffsets.mOrgue            = GetFieldIDOrDie(env, clazz, "mOrgue", "J");

    return RegisterMethodsOrDie(env, "android/os/BinderProxy",
                                gBinderProxyMethods, NELEM(gBinderProxyMethods));
}
```

`gBinderProxyMethods` 注册的核心方法：

```cpp
static const JNINativeMethod gBinderProxyMethods[] = {
    {"pingBinder",              "()Z",    android_os_BinderProxy_pingBinder},
    {"isBinderAlive",           "()Z",    android_os_BinderProxy_isBinderAlive},
    {"getInterfaceDescriptor",  "()...",  android_os_BinderProxy_getInterfaceDescriptor},
    {"transactNative",          "(IL...;)Z", android_os_BinderProxy_transact},
    {"linkToDeath",             "(L...;)V", android_os_BinderProxy_linkToDeath},
    {"unlinkToDeath",           "(L...;)Z", android_os_BinderProxy_unlinkToDeath},
    {"destroy",                 "()V",    android_os_BinderProxy_destroy},
};
```

### 2.4 register_android_os_BinderInternal

`int_register_android_os_BinderInternal` 注册 BinderInternal 类的 JNI 方法——其中最核心的是 `getContextObject`，后续 ServiceManager 获取依赖它：

```cpp
static int int_register_android_os_BinderInternal(JNIEnv* env) {
    jclass clazz = FindClassOrDie(env, "com/android/internal/os/BinderInternal");
    gBinderInternalOffsets.mClass   = MakeGlobalRefOrDie(env, clazz);
    gBinderInternalOffsets.mForceGc = GetStaticMethodIDOrDie(env, clazz, "forceBinderGc", "()V");
    return RegisterMethodsOrDie(env, kBinderInternalPathName,
                                gBinderInternalMethods, NELEM(gBinderInternalMethods));
}

static const JNINativeMethod gBinderInternalMethods[] = {
    {"getContextObject",             "()...", android_os_BinderInternal_getContextObject},
    {"joinThreadPool",               "()V",   android_os_BinderInternal_joinThreadPool},
    {"disableBackgroundScheduling",  "(Z)V",  android_os_BinderInternal_disableBackgroundScheduling},
    {"handleGc",                     "()V",   android_os_BinderInternal_handleGc},
};
```

---

## 三、Java 层 ServiceManager 封装

ServiceManager 在 Java 层的封装链路是理解整个 Framework 层的入口——从 `getIServiceManager()` 单例获取开始，经 `getContextObject()` 的 JNI 转换，最终落到 `ServiceManagerProxy` 代理对象。本章按调用顺序拆解这三步。

### 3.1 getIServiceManager：单例获取 SM 代理

`ServiceManager.getIServiceManager()` 采用单例模式获取 SM 代理——首次调用时通过 `BinderInternal.getContextObject()` 和 `ServiceManagerNative.asInterface()` 构造 `ServiceManagerProxy`。完整代码：

```java
// frameworks/base/core/java/android/os/ServiceManager.java
private static IServiceManager getIServiceManager() {
    if (sServiceManager != null) return sServiceManager;

    sServiceManager = ServiceManagerNative.asInterface(
        BinderInternal.getContextObject()   // → native → BpBinder(0)
    );
    return sServiceManager;
}
```

> `getIServiceManager` 采用单例模式——返回的是 `ServiceManagerProxy` 对象（SMP）。

### 3.2 getContextObject → javaObjectForIBinder

`BinderInternal.getContextObject()` 是 native 方法，JNI 实现：

```cpp
// android_util_Binder.cpp
static jobject android_os_BinderInternal_getContextObject(JNIEnv* env, jobject clazz) {
    sp<IBinder> b = ProcessState::self()->getContextObject(NULL);  // → BpBinder(0)
    return javaObjectForIBinder(env, b);  // ★ 将 C++ BpBinder 转为 Java BinderProxy
}
```

**javaObjectForIBinder**：C++ IBinder → Java BinderProxy 转换的核心函数：

```cpp
jobject javaObjectForIBinder(JNIEnv* env, const sp<IBinder>& val) {
    if (val == NULL) return NULL;

    // 检查是否为 JavaBBinder（Java 层的 Binder 对应的 C++ 对象）
    if (val->checkSubclass(&gBinderOffsets)) {
        return static_cast<JavaBBinder*>(val.get())->object();
    }

    AutoMutex _l(mProxyLock);

    // 先尝试从缓存查找：用 val->findObject 查询已创建的 BinderProxy
    jobject object = (jobject)val->findObject(&gBinderProxyOffsets);
    if (object != NULL) {
        jobject res = jniGetReferent(env, object);
        if (res != NULL) return res;  // 找到了，直接返回
        // 已被 GC 回收，清理旧引用
        val->detachObject(&gBinderProxyOffsets);
        env->DeleteGlobalRef(object);
    }

    // ★ 创建新的 BinderProxy 对象
    object = env->NewObject(gBinderProxyOffsets.mClass, gBinderProxyOffsets.mConstructor);
    if (object != NULL) {
        // BinderProxy.mObject = BpBinder 指针（long 值）
        env->SetLongField(object, gBinderProxyOffsets.mObject, (jlong)val.get());
        val->incStrong((void*)javaObjectForIBinder);

        // 将 BinderProxy 附加到 BpBinder 的 mObjects，建立双向引用
        jobject refObject = env->NewGlobalRef(
            env->GetObjectField(object, gBinderProxyOffsets.mSelf));
        val->attachObject(&gBinderProxyOffsets, refObject, ...);

        // 创建死亡通知列表
        sp<DeathRecipientList> drl = new DeathRecipientList;
        env->SetLongField(object, gBinderProxyOffsets.mOrgue,
                          reinterpret_cast<jlong>(drl.get()));
    }
    return object;
}
```

> `javaObjectForIBinder` 是 Java 层 BinderProxy 与 C++ 层 BpBinder 之间的 **双向绑定**——通过 `mObject`（long 值存储 BpBinder 指针）和 `attachObject`（BpBinder 持有 BinderProxy 引用）实现互查。

因此：**`ServiceManagerNative.asInterface(BinderInternal.getContextObject())`**

\[\downarrow\]

等价于 `ServiceManagerNative.asInterface(new BinderProxy())`

### 3.3 ServiceManagerNative.asInterface → ServiceManagerProxy

`ServiceManagerNative.asInterface(obj)` 判断参数是否为本地服务——由于 `obj` 是 `BinderProxy`（非本地），`queryLocalInterface` 返回 NULL，直接构造 `ServiceManagerProxy`：

```java
// ServiceManagerNative.java
static public IServiceManager asInterface(IBinder obj) {
    if (obj == null) return null;
    // queryLocalInterface 返回 null（obj 是 BinderProxy，不是本地服务）
    IServiceManager in = (IServiceManager) obj.queryLocalInterface(descriptor);
    if (in != null) return in;
    return new ServiceManagerProxy(obj);  // ★
}
```

`ServiceManagerProxy` 初始化：

```java
class ServiceManagerProxy implements IServiceManager {
    private IBinder mRemote;

    public ServiceManagerProxy(IBinder remote) {
        mRemote = remote;   // BinderProxy 对象，对应 BpBinder(0)
    }
}
```

> 最终 `ServiceManager.getIServiceManager()` 等价于 `new ServiceManagerProxy(new BinderProxy())`。

下图展示了 Binder Framework 层的完整类图关系——浅蓝色为 Interface，其余为 Class：

<img src="./images/binder-doc9-00.png" width="500" alt="Binder Framework 层类图">

---

## 四、服务注册：Java → Native 全链路

服务注册是 Binder Framework 层最完整的纵向切片——从 Java 层 `ServiceManagerProxy.addService` 出发，经 `writeStrongBinder` 的 JNI 转换、`JavaBBinder` 桥、`flatten_binder` 扁平化，最终进入 `BpBinder::transact`。本章逐层拆解每一环的转换细节。

### 4.1 ServiceManagerProxy.addService

Java 层的 `ServiceManagerProxy.addService` 将服务名和 IBinder 写入 Parcel，通过 `mRemote.transact(ADD_SERVICE_TRANSACTION)` 发往 BinderProxy（handle=0）。完整代码：

```java
// ServiceManagerNative.java :: ServiceManagerProxy
public void addService(String name, IBinder service, boolean allowIsolated)
        throws RemoteException {
    Parcel data = Parcel.obtain();
    Parcel reply = Parcel.obtain();
    data.writeInterfaceToken(IServiceManager.descriptor);  // "android.os.IServiceManager"
    data.writeString(name);
    data.writeStrongBinder(service);     // ★ Java Binder → flat_binder_object
    data.writeInt(allowIsolated ? 1 : 0);
    mRemote.transact(ADD_SERVICE_TRANSACTION, data, reply, 0);  // ★ 发往 handle=0
    reply.recycle();
    data.recycle();
}
```

### 4.2 Java writeStrongBinder → ibinderForJavaObject

Java 层的 `Parcel.writeStrongBinder` 通过 JNI 调用 `android_os_Parcel_writeStrongBinder`，后者再调用 `ibinderForJavaObject` 将 Java IBinder 对象转换为 C++ 的 `sp<IBinder>`。Java 层入口和 JNI 实现如下：

```java
// Parcel.java
public final void writeStrongBinder(IBinder val) {
    nativeWriteStrongBinder(mNativePtr, val);  // JNI 调用
}
```

JNI 层实现：

```cpp
// android_os_Parcel.cpp
static void android_os_Parcel_writeStrongBinder(JNIEnv* env, jclass clazz,
                                                  jlong nativePtr, jobject object) {
    Parcel* parcel = reinterpret_cast<Parcel*>(nativePtr);  // Java Parcel → C++ Parcel
    if (parcel != NULL) {
        const status_t err = parcel->writeStrongBinder(ibinderForJavaObject(env, object));
    }
}
```

**ibinderForJavaObject**：Java IBinder → C++ IBinder 反向转换：

```cpp
// android_util_Binder.cpp
sp<IBinder> ibinderForJavaObject(JNIEnv* env, jobject obj) {
    if (obj == NULL) return NULL;

    // ★ Java 层的 Binder 对象 → 提取 mObject → JavaBBinderHolder → JavaBBinder
    if (env->IsInstanceOf(obj, gBinderOffsets.mClass)) {
        JavaBBinderHolder* jbh = (JavaBBinderHolder*)
            env->GetLongField(obj, gBinderOffsets.mObject);
        return jbh != NULL ? jbh->get(env, obj) : NULL;
    }

    // ★ Java 层的 BinderProxy → 提取 mObject → 直接拿到 BpBinder 指针
    if (env->IsInstanceOf(obj, gBinderProxyOffsets.mClass)) {
        return (IBinder*)env->GetLongField(obj, gBinderProxyOffsets.mObject);
    }
    return NULL;
}
```

> `ibinderForJavaObject` 根据 Java 对象类型判断：Binder → 通过 `JavaBBinderHolder` 获取 `JavaBBinder`；BinderProxy → 直接读取 `mObject` 字段中的 BpBinder 指针。

### 4.3 JavaBBinderHolder → JavaBBinder（Java Binder → C++ BBinder 桥）

`JavaBBinderHolder` 是 Java 层 `Binder` 类在 C++ 层的持有者——`Binder.mObject`（long 值）存储 `JavaBBinderHolder` 的指针。`get()` 方法按需创建 `JavaBBinder`（继承 BBinder），并用弱引用（wp）缓存以支持 GC 回收。核心代码：

```cpp
// android_util_Binder.cpp
sp<JavaBBinder> JavaBBinderHolder::get(JNIEnv* env, jobject obj) {
    AutoMutex _l(mLock);
    sp<JavaBBinder> b = mBinder.promote();  // 尝试从弱引用升级
    if (b == NULL) {
        b = new JavaBBinder(env, obj);      // ★ 首次创建 JavaBBinder
        mBinder = b;                         // 保存为弱引用（wp）
    }
    return b;
}

// JavaBBinder 构造函数
JavaBBinder::JavaBBinder(JNIEnv* env, jobject object)
    : mVM(jnienv_to_javavm(env)),
      mObject(env->NewGlobalRef(object))     // ★ 持有 Java 层 Binder 的全局引用
{
    android_atomic_inc(&gNumLocalRefs);
    incRefsCreated(env);
}
```

> `JavaBBinder` 继承自 `BBinder`——它是 Java 层 `Binder` 类在 C++ 层的对应实体。当 Java 层的 `onTransact()` 需要被调用时，`JavaBBinder` 通过 `mObject` 全局引用回调到 Java 层执行。

### 4.4 Parcel.writeStrongBinder(C++) → flatten_binder

C++ 层的 `Parcel::writeStrongBinder` 调用 `flatten_binder` 将 IBinder 转换为 `flat_binder_object`——`localBinder()` 非 NULL 则为 BINDER_TYPE_BINDER（本地实体），否则为 BINDER_TYPE_HANDLE（远程代理）。通过 `BBinder::localBinder()≠NULL` 和 `IBinder::localBinder()=NULL` 的多态来区分：

```cpp
// Parcel.cpp
status_t Parcel::writeStrongBinder(const sp<IBinder>& val) {
    return flatten_binder(ProcessState::self(), val, this);
}

status_t flatten_binder(const sp<ProcessState>&, const sp<IBinder>& binder, Parcel* out) {
    flat_binder_object obj;
    obj.flags = 0x7f | FLAT_BINDER_FLAG_ACCEPTS_FDS;

    if (binder != NULL) {
        IBinder *local = binder->localBinder();
        if (local) {
            // ★ 本地实体 → JavaBBinder → BINDER_TYPE_BINDER
            obj.type = BINDER_TYPE_BINDER;
            obj.binder = reinterpret_cast<uintptr_t>(local->getWeakRefs());
            obj.cookie = reinterpret_cast<uintptr_t>(local);
        } else {
            // 远程代理 → BpBinder → BINDER_TYPE_HANDLE
            obj.type = BINDER_TYPE_HANDLE;
            obj.handle = binder->remoteBinder()->handle();
        }
    }
    return finish_flatten_binder(binder, obj, out);  // → out->writeObject(flat)
}

// BBinder::localBinder() 返回自身（非 NULL），IBinder::localBinder() 返回 NULL
BBinder* BBinder::localBinder() { return this; }
BBinder* IBinder::localBinder()  { return NULL; }
```

> `data.writeStrongBinder(service)` 的最终效果：`parcel->writeStrongBinder(new JavaBBinder(env, serviceObj))`——即把 Java 层的 Binder 服务对象转换为 `BINDER_TYPE_BINDER` 类型的 `flat_binder_object` 写入 Parcel。

### 4.5 BinderProxy.transact → BpBinder::transact（JNI 桥）

`BinderProxy.transact` 是 Java 层 Binder IPC 的最后一步——先检查 Parcel 大小（≤800KB），再通过 `transactNative` 进入 JNI 层，从 `BinderProxy.mObject` 取出 BpBinder 指针，调用 `BpBinder::transact` 进入 Native Binder 通信：

```java
// Binder.java :: BinderProxy
public boolean transact(int code, Parcel data, Parcel reply, int flags)
        throws RemoteException {
    // ★ 检查 Parcel 大小是否超过 800KB
    Binder.checkParcel(this, code, data, "Unreasonably large binder buffer");
    return transactNative(code, data, reply, flags);  // → JNI
}
```

`transactNative` 的 JNI 实现：

```cpp
// android_util_Binder.cpp
static jboolean android_os_BinderProxy_transact(JNIEnv* env, jobject obj,
    jint code, jobject dataObj, jobject replyObj, jint flags) {

    // Java Parcel → C++ Parcel
    Parcel* data  = parcelForJavaObject(env, dataObj);
    Parcel* reply = parcelForJavaObject(env, replyObj);

    // ★ 从 BinderProxy.mObject 取出 BpBinder 指针
    IBinder* target = (IBinder*)env->GetLongField(obj, gBinderProxyOffsets.mObject);

    // ★ 调用 C++ 层 BpBinder::transact → 进入 Native Binder 通信
    status_t err = target->transact(code, *data, reply, flags);
    return JNI_FALSE;
}
```

---

## 五、服务获取：Java → Native 全链路

服务获取与注册共享同一套 Java → Native 转换通道，但方向相反——查询完成后，驱动返回的 BpBinder 需要经 `readStrongBinder` 反向转换回 Java 层的 `BinderProxy`。本章拆解获取侧的三个关键环节。

### 5.1 ServiceManager.getService

`ServiceManager.getService` 对外提供查询接口——先从 `sCache`（HashMap）缓存查询，未命中则通过 `getIServiceManager().getService()` 走 Binder IPC 查询。完整代码：

```java
// ServiceManager.java
public static IBinder getService(String name) {
    IBinder service = sCache.get(name);   // ★ 先从 HashMap 缓存取
    if (service != null) return service;

    try {
        return getIServiceManager().getService(name);  // → ServiceManagerProxy
    } catch (RemoteException e) {
        Log.e(TAG, "error in getService", e);
    }
    return null;
}
```

### 5.2 ServiceManagerProxy.getService

`ServiceManagerProxy.getService` 通过 `mRemote.transact(GET_SERVICE_TRANSACTION)` 向 ServiceManager 发起查询，返回结果通过 `reply.readStrongBinder()` 解析为 IBinder。完整代码：

```java
class ServiceManagerProxy implements IServiceManager {
    public IBinder getService(String name) throws RemoteException {
        Parcel data = Parcel.obtain();
        Parcel reply = Parcel.obtain();
        data.writeInterfaceToken(IServiceManager.descriptor);
        data.writeString(name);
        mRemote.transact(GET_SERVICE_TRANSACTION, data, reply, 0);
        IBinder binder = reply.readStrongBinder();   // ★ 从 reply 解析出 IBinder
        reply.recycle();
        data.recycle();
        return binder;
    }
}
```

`mRemote.transact` → `BinderProxy.transact` → `transactNative` → JNI → `BpBinder::transact` → `IPCThreadState::transact` → `waitForResponse`：

```cpp
// waitForResponse 中收到 BR_REPLY 的处理
case BR_REPLY: {
    binder_transaction_data tr;
    err = mIn.read(&tr, sizeof(tr));
    if (reply) {
        if ((tr.flags & TF_STATUS_CODE) == 0) {
            // ★ 将驱动返回的数据引用直接赋给 reply Parcel
            //    reply 回收时会调用 freeBuffer 释放驱动 buffer
            reply->ipcSetDataReference(
                reinterpret_cast<const uint8_t*>(tr.data.ptr.buffer),
                tr.data_size,
                reinterpret_cast<const binder_size_t*>(tr.data.ptr.offsets),
                tr.offsets_size / sizeof(binder_size_t),
                freeBuffer, this);
        }
    }
}
```

### 5.3 readStrongBinder → javaObjectForIBinder（返回为 BinderProxy）

`reply.readStrongBinder()` 最终调用 `javaObjectForIBinder`——将 C++ 层的 `BpBinder(handle)` 转换为 Java 层的 `BinderProxy` 对象。调用方拿到这个 `BinderProxy` 后，通过 `asInterface` 转换为具体的业务代理（如 `BpActivityManager`）。

---

## 六、关键总结

本章汇总 Binder Framework 层的核心结论——从 JNI 双向桥到 ServiceManager 的 Java 封装，再到完整的 addService/getService 调用链。

下图是 AIDL 编译文件与调用链的总览：

<img src="./images/binder-doc9-02.png" width="500" alt="AIDL 编译与调用链">

1. **JNI 双向桥**：`gBinderOffsets`（C→Java）和 `gBinderMethods`（Java→C）在 Zygote 启动时一次性建立，所有 App 进程通过 COW 继承。

2. **javaObjectForIBinder / ibinderForJavaObject**：Java ↔ C++ Binder 对象互转的核心函数——前者创建 BinderProxy + 双向绑定，后者通过 mObject 字段还原指针。

3. **JavaBBinderHolder → JavaBBinder**：Java 层 `Binder` 类在 C++ 层的代理——`mObject` 字段存储 `JavaBBinderHolder` 的指针，按需创建 `JavaBBinder`（继承 BBinder），可通过 JNI 回调 Java 层的 `execTransact()`。

4. **ServiceManager Java 封装**：`getIServiceManager()` → `ServiceManagerNative.asInterface(new BinderProxy())` → `new ServiceManagerProxy(BinderProxy)`，所有 addService/getService 最终通过 `mRemote.transact()` 发往 handle=0。

5. **BinderProxy.transact**：Java 层先 `checkParcel`（800KB 限制），再通过 `transactNative` → JNI → `GetLongField(mObject)` 取 BpBinder 指针 → `BpBinder::transact` → 进入 Native Binder 通信。获取服务后通过 `javaObjectForIBinder` 将返回的 BpBinder 转为 BinderProxy。
