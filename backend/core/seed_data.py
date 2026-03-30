"""
====================================
代码任务: 生成丰富的虚拟测试数据
最后修改: 2026-03-30 20:30
====================================
"""

import random
import asyncio
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import select
from decimal import Decimal

from backend.models import (
    User, Shop, Product, Order, Logistics,
    ProductReview, Customer, Promotion, ShopAnalytics,
    ShopType, ShopStatus, OrderStatus, CustomerLevel, PromotionType, PromotionStatus
)
from backend.database import async_session_maker

fake = Faker('zh_CN')

# 扩展的测试数据配置
TEST_DATA_CONFIG = {
    "users": [
        {"username": "demo_user", "email": "demo@test.com", "password": "demo123"},
        {"username": "test_user1", "email": "user1@test.com", "password": "password123"},
        {"username": "test_user2", "email": "user2@test.com", "password": "password123"},
        {"username": "test_user3", "email": "user3@test.com", "password": "password123"},
        {"username": "premium_user", "email": "premium@test.com", "password": "premium123"},
        {"username": "shop_owner1", "email": "owner1@test.com", "password": "owner123"},
        {"username": "shop_owner2", "email": "owner2@test.com", "password": "owner123"},
        {"username": "analyst_user", "email": "analyst@test.com", "password": "analyst123"},
    ],
    "shops_per_user": [3, 2, 4, 1, 2, 3, 2, 1],
    "products_per_shop": (30, 80),
    "orders_per_shop": (200, 600),
    "customers_per_shop": (50, 150),
    "reviews_per_product": (5, 30),
    "promotions_per_shop": (3, 8),
}

SHOP_NAME_TEMPLATES = [
    "{category}专营店", "{brand}旗舰店", "优选{category}馆",
    "{category}直销店", "{brand}官方店", "精品{category}",
    "{category}大卖场", "{brand}专营", "{category}达人店"
]

PRODUCT_CATEGORIES = [
    "数码", "家电", "服装", "鞋包", "美妆", "家居", "食品",
    "母婴", "运动", "图书", "汽车用品", "办公用品",
    "宠物用品", "户外", "珠宝", "健康保健"
]

PRODUCT_BRANDS = [
    "小米", "华为", "苹果", "耐克", "阿迪达斯", "海尔", "格力",
    "美的", "三只松鼠", "良品铺子", "雅诗兰黛", "兰蔻", "迪奥",
    "李宁", "安踏", "fila", "彪马", "匡威", "vivo", "oppo"
]

CARRIERS = [
    {"name": "顺丰速运", "code": "SF"},
    {"name": "中通快递", "code": "ZTO"},
    {"name": "圆通速递", "code": "YTO"},
    {"name": "韵达速递", "code": "YD"},
    {"name": "申通快递", "code": "STO"},
    {"name": "京东物流", "code": "JD"},
    {"name": "德邦快递", "code": "DB"},
]

REVIEW_TEMPLATES = [
    "质量很好，物流也快，值得购买！",
    "商品收到了，和描述一致，很满意。",
    "包装很精美，送给朋友的，她很喜欢。",
    "性价比很高，推荐购买。",
    "客服态度很好，解答很耐心。",
    "第二次购买了，一如既往的好。",
    "尺寸稍微有点偏，但整体不错。",
    "颜色比图片稍深，但质量很好。",
    "发货速度很快，第二天就到了。",
    "用了几天再来评价，确实不错。",
    "老公很喜欢，说很实用。",
    "给宝宝买的，质量放心。",
    "希望能用久一点，目前感觉不错。",
    "跟之前在别家买的差不多，这个价格更实惠。",
    "已经是第三次购买了，老客户了。",
    "有一点小瑕疵，但不影响使用。",
    "期待已久的东西，终于拿到了。",
    "买给爸妈的，他们觉得很方便。",
    "包装有点破损，但商品没问题。",
    "整体满意，会继续关注这家店。",
]

