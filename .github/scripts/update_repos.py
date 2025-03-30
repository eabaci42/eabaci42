#!/usr/bin/env python3
import os
import re
import random
import requests
from datetime import datetime

# GitHub API için token - GitHub Actions secrets'dan alınır
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = 'eabaci42'

def get_public_repos():
    """Kullanıcının tüm public repolarını çeker"""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    repos = []
    page = 1
    
    while True:
        url = f'https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100&page={page}&type=public'
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"API hatası: {response.status_code}")
            print(response.text)
            break
            
        page_repos = response.json()
        if not page_repos:
            break
            
        # Sadece public repoları filtrele
        for repo in page_repos:
            if not repo.get('private', True):
                repos.append(repo)
                
        page += 1
    
    return repos

def select_random_repos(repos, count=4):
    """Verilen repo listesinden rastgele 'count' kadar repo seçer"""
    if len(repos) <= count:
        return repos
    return random.sample(repos, count)

def generate_repo_markdown(repos):
    """Seçilen repolar için markdown formatında HTML oluşturur"""
    
    # Farklı temalar
    themes = ['tokyonight', 'radical', 'nightowl', 'synthwave', 'dracula', 'cobalt', 'merko', 'vue-dark']
    
    # İlk satır için iki repo
    first_row = f"""  <div>
    <a href="{repos[0]['html_url']}">
      <img width="48%" src="https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/pin/?username={GITHUB_USERNAME}&repo={repos[0]['name']}&theme={themes[0]}" />
    </a>
    <a href="{repos[1]['html_url']}">
      <img width="48%" src="https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/pin/?username={GITHUB_USERNAME}&repo={repos[1]['name']}&theme={themes[1]}" />
    </a>
  </div>
  
  <div style="margin-top: 10px;">
    <a href="{repos[2]['html_url']}">
      <img width="48%" src="https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/pin/?username={GITHUB_USERNAME}&repo={repos[2]['name']}&theme={themes[2]}" />
    </a>
    <a href="{repos[3]['html_url']}">
      <img width="48%" src="https://github-readme-stats-git-masterrstaa-rickstaa.vercel.app/api/pin/?username={GITHUB_USERNAME}&repo={repos[3]['name']}&theme={themes[3]}" />
    </a>
  </div>"""
    
    return first_row

def update_readme(repo_markdown):
    """README.md dosyasında repo bölümünü günceller"""
    with open('README.md', 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Projeler bölümünü bul ve değiştir
    projects_section_pattern = r'(## <div align="center">📊 Projeler ve Yaklaşımım</div>\n\n<div align="center">\n  <!-- Dinamik Projeler - Haftada bir güncellenir -->\n)(.*?)(\n\n<div align="center" style="margin-top: 20px;">)'
    
    # Son güncelleme bilgisini ekle
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    replacement = f'\\1  <!-- Son güncelleme: {now} -->\n{repo_markdown}\\3'
    
    updated_content = re.sub(projects_section_pattern, replacement, content, flags=re.DOTALL)
    
    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_content)

def main():
    print("GitHub repolarını alıyor...")
    repos = get_public_repos()
    
    if not repos:
        print("Hiç public repo bulunamadı!")
        return
    
    print(f"Toplam {len(repos)} repo bulundu.")
    print("Rastgele repo seçiliyor...")
    
    selected_repos = select_random_repos(repos)
    print(f"Seçilen repolar: {[repo['name'] for repo in selected_repos]}")
    
    repo_markdown = generate_repo_markdown(selected_repos)
    print("README.md güncelleniyor...")
    
    update_readme(repo_markdown)
    print("README.md başarıyla güncellendi!")

if __name__ == "__main__":
    main() 