#!/usr/bin/env python3
"""Build Simplified Chinese catalog JSON from grokbot.dev API snapshots."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "source"
OUT = ROOT / "data" / "localized"
OUT.mkdir(parents=True, exist_ok=True)

TAG_ZH = {
    "personal": "个人", "developer": "开发", "marketer": "营销", "marketing": "营销",
    "sales": "销售", "business": "商业", "engineering": "工程", "data": "数据",
    "support": "客服", "work": "办公", "finance": "财务", "ops": "运维",
    "creator": "创作", "content": "内容", "social-media": "社交", "social": "社交",
    "research": "研究", "learning": "学习", "family": "家庭", "health": "健康",
    "shopping": "购物", "travel": "旅行", "investor": "投资", "crypto": "加密",
    "productivity": "效率", "automation": "自动化", "monitoring": "监控",
    "analytics": "分析", "design": "设计", "video": "视频", "youtube": "YouTube",
    "email": "邮件", "calendar": "日历", "news": "资讯", "growth": "增长",
    "recruiting": "招聘", "back-office": "中后台", "knowledge-base": "知识库",
    "decision-support": "决策", "on-demand": "即用", "scheduled": "定时",
    "meta-bot": "元机器人", "agent-team": "智能体团队", "student": "学生",
    "home": "家居", "life-hacks": "生活妙招", "wellbeing": "健康",
    "saving-money": "省钱", "food": "美食", "events": "活动", "real-estate": "房产",
    "fun": "玩乐", "finance-ops": "财务与运营", "seo": "SEO", "meetings": "会议",
    "ads": "广告", "prospecting": "获客", "crm": "CRM", "outreach": "触达",
    "calls": "电话", "pipeline": "销售漏斗", "code-review": "代码评审",
    "ci-cd": "CI/CD", "issues": "工单", "docs": "文档", "agents-ops": "智能体运维",
    "triage": "分诊", "replies": "回复", "escalation": "升级", "bookkeeping": "记账",
    "invoicing": "开票", "reporting": "报表", "subscriptions": "订阅",
    "compliance": "合规", "scraping": "抓取", "alerts": "告警", "dashboards": "看板",
    "enrichment": "数据补全", "money": "理财", "markets": "市场", "portfolio": "组合",
    "creative": "创意", "games": "游戏", "roleplay": "角色扮演", "media": "媒体",
    "scheduling": "排程", "tasks": "任务", "trading-crypto": "交易与加密",
}

CAT_PAGE = {
    "work": ("办公", "邮件、会议、文档、排程——把桌上那摊事交给 Bot。"),
    "sales": ("销售", "获客、CRM、触达、电话、漏斗。让 Bot 做跟进，成交还是你来点头。"),
    "marketing": ("营销", "SEO、内容、社交、广告、分析、竞品情报。"),
    "engineering": ("工程", "代码评审、CI/CD、工单、文档、智能体运维。"),
    "support": ("客服", "分诊、回复、知识库、升级。前线可以是 Bot。"),
    "finance-ops": ("财务与运营", "记账、开票、报表、订阅、合规。"),
    "data": ("数据", "抓取、监控、告警、看板、补全。"),
    "personal": ("个人", "家居、旅行、健康、学习、家庭、理财。"),
    "trading-crypto": ("交易与加密", "行情、组合、告警。"),
    "fun": ("玩乐", "创意、游戏、角色扮演、媒体。"),
}

SUB_ZH = {
    "email": "邮件", "meetings": "会议", "docs": "文档", "scheduling": "排程",
    "tasks": "任务", "research": "研究", "prospecting": "获客", "crm": "CRM",
    "outreach": "触达", "calls": "电话", "pipeline": "销售漏斗", "seo": "SEO",
    "content": "内容", "social": "社交", "ads": "广告", "analytics": "分析",
    "competitive-intel": "竞品情报", "code-review": "代码评审", "ci-cd": "CI/CD",
    "issues": "工单", "agents-ops": "智能体运维", "triage": "分诊", "replies": "回复",
    "knowledge-base": "知识库", "escalation": "升级", "bookkeeping": "记账",
    "invoicing": "开票", "reporting": "报表", "subscriptions": "订阅",
    "compliance": "合规", "scraping": "抓取", "monitoring": "监控", "alerts": "告警",
    "dashboards": "看板", "enrichment": "数据补全", "home": "家居", "travel": "旅行",
    "health": "健康", "learning": "学习", "family": "家庭", "money": "理财",
    "markets": "市场", "portfolio": "组合", "creative": "创意", "games": "游戏",
    "roleplay": "角色扮演", "media": "媒体",
}

INT_ZH = {
    "devtune": "DevTune", "discord": "Discord", "github": "GitHub", "gmail": "Gmail",
    "google-calendar": "Google 日历", "google-docs": "Google 文档",
    "google-drive": "Google 云端硬盘", "hubspot": "HubSpot", "linear": "Linear",
    "notion": "Notion", "quickbooks": "QuickBooks", "salesforce": "Salesforce",
    "shopify": "Shopify", "slack": "Slack", "stripe": "Stripe",
    "telegram": "Telegram", "whatsapp": "WhatsApp", "x": "X",
}

SPONSOR_SLUGS = {"stayingapi", "transcriptapi", "zillapi"}

HEADING = {
    "What it does": "它能做什么",
    "Use it in Grok Bot": "在 Grok Bot 里怎么用",
    "Setup": "怎么装",
    "The prompt": "提示词",
    "Why it's cool": "为什么好看",
    "How it's set up": "怎么搭",
}


def tag_zh(slug):
    if not slug:
        return ""
    s = str(slug).replace("_", "-")
    return TAG_ZH.get(s, TAG_ZH.get(slug, slug))


def tags_zh(tags):
    out = []
    for t in tags or []:
        zh = tag_zh(t)
        out.append({"slug": t, "en": t.replace("-", " "), "zh": zh})
    return out


def zh_date(iso):
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)
        return f"{dt.year}年{dt.month}月{dt.day}日"
    except Exception:
        return str(iso)[:10]


def handle_of(obj):
    if not obj:
        return ""
    if isinstance(obj, dict):
        return obj.get("handle") or ""
    return str(obj)


def author_block(item):
    a = item.get("author") or item.get("sharer") or {}
    if not isinstance(a, dict):
        a = {}
    handle = a.get("handle") or ""
    url = a.get("url") or (f"https://x.com/{handle}" if handle else "")
    return {
        "handle": handle,
        "url": url,
        "platform": a.get("platform") or "x",
        "name": a.get("name"),
    }


def orig_url(item):
    return item.get("url") or "https://grokbot.dev/"


def md_headings(text):
    if not text:
        return ""
    out = text
    for en, zh in HEADING.items():
        out = re.sub(rf"^##\s*{re.escape(en)}\s*$", f"## {zh}", out, flags=re.M)
        out = out.replace(f"## {en}", f"## {zh}")
    return out


def attr_line(item):
    a = author_block(item)
    who = f"@{a['handle']}" if a["handle"] else "原作者"
    return (
        f"本条目译自 grokbot.dev，作者 {who}。"
        f"按 CC BY 4.0 复用时请同时署明作者与 grokbot.dev。"
    )

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from zh_templates import TEMPLATE_ZH
from zh_usecases import USECASE_ZH
from zh_plugins import PLUGIN_ZH
from zh_collections import COLLECTION_ZH

STEP_PHRASES = [
    ("Paste the prompt below into your Grok Bot", "把下面的提示词贴进你的 Grok Bot"),
    ("Paste the prompt below", "把下面的提示词贴进去"),
    ("so this becomes a standing capability", "让它成为常驻能力"),
    ("Create a ", "注册一个 "),
    ("Create an ", "注册一个 "),
    ("account at ", "账号，打开 "),
    ("and connect the accounts or data you want it to reach.", "并接上你希望它够得着的账户或数据。"),
    ("Get your API key or MCP connection from your", "从控制台拿到 API 密钥或 MCP 连接，产品是"),
    ("dashboard (see the linked docs for the exact place).", "（具体位置见其文档）。"),
    ("In Grok Bot,", "在 Grok Bot 里，"),
    ("Do not paste API keys into the chat.", "不要把 API 密钥贴进对话。"),
    ("Nothing goes live until you say yes.", "你说 yes 之前，什么也不会上线。"),
    ("Give your Grok Bot", "给你的 Grok Bot"),
    ("See the linked docs", "见链接中的文档"),
]


def tr_step(s: str) -> str:
    out = s
    for en, zh in STEP_PHRASES:
        out = out.replace(en, zh)
    # If still mostly English, wrap with a Chinese lead
    if sum(1 for c in out if "\u4e00" <= c <= "\u9fff") < 4:
        return f"按原文操作：{s}"
    return out


def tr_member_reason(s: str) -> str:
    if not s:
        return ""
    mapping = {
        "Your executive assistant:": "你的行政助理：",
        "Your CMO:": "你的 CMO：",
        "Your SDR:": "你的 SDR：",
        "so you start the day already briefed.": "这样你一睁眼就已经看过简报。",
        "so the day starts with a list, not a blank page.": "让一天从清单开始，而不是空白页。",
    }
    out = s
    for en, zh in mapping.items():
        out = out.replace(en, zh)
    if sum(1 for c in out if "\u4e00" <= c <= "\u9fff") < 6:
        # compact paraphrase
        return s  # keep English reason as fallback alongside; we'll prefix
    return out


def load(name):
    with open(SRC / name, encoding="utf-8") as f:
        return json.load(f)


def dump(name, obj):
    path = OUT / name
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def integrations_zh(arr):
    out = []
    for it in arr or []:
        if isinstance(it, str):
            out.append({"slug": it, "name": it, "name_zh": INT_ZH.get(it, it)})
        else:
            slug = it.get("slug") or ""
            out.append({
                **{k: it[k] for k in it if k != "page_url"},
                "name_zh": INT_ZH.get(slug, it.get("name") or slug),
                "page_url": f"/integrations/{slug}/" if slug else it.get("page_url"),
            })
    return out


def process_plugins():
    data = load("plugins.json")
    items = []
    for p in data["items"]:
        zh = PLUGIN_ZH.get(p["slug"], {})
        steps = zh.get("steps")
        if not steps:
            steps = [tr_step(s) for s in (p.get("install_steps") or [])]
        desc = zh.get("description") or md_headings(p.get("description") or "")
        items.append({
            **{k: p.get(k) for k in (
                "type", "slug", "name", "category", "categories", "subcategory",
                "status", "added_at", "updated_at", "verified_at", "featured",
                "project_url", "repo_url", "source_url", "prompt", "setup_minutes",
            )},
            "url": f"/plugins/{p['slug']}/",
            "orig_url": orig_url(p),
            "tagline": p.get("tagline"),
            "tagline_zh": zh.get("tagline") or p.get("tagline"),
            "category_zh": tag_zh(p.get("category")),
            "subcategory_zh": SUB_ZH.get(p.get("subcategory") or "", p.get("subcategory")),
            "integrations": integrations_zh(p.get("integrations")),
            "author": author_block(p),
            "scouted_by": p.get("scouted_by"),
            "featured": bool(p.get("featured")),
            "sponsor": p["slug"] in SPONSOR_SLUGS,
            "install_steps": p.get("install_steps") or [],
            "install_steps_zh": steps,
            "pricing_note": p.get("pricing_note"),
            "pricing_note_zh": zh.get("pricing") or p.get("pricing_note"),
            "description": p.get("description"),
            "description_zh": desc,
            "added_zh": zh_date(p.get("added_at")),
            "updated_zh": zh_date(p.get("updated_at")),
            "attribution": attr_line(p),
            "search_blob": " ".join(filter(None, [
                p.get("name"), p.get("tagline"), zh.get("tagline"), p.get("category"),
                tag_zh(p.get("category")), handle_of(p.get("author")),
            ])).lower(),
        })
    # featured table order: sponsors first matching homepage, then other featured
    sponsors = [x for x in items if x["sponsor"]]
    featured = [x for x in items if x["featured"] and not x["sponsor"]]
    # homepage order for sponsors
    order = ["stayingapi", "transcriptapi", "zillapi"]
    sponsors.sort(key=lambda x: order.index(x["slug"]) if x["slug"] in order else 99)
    dump("plugins.json", {
        "generated_at": data.get("generated_at"),
        "count": len(items),
        "items": items,
        "featured": sponsors + featured,
    })
    return items


def process_templates():
    data = load("templates.json")
    items = []
    for t in data["items"]:
        pair = TEMPLATE_ZH.get(t["slug"], (t.get("tagline"), t.get("description") or t.get("tagline")))
        tag_zh_s, desc_zh = pair
        tags = t.get("tags") or []
        items.append({
            "type": "template",
            "slug": t["slug"],
            "name": t.get("name"),
            "url": f"/marketplace/{t['slug']}/",
            "orig_url": orig_url(t),
            "tagline": t.get("tagline"),
            "tagline_zh": tag_zh_s,
            "description": t.get("description"),
            "description_zh": desc_zh,
            "body": t.get("body"),
            "body_zh": f"## 它能做什么\n\n{desc_zh}\n\n原文完整说明见 grokbot.dev。提示词/安装包请走分享链接，本页不改行为。",
            "share_url": t.get("share_url"),
            "sharer": author_block(t),
            "source": t.get("source"),
            "tags": tags,
            "tags_zh": tags_zh(tags),
            "tag_facets": t.get("tag_facets"),
            "primary_category": t.get("primary_category"),
            "primary_category_zh": tag_zh(t.get("primary_category")),
            "includes": t.get("includes"),
            "integrations": integrations_zh(t.get("integrations")),
            "related_use_cases": t.get("related_use_cases"),
            "featured": bool(t.get("featured")),
            "status": t.get("status"),
            "added_at": t.get("added_at"),
            "updated_at": t.get("updated_at"),
            "added_zh": zh_date(t.get("added_at")),
            "attribution": attr_line({**t, "author": t.get("sharer")}),
            "search_blob": " ".join(filter(None, [
                t.get("name"), t.get("tagline"), tag_zh_s, desc_zh,
                " ".join(tags), " ".join(tag_zh(x) for x in tags),
                handle_of(t.get("sharer")),
            ])).lower(),
        })
    items_sorted = sorted(items, key=lambda x: x.get("added_at") or "", reverse=True)
    dump("templates.json", {
        "generated_at": data.get("generated_at"),
        "count": len(items),
        "items": items_sorted,
        "fresh": items_sorted[:12],
    })
    return items_sorted


FULL_UC = set()


def process_usecases():
    data = load("use-cases.json")
    items = []
    scored = sorted(
        [u for u in data["items"] if isinstance(u.get("awesome_score"), (int, float))],
        key=lambda u: u["awesome_score"],
        reverse=True,
    )
    full = {u["slug"] for u in scored[:24]}
    full.update({u["slug"] for u in data["items"][:12]})
    FULL_UC.update(full)
    for u in data["items"]:
        pair = USECASE_ZH.get(u["slug"], (u.get("headline") or u.get("name"), u.get("tagline") or u.get("summary")))
        name_zh, tag_s = pair
        why = u.get("why_its_cool") or ""
        how = u.get("how_its_set_up") or ""
        is_full = u["slug"] in full
        why_zh = tag_s if not is_full else (
            f"{tag_s}\n\n" + (why if False else tag_s)
        )
        # For full pages, expand why with Chinese paraphrase of the one-liner plus a note
        if is_full:
            why_zh = f"{tag_s}\n\n这是目录里写得比较完整的一条。设置步骤见下方中文摘要；完整英文提示词保持原样，行为不要改。原帖只作引用，不整篇转载。"
            how_zh = f"按作者 @{handle_of(u.get('author'))} 的原设置来。下面保留英文步骤原文，以免漏掉工具名和路径。装完把提示词原样贴进 Grok Bot。\n\n" + (how or "")
        else:
            why_zh = tag_s
            how_zh = "轻量页：中文标题与简介如下。完整设置说明请看原文。提示词保持英文。"
        items.append({
            "type": "use-case",
            "slug": u["slug"],
            "name": u.get("name"),
            "name_zh": name_zh,
            "headline": u.get("headline"),
            "headline_zh": name_zh,
            "url": f"/use-cases/{u['slug']}/",
            "orig_url": orig_url(u),
            "tagline": u.get("tagline") or u.get("summary"),
            "tagline_zh": tag_s,
            "summary": u.get("summary"),
            "summary_zh": tag_s,
            "what_it_does": u.get("what_it_does"),
            "what_it_does_zh": tag_s,
            "why_its_cool": why,
            "why_its_cool_zh": why_zh,
            "how_its_set_up": how,
            "how_its_set_up_zh": how_zh,
            "prompt": u.get("prompt"),
            "prompt_provenance": u.get("prompt_provenance"),
            "category": u.get("category"),
            "category_zh": tag_zh(u.get("category")),
            "categories": u.get("categories") or [],
            "subcategory": u.get("subcategory"),
            "integrations": integrations_zh(u.get("integrations")),
            "author": author_block(u),
            "scouted_by": u.get("scouted_by"),
            "primary_source": u.get("primary_source"),
            "source_tweets": u.get("source_tweets") or [],
            "awesome_score": u.get("awesome_score"),
            "format": u.get("format"),
            "featured": bool(u.get("featured")),
            "full_detail": is_full,
            "added_at": u.get("added_at"),
            "added_zh": zh_date(u.get("added_at")),
            "verified_at": u.get("verified_at"),
            "attribution": attr_line(u),
            "search_blob": " ".join(filter(None, [
                u.get("name"), name_zh, u.get("tagline"), tag_s,
                u.get("category"), tag_zh(u.get("category")),
                handle_of(u.get("author")),
            ])).lower(),
        })
    dump("use-cases.json", {
        "generated_at": data.get("generated_at"),
        "count": len(items),
        "items": items,
        "full_slugs": sorted(full),
    })
    return items


def process_collections():
    data = load("collections.json")
    items = []
    for c in data["items"]:
        trip = COLLECTION_ZH.get(c["slug"], (c.get("name"), c.get("tagline"), c.get("rationale") or ""))
        name_zh, tag_s, rat_zh = trip
        members = []
        for m in c.get("members") or []:
            reason = m.get("reason") or ""
            reason_zh = tr_member_reason(reason)
            if reason_zh == reason and reason:
                reason_zh = reason  # keep; template name is the hook
            href = m.get("url") or ""
            local = None
            if m.get("type") == "template":
                local = f"/marketplace/{m['slug']}/"
            elif m.get("type") == "use-case":
                local = f"/use-cases/{m['slug']}/"
            elif m.get("type") == "plugin":
                local = f"/plugins/{m['slug']}/"
            members.append({
                "type": m.get("type"),
                "slug": m.get("slug"),
                "name": m.get("name"),
                "reason": reason,
                "reason_zh": reason_zh if reason_zh != reason else reason,
                "url": local or href,
                "orig_url": href,
            })
        items.append({
            "type": "collection",
            "slug": c["slug"],
            "name": c.get("name"),
            "name_zh": name_zh,
            "url": f"/collections/{c['slug']}/",
            "orig_url": orig_url(c),
            "tagline": c.get("tagline"),
            "tagline_zh": tag_s,
            "rationale": c.get("rationale"),
            "rationale_zh": rat_zh,
            "category": c.get("category"),
            "category_zh": tag_zh(c.get("category")),
            "members": members,
            "member_count": c.get("member_count") or len(members),
            "added_at": c.get("added_at"),
            "added_zh": zh_date(c.get("added_at")),
            "author": author_block(c) if c.get("author") else {"handle": "grokbot.dev", "url": "https://grokbot.dev/", "platform": "web"},
            "attribution": "合集由 grokbot.dev 策展。成员条目请分别署明其作者与 grokbot.dev。",
            "search_blob": " ".join(filter(None, [
                c.get("name"), name_zh, c.get("tagline"), tag_s, rat_zh,
            ])).lower(),
        })
    dump("collections.json", {"generated_at": data.get("generated_at"), "count": len(items), "items": items})
    return items


def process_categories(plugins, usecases):
    data = load("categories.json")
    items = []
    for c in data["items"]:
        name_zh, intro = CAT_PAGE.get(c["slug"], (tag_zh(c["slug"]), ""))
        subs = []
        for s in c.get("subcategories") or []:
            slug = s.get("slug") if isinstance(s, dict) else s
            subs.append({
                "slug": slug,
                "name": s.get("name") if isinstance(s, dict) else slug,
                "name_zh": SUB_ZH.get(slug, slug),
                "counts": s.get("counts") if isinstance(s, dict) else {},
            })
        items.append({
            "slug": c["slug"],
            "name": c.get("name"),
            "name_zh": name_zh,
            "intro_zh": intro,
            "url": f"/categories/{c['slug']}/",
            "orig_url": c.get("url") or f"https://grokbot.dev/categories/{c['slug']}/",
            "counts": c.get("counts"),
            "subcategories": subs,
        })
    dump("categories.json", {"count": len(items), "items": items})
    return items


def process_integrations():
    data = load("integrations.json")
    items = []
    for it in data["items"]:
        slug = it["slug"]
        items.append({
            "slug": slug,
            "name": it.get("name"),
            "name_zh": INT_ZH.get(slug, it.get("name")),
            "aliases": it.get("aliases") or [],
            "url": f"/integrations/{slug}/",
            "orig_url": it.get("page_url") or it.get("url"),
            "auth": it.get("auth"),
            "counts": it.get("counts"),
            "intro_zh": f"{INT_ZH.get(slug, it.get('name'))} 在本目录中的插件与用例。名称保持英文专有名词。条目均来自 grokbot.dev。",
        })
    dump("integrations.json", {"count": len(items), "items": items})
    return items


def process_news():
    data = load("news.json")
    items = []
    NEWS_ZH = {
        "title": None,
    }
    for n in data.get("items") or []:
        items.append({
            **n,
            "title_zh": n.get("title"),
            "summary_zh": n.get("summary") or n.get("tagline") or "",
            "url": f"/news/",
            "orig_url": n.get("url"),
            "added_zh": zh_date(n.get("added_at") or n.get("published_at")),
        })
    dump("news.json", {"count": len(items), "items": items})


def main():
    plugins = process_plugins()
    templates = process_templates()
    usecases = process_usecases()
    collections = process_collections()
    cats = process_categories(plugins, usecases)
    ints = process_integrations()
    process_news()
    stats = {
        "plugins": len(plugins),
        "use_cases": len(usecases),
        "templates": len(templates),
        "collections": len(collections),
        "categories": len(cats),
        "integrations": len(ints),
        "generated_zh": zh_date(datetime.now(timezone.utc).isoformat()),
        "source_generated_at": load("index.json").get("generated_at"),
        "attribution": "内容译自 grokbot.dev，CC BY 4.0。代码 MIT。独立社区本地化，不隶属于 xAI。",
    }
    dump("stats.json", stats)
    print("localized", stats)


if __name__ == "__main__":
    main()