PROMOTION_NAME_TEMPLATES = [
    "{season}大促", "{category}专场", "会员专享", "限时秒杀",
    "新品首发", "清仓特卖", "满减活动", "包邮活动"
]

PROMOTION_DESCRIPTIONS = [
    "全场满200减30，满500减100",
    "精选商品限时5折起",
    "新用户专享优惠券",
    "会员专享折上折",
    "爆款商品秒杀价",
    "全场包邮，不限金额",
    "买二送一，多买多送",
    "领券立减，先到先得",
]


def hash_password(password: str) -> str:
    """简单的密码哈希"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


async def generate_all_test_data():
    """生成所有测试数据"""
    stats = {
        "users": 0, "shops": 0, "products": 0, "orders": 0,
        "logistics": 0, "customers": 0, "reviews": 0, "promotions": 0, "analytics": 0
    }

    async with async_session_maker() as session:
        # 1. 创建用户
        print("Creating users...")
        users = []
        for user_config in TEST_DATA_CONFIG["users"]:
            user = User(
                username=user_config["username"],
                email=user_config["email"],
                password_hash=hash_password(user_config["password"]),
                phone=fake.phone_number() if random.random() > 0.3 else None,
                is_active=True
            )
            session.add(user)
            users.append(user)
        await session.commit()
        for user in users:
            await session.refresh(user)
        stats["users"] = len(users)

        # 2. 为每个用户创建店铺
        print("Creating shops...")
        all_shops = []
        for i, user in enumerate(users):
            shop_count = TEST_DATA_CONFIG["shops_per_user"][i]
            for j in range(shop_count):
                category = random.choice(PRODUCT_CATEGORIES)
                brand = random.choice(PRODUCT_BRANDS)
                shop_name = fake.random_element(SHOP_NAME_TEMPLATES).format(
                    category=category, brand=brand
                )
                shop = Shop(
                    user_id=user.user_id,
                    shop_name=f"{user.username}_{shop_name}",
                    shop_type=random.choice(list(ShopType)),
                    description=fake.text(max_nb_chars=200),
                    status=ShopStatus.ACTIVE,
                    logo_url=f"https://logo.example.com/{fake.word()}.png"
                )
                session.add(shop)
                all_shops.append(shop)
        await session.commit()
        for shop in all_shops:
            await session.refresh(shop)
        stats["shops"] = len(all_shops)

        # 3. 为每个店铺创建商品
        print("Creating products...")
        all_products = []
        for shop in all_shops:
            product_count = random.randint(*TEST_DATA_CONFIG["products_per_shop"])
            for _ in range(product_count):
                category = random.choice(PRODUCT_CATEGORIES)
                cost_price = random.randint(30, 8000)
                current_price = round(cost_price * random.uniform(1.15, 2.5), 2)
                product = Product(
                    shop_id=shop.shop_id,
                    sku=fake.unique.bothify(text='SKU-????-########'),
                    name=f"{category}_{fake.word()}_{fake.random_int(min=100, max=999)}",
                    description=fake.text(max_nb_chars=500),
                    category=category,
                    brand=random.choice(PRODUCT_BRANDS),
                    cost_price=cost_price,
                    current_price=current_price,
                    original_price=round(cost_price * random.uniform(1.3, 3.0), 2),
                    stock_count=random.randint(0, 2000),
                    sales_count=random.randint(0, 1500),
                    main_image=f"https://img.example.com/{fake.uuid4()}.jpg",
                    images=[f"https://img.example.com/{fake.uuid4()}.jpg" for _ in range(random.randint(1, 5))],
                    is_active=True
                )
                session.add(product)
                all_products.append(product)
        await session.commit()
        stats["products"] = len(all_products)

        # 4. 为每个店铺创建客户
        print("Creating customers...")
        all_customers = []
        for shop in all_shops:
            customer_count = random.randint(*TEST_DATA_CONFIG["customers_per_shop"])
            for _ in range(customer_count):
                level_prob = random.random()
                if level_prob < 0.5:
                    level = CustomerLevel.NORMAL
                elif level_prob < 0.75:
                    level = CustomerLevel.BRONZE
                elif level_prob < 0.9:
                    level = CustomerLevel.SILVER
                elif level_prob < 0.97:
                    level = CustomerLevel.GOLD
                else:
                    level = random.choice([CustomerLevel.PLATINUM, CustomerLevel.DIAMOND])

                total_orders = random.randint(1, 50) if level != CustomerLevel.NORMAL else random.randint(1, 5)
                total_amount = random.randint(5000, 500000) if level != CustomerLevel.NORMAL else random.randint(100, 5000)

                customer = Customer(
                    shop_id=shop.shop_id,
                    name=fake.name(),
                    phone=fake.phone_number(),
                    email=fake.email() if random.random() > 0.3 else None,
                    province=fake.province(),
                    city=fake.city(),
                    district=fake.district(),
                    address=fake.street_address(),
                    level=level,
                    total_orders=total_orders,
                    total_amount=total_amount,
                    avg_order_amount=total_amount // total_orders if total_orders > 0 else 0,
                    last_order_at=fake.date_time_between(start_date='-90d', end_date='now'),
                    first_purchase_at=fake.date_time_between(start_date='-365d', end_date='-30d'),
                    tags=random.sample(["新客", "老客", "高价值", "价格敏感", "品质优先", "易退货"], k=random.randint(0, 3))
                )
                session.add(customer)
                all_customers.append(customer)
        await session.commit()
        stats["customers"] = len(all_customers)

        # 5. 为每个店铺生成订单（过去90天）
        print("Creating orders...")
        all_orders = []
        for shop in all_shops:
            order_count = random.randint(*TEST_DATA_CONFIG["orders_per_shop"])
            shop_products = [p for p in all_products if p.shop_id == shop.shop_id]

            for _ in range(order_count):
                if not shop_products:
                    break
                product = random.choice(shop_products)
                days_ago = random.randint(0, 90)
                created_at = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))

                # 根据订单创建时间决定状态
                if days_ago > 30:
                    status_weights = [OrderStatus.COMPLETED, OrderStatus.COMPLETED, OrderStatus.COMPLETED, OrderStatus.CANCELLED]
                elif days_ago > 7:
                    status_weights = [OrderStatus.COMPLETED, OrderStatus.SHIPPED, OrderStatus.PAID]
                else:
                    status_weights = [OrderStatus.PAID, OrderStatus.PENDING, OrderStatus.SHIPPED, OrderStatus.PENDING]
                status = random.choice(status_weights)

                quantity = random.randint(1, 5)
                order = Order(
                    shop_id=shop.shop_id,
                    platform_order_id=fake.bothify(text='ORD-##########'),
                    product_id=product.product_id,
                    order_no=fake.unique.bothify(text='ON-############'),
                    status=status,
                    total_amount=float(product.current_price or product.cost_price) * quantity,
                    payment_amount=float(product.current_price or product.cost_price) * quantity if status != OrderStatus.PENDING else None,
                    quantity=quantity,
                    buyer_name=fake.name(),
                    buyer_phone=fake.phone_number(),
                    buyer_address=fake.street_address(),
                    remark=fake.sentence() if random.random() > 0.8 else None,
                    created_at=created_at,
                    paid_at=created_at + timedelta(hours=random.randint(1, 24)) if status != OrderStatus.PENDING else None,
                    shipped_at=created_at + timedelta(days=random.randint(1, 3)) if status in [OrderStatus.SHIPPED, OrderStatus.COMPLETED] else None,
                    completed_at=created_at + timedelta(days=random.randint(5, 20)) if status == OrderStatus.COMPLETED else None
                )
                session.add(order)
                all_orders.append(order)
        await session.commit()
        stats["orders"] = len(all_orders)

        # 6. 为已发货订单生成物流信息
        print("Creating logistics...")
        for order in all_orders:
            if order.status in [OrderStatus.SHIPPED, OrderStatus.COMPLETED]:
                carrier = random.choice(CARRIERS)
                logistics = Logistics(
                    order_id=order.order_id,
                    tracking_number=f"{carrier['code']}{fake.numerify(text='##########')}",
                    carrier=carrier['name'],
                    carrier_code=carrier['code'],
                    current_status="已签收" if order.status == OrderStatus.COMPLETED else "运输中",
                    current_location=fake.city() if random.random() > 0.3 else None,
                    tracking_details=generate_tracking_details(
                        carrier['name'],
                        order.shipped_at,
                        order.completed_at
                    ),
                    anomaly_detected=random.random() < 0.03,
                    anomaly_type=random.choice(["延迟", "丢件", "破损", "地址错误"]) if random.random() < 0.03 else None,
                    last_sync_at=datetime.now()
                )
                session.add(logistics)
                stats["logistics"] += 1
        await session.commit()

        # 7. 生成商品评价
        print("Creating product reviews...")
        for product in all_products[:200]:  # 为前200个商品生成评价
            review_count = random.randint(*TEST_DATA_CONFIG["reviews_per_product"])
            for _ in range(review_count):
                # 只有已完成的订单才能评价
                completed_orders = [o for o in all_orders if o.product_id == product.product_id and o.status == OrderStatus.COMPLETED]
                if completed_orders:
                    order = random.choice(completed_orders)
                    review = ProductReview(
                        product_id=product.product_id,
                        shop_id=product.shop_id,
                        order_id=order.order_id,
                        rating=random.choices([5, 4, 3, 2, 1], weights=[0.5, 0.3, 0.12, 0.05, 0.03])[0],
                        content=random.choice(REVIEW_TEMPLATES),
                        images=[f"https://review.example.com/{fake.uuid4()}.jpg" for _ in range(random.randint(0, 3))],
                        buyer_name=fake.name(),
                        seller_reply=fake.sentence() if random.random() > 0.7 else None,
                        replied_at=fake.date_time_between(start_date='-30d', end_date='now') if random.random() > 0.7 else None,
                        status="approved",
                        tags=random.sample(["质量好", "物流快", "价格实惠", "包装精美", "客服好", "性价比高"], k=random.randint(1, 3)),
                        created_at=order.completed_at + timedelta(hours=random.randint(1, 72))
                    )
                    session.add(review)
                    stats["reviews"] += 1
        await session.commit()

        # 8. 生成促销活动
        print("Creating promotions...")
        for shop in all_shops:
            promotion_count = random.randint(*TEST_DATA_CONFIG["promotions_per_shop"])
            for _ in range(promotion_count):
                now = datetime.now()
                start_offset = random.randint(-60, 30)
                start_time = now + timedelta(days=start_offset)
                duration = random.randint(3, 30)

                # 确定状态
                if start_offset < -duration:
                    status = PromotionStatus.ENDED
                elif start_offset < 0:
                    status = PromotionStatus.ACTIVE
                else:
                    status = PromotionStatus.SCHEDULED

                promotion = Promotion(
                    shop_id=shop.shop_id,
                    name=random.choice(PROMOTION_NAME_TEMPLATES).format(
                        season=random.choice(["春季", "夏季", "秋季", "冬季", "年中", "年末"]),
                        category=random.choice(PRODUCT_CATEGORIES)
                    ),
                    description=random.choice(PROMOTION_DESCRIPTIONS),
                    type=random.choice(list(PromotionType)),
                    status=status,
                    start_time=start_time,
                    end_time=start_time + timedelta(days=duration),
                    discount_value=Decimal(str(random.randint(5, 50))),
                    min_amount=Decimal(str(random.randint(100, 500))),
                    max_discount=Decimal(str(random.randint(20, 200))),
                    applicable_products=[p.product_id for p in random.sample([pr for pr in all_products if pr.shop_id == shop.shop_id], k=random.randint(5, 20))] if random.random() > 0.5 else None,
                    applicable_categories=random.sample(PRODUCT_CATEGORIES, k=random.randint(1, 4)) if random.random() > 0.6 else None,
                    stock_limit=random.randint(50, 500) if random.random() > 0.5 else None,
                    per_customer_limit=random.randint(1, 5) if random.random() > 0.7 else None,
                    used_count=random.randint(0, 500) if status == PromotionStatus.ENDED else 0
                )
                session.add(promotion)
                stats["promotions"] += 1
        await session.commit()

        # 9. 生成店铺统计数据（过去60天）
        print("Creating analytics data...")
        for shop in all_shops:
            for days_ago in range(60, 0, -1):
                stat_date = datetime.now() - timedelta(days=days_ago)

                # 获取当天订单
                day_orders = [o for o in all_orders
                             if o.shop_id == shop.shop_id and
                             o.created_at.date() == stat_date.date()]

                gmv = sum(o.total_amount for o in day_orders if o.status != OrderStatus.CANCELLED)
                order_count = len(day_orders)
                completed_count = len([o for o in day_orders if o.status == OrderStatus.COMPLETED])
                cancelled_count = len([o for o in day_orders if o.status == OrderStatus.CANCELLED])

                analytics = ShopAnalytics(
                    shop_id=shop.shop_id,
                    stat_date=stat_date,
                    page_views=random.randint(500, 5000),
                    unique_visitors=random.randint(200, 2000),
                    gmv=gmv,
                    order_count=order_count,
                    paid_order_count=len([o for o in day_orders if o.status in [OrderStatus.PAID, OrderStatus.SHIPPED, OrderStatus.COMPLETED]]),
                    completed_order_count=completed_count,
                    cancelled_order_count=cancelled_count,
                    product_views=random.randint(1000, 8000),
                    add_to_cart_count=random.randint(100, 1000),
                    aov=round(gmv / completed_count, 2) if completed_count > 0 else None,
                    conversion_rate=round(random.uniform(0.01, 0.08), 4),
                    new_customer_count=random.randint(5, 50),
                    refund_amount=random.randint(0, 5000) if random.random() > 0.7 else 0,
                    refund_order_count=random.randint(0, 5) if random.random() > 0.8 else 0,
                    avg_ship_time=random.randint(2, 48)
                )
                session.add(analytics)
                stats["analytics"] += 1
        await session.commit()

    print(f"\nTest data generation complete!")
    return stats


def generate_tracking_details(carrier, shipped_at, completed_at):
    """生成物流轨迹"""
    if not shipped_at:
        return []

    details = [
        {"time": shipped_at.strftime("%Y-%m-%d %H:%M"), "status": "已揽收", "location": "发货地"},
    ]

    # 添加运输中节点
    transit_count = random.randint(1, 3)
    for i in range(transit_count):
        details.append({
            "time": (shipped_at + timedelta(hours=6*(i+1))).strftime("%Y-%m-%d %H:%M"),
            "status": "运输中",
            "location": f"中转站{random.randint(1, 100)}"
        })

    # 派送中
    if completed_at or random.random() > 0.1:
        details.append({
            "time": (shipped_at + timedelta(days=random.randint(1, 3))).strftime("%Y-%m-%d %H:%M"),
            "status": "派送中",
            "location": "目的地网点"
        })

    # 已签收
    if completed_at:
        details.append({
            "time": completed_at.strftime("%Y-%m-%d %H:%M"),
            "status": "已签收",
            "location": "收货地址"
        })

    return details


if __name__ == "__main__":
    asyncio.run(generate_all_test_data())
