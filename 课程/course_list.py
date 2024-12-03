import requests

def get_github_files(owner, repo, path='.', token=None, indent=0):
    markdown_dir = ""
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers = {'Authorization': f'token {token}'} if token else {}

    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        print(f"The repository {owner}/{repo} or path {path} was not found.")
        return ""
    response.raise_for_status()  # 确保请求成功

    items = response.json()
    if len(items) > 8:  # 如果文件数量超过8个，则不显示任何文件
        return f"  {'  ' * indent}- [{path.replace('/', '')}]({url})\n"
    else:
        for item in items:
            prefix = '  ' * indent  # 根据缩进级别生成空格
            if item['type'] == 'file':
                markdown_dir += f"{prefix}- [{item['name']}]({item['html_url']})\n"
            elif item['type'] == 'dir':
                markdown_dir += f"{prefix}- [{item['name']}/]({item['html_url']})\n"
                sub_path = f"{path}/{item['name']}" if path != '.' else item['name']
                markdown_dir += get_github_files(owner, repo, sub_path, token, indent + 1)

    return markdown_dir

# 配置你的GitHub用户名、仓库名和访问令牌
owner = 'yangzhe6'
repo = 'COURSE'
access_token = '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'  # 替换为你的GitHub访问令牌

# 获取Markdown目录
markdown_dir = get_github_files(owner, repo, token=access_token)

# 将Markdown目录写入到README.md文件中
with open('README1.md', 'w', encoding='utf-8') as f:
    f.write("## 文件索引\n\n")
    f.write(markdown_dir)

print("README1.md文件已生成。")
