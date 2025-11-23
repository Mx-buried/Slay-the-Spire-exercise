import os
from pathlib import Path

def print_simple_tree(start_path='.'):
    """
    使用 os.walk 简化版本
    """
    start_path = Path(start_path)
    print(f"目录结构: {start_path.absolute()}")
    
    for root, dirs, files in os.walk(start_path):
        level = root.replace(str(start_path), '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            print(f"{sub_indent}{file}")

# 运行
print_simple_tree()
#print("\033[1;31;43mhelloworld\033[0m")