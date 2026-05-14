/**
 * open-studio.ts · 开 Chrome 到 TikTok Studio Upload 页 (持久化账号)
 *
 * 用法：
 *   cd ~/catchzvibe && npx tsx ~/.claude/skills/tiktok-publish/scripts/open-studio.ts --account=choice
 *   cd ~/catchzvibe && npx tsx ~/.claude/skills/tiktok-publish/scripts/open-studio.ts --account=snacks
 *
 * 必须 cd 到 catchzvibe · 因为依赖它的 node_modules/playwright + lib/browser.ts。
 *
 * 跑完 Chrome 弹出 · 用户自己上传 + 粘 caption + 点 Post。
 * 关 Chrome 窗口即结束 node 进程。
 */

import { launchAccountContext } from "/Users/happyglobal_tk_team/catchzvibe/scripts/tiktok-publish/lib/browser";

function parseArg(name: string): string | undefined {
  const prefix = `--${name}=`;
  for (const a of process.argv.slice(2)) {
    if (a.startsWith(prefix)) return a.slice(prefix.length);
  }
  return undefined;
}

async function main() {
  const account = parseArg("account");
  if (!account) {
    console.error("用法: --account=<choice|snacks|...>");
    process.exit(1);
  }
  const ctx = await launchAccountContext(account);
  const page = ctx.pages()[0] ?? (await ctx.newPage());
  await page.goto("https://www.tiktok.com/tiktokstudio/upload");
  console.log(`✅ ${account} studio 已打开 · 用完关 Chrome 即可`);
  await new Promise(() => {}); // 永不退出 · 等 Chrome 关
}

main().catch((e) => {
  console.error("❌", e);
  process.exit(1);
});
