# 推送到 GitHub（在你自己的电脑上执行）

仓库已经完全配置好了：远程地址、README 里的在线访问地址、页面右上角的 GitHub 链接，
全部已指向 `Nishino0525Nanase/kaoyan-hub`。**你只需要推送。**

## 三步

```bash
unzip kaoyan-hub.zip
cd kaoyan-schools
git push -u origin main
```

推送时会要求登录：
- 用户名填 `Nishino0525Nanase`
- 密码填你的 **Personal Access Token**（不是 GitHub 密码，GitHub 已不支持密码推送）

如果你装了 GitHub CLI 并登录过（`gh auth login`），可以省掉输密码：

```bash
gh auth setup-git   # 让 git 使用 gh 的凭据
git push -u origin main
```

## 开启 GitHub Pages

推完之后到仓库页面：

**Settings → Pages → Build and deployment → Source** 选 **GitHub Actions**

仓库里已经有 `.github/workflows/pages.yml`，选完 Actions 会自动跑一次构建（约 1 分钟）。
完成后访问：

**https://Nishino0525Nanase.github.io/kaoyan-hub/**

## 以后更新数据

```bash
# 1. 改 data/ 下的 json
# 2. 如果动了 programs-*.json，重新合并：
python3 src/merge_programs.py
# 3. 重新生成页面：
node build.mjs
# 4. 提交推送：
git add -A && git commit -m "data: 补充 XX 数据" && git push
```

GitHub Actions 会自动重新部署，不用手动做别的。
