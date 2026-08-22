#!/usr/bin/env bash
# 一键把本仓库推到你自己的 GitHub 并开启 Pages。
# 用法：  bash setup-github.sh <你的GitHub用户名>
# 例如：  bash setup-github.sh longeric666
set -euo pipefail

USER_NAME="${1:-}"
REPO="${2:-kaoyan-hub}"

if [ -z "$USER_NAME" ]; then
  echo "用法: bash setup-github.sh <你的GitHub用户名> [仓库名，默认 kaoyan-hub]"
  exit 1
fi

echo "==> 1/5 把 README 与构建脚本里的 OWNER 占位符替换成 $USER_NAME"
# macOS 与 Linux 的 sed 参数不同，统一用 perl
perl -pi -e "s/OWNER/$USER_NAME/g" README.md build.mjs

echo "==> 2/5 重新生成 index.html（GitHub 链接会指向你的仓库）"
if command -v node >/dev/null 2>&1; then
  REPO_URL="https://github.com/$USER_NAME/$REPO" node build.mjs
else
  echo "    ! 没装 node，跳过重建。页面仍可用，只是右上角 GitHub 链接还指向占位地址。"
fi

echo "==> 3/5 提交这次改动"
git add -A
git -c commit.gpgsign=false commit -q -m "chore: 将仓库地址指向 $USER_NAME/$REPO" || echo "    （没有需要提交的改动）"

echo "==> 4/5 创建远程仓库并推送"
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  echo "    检测到已登录的 gh CLI，自动创建公开仓库"
  gh repo create "$USER_NAME/$REPO" --public --source=. --remote=origin --push
else
  echo "    没有可用的 gh CLI。请先到 https://github.com/new 手动创建一个名为 $REPO 的【Public】仓库"
  echo "    （不要勾选 Add a README / .gitignore / license，保持空仓库）"
  read -r -p "    创建好之后按回车继续..." _
  git remote remove origin 2>/dev/null || true
  git remote add origin "https://github.com/$USER_NAME/$REPO.git"
  git branch -M main
  git push -u origin main
fi

echo "==> 5/5 开启 GitHub Pages"
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  gh api -X POST "repos/$USER_NAME/$REPO/pages" \
    -f "build_type=workflow" >/dev/null 2>&1 \
    && echo "    已开启（GitHub Actions 构建）" \
    || echo "    自动开启失败，请手动：仓库 Settings → Pages → Source 选 GitHub Actions"
else
  echo "    请手动开启：仓库 Settings → Pages → Source 选择 GitHub Actions"
fi

echo
echo "完成。等 Actions 跑完（约 1 分钟）后访问："
echo "  https://$USER_NAME.github.io/$REPO/"
echo
echo "以后更新数据：改 data/*.json → python3 src/merge_programs.py → node build.mjs → git push"
