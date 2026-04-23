import os
import subprocess
import re
import shutil

# 源目录（Git 仓库本地路径）
SOURCE_PATH = os.path.abspath(r"D:/source")

# Gitee 仓库的 raw 文件访问前缀
GITEE_RAW_BASE = "https://gitee.com/a2431242530qqcom/material-warehouse/raw/main/"


def parse_any_path(filepath):
    """通用路径解析（支持任意扩展名）"""
    # 修复正则：确保能匹配无盘符或纯文件名的情况
    pattern = r'^(?:([a-zA-Z]:)?[\\/]?((?:.*[\\/])?))?([^\\/]+)\.([^.\\/]+)$'
    match = re.match(pattern, filepath)
    if match:
        drive, path_part, name, ext = match.groups()
        return {
            'directory': path_part.rstrip('/\\') if path_part else '',
            'basename': name,
            'extension': '.' + ext,
            'filename': name + '.' + ext
        }
    else:
        return {'error': '路径格式不匹配'}


def copy_file(src, dst_dir):
    """复制文件到目标目录，返回新路径"""
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, os.path.basename(src))
    shutil.copy2(src, dst_path)
    return dst_path


def run_git_command(cmd, cwd=SOURCE_PATH):
    """执行 git 命令，返回 (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)


def push_image_to_gitee(image_path):
    """主函数：上传图片到 Gitee 并返回可访问 URL"""
    # 1. 解析文件名
    fileinfo = parse_any_path(image_path)
    if 'error' in fileinfo:
        raise ValueError(f"路径解析失败: {image_path}")

    filename = fileinfo['filename']
    print(f"正在处理文件: {filename}")

    # 2. 复制文件到仓库目录
    local_repo_path = copy_file(image_path, SOURCE_PATH)
    print(f"文件已复制到: {local_repo_path}")

    # 3. 执行 Git 操作
    commands = [
        ["git", "pull", "--rebase", "origin", "main"],
        ["git", "add", filename],
        ["git", "commit", "-m", f"Add image: {filename}"],
        ["git", "push", "origin", "main"]
    ]

    for cmd in commands:
        cmd_str = " ".join(cmd)
        print(f"执行: {cmd_str}")
        code, out, err = run_git_command(cmd_str)
        if code != 0:
            # 忽略“nothing to commit”等非致命错误
            if "nothing to commit" in err or "up to date" in err:
                print("⚠️ 提示:", err.strip())
                continue
            else:
                print(f"❌ Git 命令失败: {err}")
                raise RuntimeError(f"Git 操作失败: {err}")

    # 4. 返回 Gitee 图片 URL（使用 raw 链接才能直接显示）
    gitee_url = GITEE_RAW_BASE + filename
    print(f"✅ 图片已上传！访问链接:\n{gitee_url}")
    return gitee_url


# -------------------------
# 使用示例
if __name__ == "__main__":
    try:
        # 替换为你自己的图片路径
        input_image = r"D:/temp/my_photo.png"
        url = push_image_to_gitee(input_image)
        # 你可以在这里把 url 赋值给变量或返回
    except Exception as e:
        print(f"❌ 程序出错: {e}")