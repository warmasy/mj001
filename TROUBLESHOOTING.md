# 安装故障排除指南

## 问题：pydantic-core 构建失败

### 原因
pydantic v2 的核心 `pydantic-core` 是用 Rust 编写的，某些环境下需要从源码编译，如果缺少编译工具就会报错。

### 解决方案（按顺序尝试）

#### 方案 1：升级 pip（最简单，通常有效）

```bash
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

#### 方案 2：使用国内镜像（加速下载预编译包）

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 方案 3：如果上述不行，单独安装预编译的 pydantic

```bash
# 先升级 pip
python -m pip install --upgrade pip

# 单独安装 pydantic（带二进制 wheel）
pip install pydantic==2.6.1 --only-binary :all:

# 再安装其他依赖
pip install fastapi==0.109.2 uvicorn[standard]==0.27.1 pint==0.23 python-multipart==0.0.7
```

#### 方案 4：Python 版本问题

pydantic v2 要求 Python >= 3.8。如果 Python 版本太新（如 3.13），可能还没有预编译 wheel。

**推荐 Python 版本：3.10 或 3.11**（最稳定）

检查版本：
```bash
python --version
```

如果版本是 3.12/3.13，建议降级到 3.11：
```bash
# 使用 pyenv 或 conda 安装 3.11
conda create -n mech python=3.11
conda activate mech
pip install -r requirements.txt
```

#### 方案 5：Windows 缺少 Visual C++ 构建工具

如果提示 `Microsoft Visual C++ 14.0 is required`：

1. 下载 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. 安装「使用 C++ 的桌面开发」工作负载
3. 重新运行 `pip install -r requirements.txt`

#### 方案 6：使用 conda 安装（最省心）

```bash
conda create -n mech python=3.11
conda activate mech

# conda 安装主要依赖（带预编译包）
conda install -c conda-forge fastapi uvicorn pydantic pint

# pip 补充安装
pip install python-multipart
```

---

## 验证安装

安装完成后，验证是否成功：

```bash
python -c "import pydantic; print('pydantic:', pydantic.__version__)"
python -c "import pint; print('pint:', pint.__version__)"
python -c "import fastapi; print('fastapi:', fastapi.__version__)"
```

全部正常输出版本号后，即可启动服务：

```bash
python main.py
```
