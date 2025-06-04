import { test } from "./fixture";

test.beforeEach(async ({ page }) => {
  page.setViewportSize({ width: 400, height: 905 });
  await page.goto("https://heyteavivocity.meuu.online/home");
  await page.waitForLoadState("networkidle");
});

test("ai online order", async ({ page, ai }) => {
  await ai("点击左上角语言切换按钮(English、中文)，在弹出的下拉列表中点击中文");
  await ai("向下滚动一屏");
  await ai("直接点击多肉大橘的规格按钮");
  await ai("点击不使用吸管、点击冰沙推荐、点击正常冰推荐");
  await ai("向下滚动一屏");
  await ai("点击标准甜、点击绿妍（推荐）、点击标准口味");
  await ai("滚动到最下面");
  await ai("点击选好了按钮");
  await ai("点击右上角商品图标按钮");

  // 随便滚动一下
  await ai("滚动到最下面");
});