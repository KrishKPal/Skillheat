"""
Real RSS sources, grouped by country and category.

Each tuple: (slug, name, feed_url, homepage_url, default_country_code, category)

Categories: ai, vc, startups, developer, general-tech, security, hardware, business
"""

SOURCES = [
    # ─── United States ─────────────────────────────────────────────
    # Major publications
    ("techcrunch",        "TechCrunch",         "https://techcrunch.com/feed/",                              "https://techcrunch.com",        "US", "general-tech"),
    ("the-verge",         "The Verge",          "https://www.theverge.com/rss/index.xml",                    "https://www.theverge.com",      "US", "general-tech"),
    ("ars-technica",      "Ars Technica",       "https://feeds.arstechnica.com/arstechnica/technology-lab",  "https://arstechnica.com",       "US", "general-tech"),
    ("wired",             "Wired",              "https://www.wired.com/feed/rss",                            "https://www.wired.com",         "US", "general-tech"),
    ("engadget",          "Engadget",           "https://www.engadget.com/rss.xml",                          "https://www.engadget.com",      "US", "general-tech"),
    ("404-media",         "404 Media",          "https://www.404media.co/rss/",                              "https://www.404media.co",       "US", "general-tech"),
    ("rest-of-world",     "Rest of World",      "https://restofworld.org/feed/latest/",                      "https://restofworld.org",       "US", "general-tech"),
    ("mit-tech-review",   "MIT Tech Review",    "https://www.technologyreview.com/feed/",                    "https://www.technologyreview.com","US", "general-tech"),
    ("ieee-spectrum",     "IEEE Spectrum",      "https://spectrum.ieee.org/feeds/feed.rss",                  "https://spectrum.ieee.org",     "US", "general-tech"),

    # AI / ML
    ("openai-blog",       "OpenAI",             "https://openai.com/blog/rss/",                              "https://openai.com",            "US", "ai"),
    ("anthropic-news",    "Anthropic",          "https://www.anthropic.com/news/rss.xml",                    "https://www.anthropic.com",     "US", "ai"),
    ("hf-blog",           "Hugging Face",       "https://huggingface.co/blog/feed.xml",                       "https://huggingface.co",        "US", "ai"),
    ("google-research",   "Google Research",    "https://blog.google/technology/ai/rss/",                    "https://blog.google",           "US", "ai"),
    ("nvidia-blog",       "NVIDIA Blog",        "https://blogs.nvidia.com/feed/",                             "https://blogs.nvidia.com",      "US", "ai"),
    ("import-ai",         "Import AI",          "https://jack-clark.net/feed/",                              "https://jack-clark.net",        "US", "ai"),

    # Developer
    ("hacker-news",       "Hacker News",        "https://hnrss.org/frontpage",                               "https://news.ycombinator.com",  "US", "developer"),
    ("dev-to",            "DEV Community",      "https://dev.to/feed",                                        "https://dev.to",                "US", "developer"),
    ("github-blog",       "GitHub Blog",        "https://github.blog/feed/",                                  "https://github.blog",           "US", "developer"),
    ("stack-overflow",    "Stack Overflow Blog","https://stackoverflow.blog/feed/",                          "https://stackoverflow.blog",    "US", "developer"),
    ("lobsters",          "Lobsters",           "https://lobste.rs/rss",                                      "https://lobste.rs",             "US", "developer"),
    ("changelog",         "Changelog",          "https://changelog.com/feed",                                 "https://changelog.com",         "US", "developer"),
    ("css-tricks",        "CSS-Tricks",         "https://css-tricks.com/feed/",                               "https://css-tricks.com",        "US", "developer"),

    # VC / Startups
    ("a16z",              "Andreessen Horowitz","https://a16z.com/feed/",                                    "https://a16z.com",              "US", "vc"),
    ("ycombinator",       "Y Combinator Blog",  "https://www.ycombinator.com/blog/rss",                      "https://www.ycombinator.com",   "US", "vc"),
    ("first-round",       "First Round Review", "https://review.firstround.com/rss",                         "https://review.firstround.com", "US", "vc"),

    # Big Tech blogs
    ("apple-newsroom",    "Apple Newsroom",     "https://www.apple.com/newsroom/rss-feed.rss",               "https://www.apple.com/newsroom","US", "general-tech"),
    ("microsoft-blog",    "Microsoft Blog",     "https://blogs.microsoft.com/feed/",                          "https://blogs.microsoft.com",   "US", "general-tech"),
    ("aws-blog",          "AWS News Blog",      "https://aws.amazon.com/blogs/aws/feed/",                     "https://aws.amazon.com",        "US", "developer"),
    ("cloudflare-blog",   "Cloudflare Blog",    "https://blog.cloudflare.com/rss/",                           "https://blog.cloudflare.com",   "US", "developer"),
    ("vercel-blog",       "Vercel Blog",        "https://vercel.com/atom",                                    "https://vercel.com",            "US", "developer"),

    # Security
    ("krebs",             "Krebs on Security",  "https://krebsonsecurity.com/feed/",                          "https://krebsonsecurity.com",   "US", "security"),
    ("bleeping",          "Bleeping Computer",  "https://www.bleepingcomputer.com/feed/",                    "https://www.bleepingcomputer.com","US", "security"),

    # ─── India ─────────────────────────────────────────────────────
    ("yourstory",         "YourStory",          "https://yourstory.com/feed",                                "https://yourstory.com",         "IN", "startups"),
    ("inc42",             "Inc42",              "https://inc42.com/feed/",                                   "https://inc42.com",             "IN", "startups"),
    ("entrackr",          "Entrackr",           "https://entrackr.com/feed/",                                "https://entrackr.com",          "IN", "startups"),
    ("moneycontrol-tech", "MoneyControl Tech",  "https://www.moneycontrol.com/rss/technology.xml",           "https://www.moneycontrol.com",  "IN", "general-tech"),
    ("the-ken",           "The Ken",            "https://the-ken.com/feed/",                                  "https://the-ken.com",           "IN", "business"),
    ("medianama",         "MediaNama",          "https://medianama.com/feed/",                                "https://medianama.com",         "IN", "general-tech"),
    ("the-arc-india",     "The Arc",            "https://thearc.in/feed",                                     "https://thearc.in",             "IN", "general-tech"),
    ("analytics-india",   "Analytics India",    "https://analyticsindiamag.com/feed/",                        "https://analyticsindiamag.com", "IN", "ai"),

    # ─── United Kingdom ───────────────────────────────────────────
    ("the-register",      "The Register",       "https://www.theregister.com/headlines.atom",                "https://www.theregister.com",   "GB", "developer"),
    ("bbc-tech",          "BBC Technology",     "https://feeds.bbci.co.uk/news/technology/rss.xml",          "https://www.bbc.com",           "GB", "general-tech"),
    ("techradar",         "TechRadar",          "https://www.techradar.com/rss",                             "https://www.techradar.com",     "GB", "general-tech"),
    ("sifted",            "Sifted",             "https://sifted.eu/feed",                                     "https://sifted.eu",             "GB", "vc"),
    ("tech-eu",           "Tech.eu",            "https://tech.eu/feed/",                                      "https://tech.eu",               "GB", "general-tech"),
    ("financial-times-tech","FT Technology",    "https://www.ft.com/technology?format=rss",                  "https://www.ft.com",            "GB", "business"),
    ("guardian-tech",     "Guardian Tech",      "https://www.theguardian.com/technology/rss",                "https://www.theguardian.com",   "GB", "general-tech"),

    # ─── Germany ───────────────────────────────────────────────────
    ("heise",             "Heise Online",       "https://www.heise.de/rss/heise-atom.xml",                   "https://www.heise.de",          "DE", "developer"),
    ("eu-startups",       "EU-Startups",        "https://www.eu-startups.com/feed/",                          "https://www.eu-startups.com",   "DE", "startups"),
    ("deutsche-startups", "Deutsche Startups",  "https://www.deutsche-startups.de/feed/",                     "https://www.deutsche-startups.de","DE", "startups"),

    # ─── France ────────────────────────────────────────────────────
    ("frenchweb",         "FrenchWeb",          "https://www.frenchweb.fr/feed",                             "https://www.frenchweb.fr",      "FR", "startups"),
    ("maddyness",         "Maddyness",          "https://www.maddyness.com/feed/",                            "https://www.maddyness.com",     "FR", "startups"),

    # ─── Canada ────────────────────────────────────────────────────
    ("betakit",           "BetaKit",            "https://betakit.com/feed/",                                 "https://betakit.com",           "CA", "startups"),
    ("the-logic",         "The Logic",          "https://thelogic.co/feed/",                                  "https://thelogic.co",           "CA", "general-tech"),

    # ─── Singapore (covers SE Asia) ────────────────────────────────
    ("e27",               "e27",                "https://e27.co/feed/",                                      "https://e27.co",                "SG", "startups"),
    ("tech-in-asia",      "Tech in Asia",       "https://www.techinasia.com/rss",                             "https://www.techinasia.com",    "SG", "startups"),
    ("kr-asia",           "KrASIA",             "https://kr-asia.com/feed",                                   "https://kr-asia.com",           "SG", "startups"),
    # ─── China ────────────────────────────────────────────────
    ("technode", "TechNode", "https://technode.com/feed/", "https://technode.com", "CN", "general-tech"),
    ("pandaily", "Pandaily", "https://pandaily.com/feed/", "https://pandaily.com", "CN", "general-tech"),
    ("kr-asia-cn", "KrASIA China", "https://kr-asia.com/feed", "https://kr-asia.com", "CN", "startups"),
    ("36kr-en", "36Kr (EN)", "https://36kr.com/feed", "https://36kr.com", "CN", "startups"),
    ("caixin-tech", "Caixin Tech", "https://www.caixinglobal.com/feed/", "https://www.caixinglobal.com", "CN", "business"),
    # ─── Japan ────────────────────────────────────────────────
    ("japan-times-tech", "Japan Times Tech", "https://www.japantimes.co.jp/news_category/tech/feed/",
     "https://www.japantimes.co.jp", "JP", "general-tech"),
    ("nikkei-tech", "Nikkei Asia Tech", "https://asia.nikkei.com/rss/feed/nar", "https://asia.nikkei.com", "JP",
     "business"),
    ("techable", "Techable Japan", "https://techable.jp/feed", "https://techable.jp", "JP", "startups"),
    ("thebridge", "The Bridge", "https://thebridge.jp/en/feed", "https://thebridge.jp", "JP", "startups"),

    # ─── South Korea ───────────────────────────────────────────────
    ("the-elec",          "The Elec",           "https://www.thelec.net/rss/allArticle.xml",                 "https://www.thelec.net",        "KR", "hardware"),

    # ─── Israel ────────────────────────────────────────────────────
    ("ctech",             "CTech",              "https://www.calcalistech.com/GeneralRSS/0,16335,L-3700,00.xml","https://www.calcalistech.com","IL", "startups"),
    ("times-of-israel-tech","Times of Israel Tech","https://www.timesofisrael.com/topic/tech-israel/feed/",  "https://www.timesofisrael.com", "IL", "startups"),

    # ─── Brazil ────────────────────────────────────────────────────
    ("olhar-digital",     "Olhar Digital",      "https://olhardigital.com.br/feed/",                         "https://olhardigital.com.br",   "BR", "general-tech"),
    ("labs-news",         "LABS — Latam",       "https://labsnews.com/en/feed/",                              "https://labsnews.com",          "BR", "startups"),

    # ─── Mexico ────────────────────────────────────────────────────
    ("contxto",           "Contxto",            "https://www.contxto.com/en/feed/",                          "https://www.contxto.com",       "MX", "startups"),

    # ─── Australia ─────────────────────────────────────────────────
    ("startup-daily",     "StartupDaily",       "https://www.startupdaily.net/feed/",                        "https://www.startupdaily.net",  "AU", "startups"),
    ("itnews-au",         "iTnews Australia",   "https://www.itnews.com.au/RSS/rss.ashx?CIID=192",           "https://www.itnews.com.au",     "AU", "general-tech"),

    # ─── Africa ────────────────────────────────────────────────────
    ("techcabal",         "TechCabal",          "https://techcabal.com/feed/",                                "https://techcabal.com",         "NG", "startups"),
    ("disrupt-africa",    "Disrupt Africa",     "https://disrupt-africa.com/feed/",                           "https://disrupt-africa.com",    "ZA", "startups"),
    ("techpoint-africa",  "Techpoint Africa",   "https://techpoint.africa/feed/",                             "https://techpoint.africa",      "NG", "startups"),

    # ─── Spain ─────────────────────────────────────────────────────
    ("xataka",            "Xataka",             "https://www.xataka.com/feedburner.xml",                     "https://www.xataka.com",        "ES", "general-tech"),

    # ─── Netherlands ───────────────────────────────────────────────
    ("silicon-canals",    "Silicon Canals",     "https://siliconcanals.com/feed/",                            "https://siliconcanals.com",     "NL", "startups"),

    # ─── Sweden ────────────────────────────────────────────────────
    ("breakit",           "Breakit",            "https://www.breakit.se/feed",                                "https://www.breakit.se",        "SE", "startups"),

    # ─── Italy ────────────────────────────────────────────────────
    ("wired-it", "Wired Italia", "https://www.wired.it/feed/", "https://www.wired.it", "IT", "general-tech"),
    ("startup-italia", "Startup Italia", "https://startupitalia.eu/feed/", "https://startupitalia.eu", "IT", "startups"),

    # ─── Poland ────────────────────────────────────────────────────
    ("spidersweb", "Spider’s Web", "https://spidersweb.pl/feed", "https://spidersweb.pl", "PL", "general-tech"),
    ("mamstartup", "MamStartup", "https://mamstartup.pl/feed/", "https://mamstartup.pl", "PL", "startups"),
    # ───Turkey ────────────────────────────────────────────────────
    ("webrazzi", "Webrazzi", "https://webrazzi.com/feed/", "https://webrazzi.com", "TR", "startups"),
    # ─── Indonesia ────────────────────────────────────────────────────
    ("daily-social", "DailySocial", "https://dailysocial.id/feed", "https://dailysocial.id", "ID", "startups"),
    # ─── Philippines ────────────────────────────────────────────────────
    ("yugatech", "YugaTech", "https://www.yugatech.com/feed/", "https://www.yugatech.com", "PH", "general-tech"),
    # ─── Veitnam ────────────────────────────────────────────────────
    ("vietnam-briefing-tech", "Vietnam Briefing Tech", "https://www.vietnam-briefing.com/news/category/technology/feed", "https://www.vietnam-briefing.com", "VN", "general-tech"),
    # ─── Ireland ───────────────────────────────────────────────────
    ("siliconrepublic",   "Silicon Republic",   "https://www.siliconrepublic.com/feed",                       "https://www.siliconrepublic.com","IE", "general-tech"),

    # ─── Egypt ───────────────────────────────────────────────────
    ("egyptian-streets-tech", "Egyptian Streets Tech", "https://egyptianstreets.com/category/tech/feed/", "https://egyptianstreets.com", "EG", "general-tech"),

    # ─── South Africa ───────────────────────────────────────────────────
    ("mybroadband", "MyBroadband", "https://mybroadband.co.za/news/feed", "https://mybroadband.co.za", "ZA", "general-tech"),
    # ─── Argentina ─────────────────────────────────────────────
    ("infotechnology", "Infotechnology", "https://www.infotechnology.com/feed", "https://www.infotechnology.com", "AR", "general-tech"),

    # ─── Chile ─────────────────────────────────────────────────
    ("fayerwayer", "FayerWayer", "https://www.fayerwayer.com/feed/", "https://www.fayerwayer.com", "CL", "general-tech"),

    # ─── Colombia ──────────────────────────────────────────────
    ("pulzo-tech", "Pulzo Tech", "https://www.pulzo.com/rss/tecnologia.xml", "https://www.pulzo.com", "CO", "general-tech"),

    # ─── Russia (careful politically) ──────────────────────────
    ("vc-ru", "VC.ru", "https://vc.ru/rss/all", "https://vc.ru", "RU", "startups"),

    # ─── Ukraine ───────────────────────────────────────────────
    ("ain-ua", "AIN.UA", "https://ain.ua/feed/", "https://ain.ua", "UA", "startups"),

    # ─── Finland ───────────────────────────────────────────────
    ("arctic-startup", "ArcticStartup", "https://arcticstartup.com/feed/", "https://arcticstartup.com", "FI", "startups"),

    # ─── Denmark ───────────────────────────────────────────────
    ("bootstrapping", "Bootstrapping.dk", "https://bootstrapping.dk/feed/", "https://bootstrapping.dk", "DK", "startups"),

    # ─── Norway ────────────────────────────────────────────────
    ("shifter", "Shifter", "https://shifter.no/rss", "https://shifter.no", "NO", "startups"),

    # ─── Portugal ──────────────────────────────────────────────
    ("dinheiro-vivo-tech", "Dinheiro Vivo Tech", "https://www.dinheirovivo.pt/rss/tecnologia.xml", "https://www.dinheirovivo.pt", "PT", "general-tech"),

    # ─── Greece ────────────────────────────────────────────────
    ("startupper", "Startupper Greece", "https://startupper.gr/feed/", "https://startupper.gr", "GR", "startups"),

    # ─── New Zealand ───────────────────────────────────────────
    ("nz-herald-tech", "NZ Herald Tech", "https://www.nzherald.co.nz/rss/technology/", "https://www.nzherald.co.nz", "NZ", "general-tech"),

    # ─── Switzerland ───────────────────────────────────────────────
    ("inside-it",         "Inside-IT.ch",       "https://www.inside-it.ch/feed",                              "https://www.inside-it.ch",      "CH", "general-tech"),

    # ─── United Arab Emirates ──────────────────────────────────────
    ("magnitt", "MAGNiTT", "https://magnitt.com/feed", "https://magnitt.com", "SA", "startups" ),( "wamda",             "Wamda",              "https://www.wamda.com/feed",                                 "https://www.wamda.com",         "AE", "startups"),
]
