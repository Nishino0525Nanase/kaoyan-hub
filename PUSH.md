# 把这个仓库推到 GitHub

沙箱里没有你的 GitHub 凭据（只能匿名读，不能写），所以 `git push` 这一步得在你自己电脑上做。
但该整理的都整理好了：解压完不用 init、不用 add、不用 commit，也不用处理分叉，一条 push 就完事。

## 当前状态

远端 `Nishino0525Nanase/kaoyan-hub` 上已经有东西了，`main` 停在
`b92f2c2 chore: 更新数据源守望基线 [skip ci]`——这两条是 Actions 工作流自动提交的，
只动了 `data/.watch-state.json`。

本地这四条是真正要推的内容：

```
(顶部)  docs: PUSH.md 更新为 rebase 后的快进推送说明
ee82fcb feat: 0854 全 79 所查证完毕，区分「确实不招」与「还没查」
c8c80ef feat: 0854 覆盖 41→73 所，修复分数线静默丢失
e1333d5 feat: 0854 补充 9 所院校，新增覆盖缺口清单
```

两边原本是分叉的（本地 4 条、远端 2 条，直接 push 会被拒），已经把本地这四条 rebase 到
`origin/main` 之上了。两边改的文件完全不重叠，rebase 没有冲突。现在是干净的快进推送，
不需要 `--force`。

## Windows

```cmd
cd /d D:\Users\Kn\Downloads
mkdir kaoyan-hub 2>nul
tar -xf kaoyan-hub-git.zip -C kaoyan-hub
cd kaoyan-hub
git log --oneline -5
git push origin main
```

`git log` 应该打印出上面那四条加 `b92f2c2`（顶部那条 docs 提交的哈希以实际为准），
看到了就说明历史完好。

## macOS / Linux

```bash
unzip -q ~/Downloads/kaoyan-hub-git.zip -d ~/kaoyan-hub
cd ~/kaoyan-hub
git push origin main
```

## 登录方式

push 时会要账号密码：

- 用户名：`Nishino0525Nanase`
- 密码：不是 GitHub 登录密码，要用 Personal Access Token
  （GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) →
  Generate new token，勾 **repo** 这一项即可）

装了 [GitHub CLI](https://cli.github.com/) 的话更省事，先 `gh auth login` 走浏览器授权，
之后 push 不再问密码。

> 任何在聊天窗口里出现过的 token 都应视为已泄露，去 Settings → Developer settings
> 撤销掉，重新建一个用。

## 如果 push 还是被拒

说明在你解压之前 Actions 又自动提交了新的守望基线。不要 force，跑这两条就行：

```bash
git pull --rebase origin main
git push origin main
```

## 推完之后

仓库设置里开一下 GitHub Pages：
Settings → Pages → Source 选 `GitHub Actions`（仓库里已经带好 `.github/workflows/pages.yml`）。
几分钟后站点就在 `https://nishino0525nanase.github.io/kaoyan-hub/`。
