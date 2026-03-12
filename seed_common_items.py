from bbq_app.models import BbqItem

# いったん共通テンプレを全部削除
BbqItem.objects.filter(user__isnull=True).delete()

common_items = [
    # 火起こし・調理グッズ
    (BbqItem.Category.FIRE, "BBQコンロ"),
    (BbqItem.Category.FIRE, "網"),
    (BbqItem.Category.FIRE, "鉄板"),
    (BbqItem.Category.FIRE, "火ばさみ"),
    (BbqItem.Category.FIRE, "炭"),
    (BbqItem.Category.FIRE, "着火剤"),
    (BbqItem.Category.FIRE, "火起こし器"),
    (BbqItem.Category.FIRE, "トング"),
    (BbqItem.Category.FIRE, "うちわ"),
    (BbqItem.Category.FIRE, "チャッカマン"),
    (BbqItem.Category.FIRE, "キッチンばさみ"),
    (BbqItem.Category.FIRE, "クーラーボックス"),
    (BbqItem.Category.FIRE, "保冷剤"),
    (BbqItem.Category.FIRE, "使い捨て紙皿"),
    (BbqItem.Category.FIRE, "使い捨てコップ類"),
    (BbqItem.Category.FIRE, "箸"),
    (BbqItem.Category.FIRE, "スプーン"),
    (BbqItem.Category.FIRE, "フォーク"),
    (BbqItem.Category.FIRE, "包丁"),
    (BbqItem.Category.FIRE, "まな板"),
    (BbqItem.Category.FIRE, "食器用洗剤"),
    (BbqItem.Category.FIRE, "スポンジ"),

    # 会場設営
    (BbqItem.Category.PLACE, "テーブル"),
    (BbqItem.Category.PLACE, "椅子"),
    (BbqItem.Category.PLACE, "レジャーシート"),
    (BbqItem.Category.PLACE, "タープ"),
    (BbqItem.Category.PLACE, "ブランケット"),

    # 食材・飲み物
    (BbqItem.Category.FOOD, "お肉"),
    (BbqItem.Category.FOOD, "野菜"),
    (BbqItem.Category.FOOD, "海鮮類"),
    (BbqItem.Category.FOOD, "ソフトドリンク"),
    (BbqItem.Category.FOOD, "ビール"),
    (BbqItem.Category.FOOD, "ワイン"),
    (BbqItem.Category.FOOD, "ウィスキー"),
    (BbqItem.Category.FOOD, "氷"),
    (BbqItem.Category.FOOD, "炭酸水"),
    (BbqItem.Category.FOOD, "焼肉のたれ"),
    (BbqItem.Category.FOOD, "塩・胡椒"),

    # 便利グッズ
    (BbqItem.Category.CONVENIENCE, "食品保存袋"),
    (BbqItem.Category.CONVENIENCE, "ゴミ袋"),
    (BbqItem.Category.CONVENIENCE, "ウェットティッシュ"),
    (BbqItem.Category.CONVENIENCE, "キッチンペーパー"),
    (BbqItem.Category.CONVENIENCE, "サランサップ"),
    (BbqItem.Category.CONVENIENCE, "アルミホイル"),
    (BbqItem.Category.CONVENIENCE, "タオル"),
    (BbqItem.Category.CONVENIENCE, "使い捨て手袋"),
    (BbqItem.Category.CONVENIENCE, "日焼け止め"),
    (BbqItem.Category.CONVENIENCE, "虫除け・痒み止め"),
    (BbqItem.Category.CONVENIENCE, "耐熱グローブ"),
    (BbqItem.Category.CONVENIENCE, "軍手"),
]

for category, name in common_items:
    BbqItem.objects.create(
        user=None,
        name=name,
        category=category,
    )

print("共通テンプレ登録完了")
print(BbqItem.objects.filter(user__isnull=True).count())